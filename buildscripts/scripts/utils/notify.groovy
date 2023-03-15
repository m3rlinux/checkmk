#!groovy

/// file: notify.groovy

import org.codehaus.groovy.runtime.StackTraceUtils;

def get_author_email() {
    // Workaround since CHANGE_AUTHOR_EMAIL is not available
    // Bug: https://issues.jenkins-ci.org/browse/JENKINS-39838
    return (
        onWindows ?
        /// windows will replace %ae with ae..
        cmd_output('git log -1 --pretty=format:%%ae') :
        cmd_output('git log -1 --pretty=format:%ae'))
}

// Send a build failed massage to jenkins
def slack_build_failed(error) {
    slackSend(
        botUser: true,
        color: 'danger',
        message: ("""
            |Build Failed:
            |    ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)
            |Error Message:
            |    ${error}
            |""".stripMargin()),
    )
}


def notify_error(error) {
    // It seems the option "Allowed domains" is not working properly.
    // See: https://ci.lan.tribe29.com/configure
    // So ensure here we only notify internal addresses.
    try {
        def isChangeValidation = currentBuild.fullProjectName.contains("change_validation");
        print("|| error-reporting: isChangeValidation=${isChangeValidation}");

        def isFirstFailure = currentBuild.getPreviousBuild()?.result == "FAILURE";
        print("|| error-reporting: isFirstFailure=${isFirstFailure}");

        if (isFirstFailure && ! isChangeValidation) {
            /// include me for now to give me the chance to debug
            def notify_emails = [
                "frans.fuerst@tribe29.com",
            ];
            currentBuild.changeSets.each { changeSet -> 
                print("|| error-reporting:   changeSet=${changeSet}");
                print("|| error-reporting:   changeSet.items=${changeSet.items}");

                def culprits_emails = changeSet.items.collect {e -> e.authorEmail};
                print("|| error-reporting:   culprits_emails ${culprits_emails}");

                notify_emails += culprits_emails;
                print("|| error-reporting:   notify_emails ${notify_emails}");
            }

            // It seems the option "Allowed domains" is not working properly.
            // See: https://ci.lan.tribe29.com/configure
            // So ensure here we only notify internal addresses.
            notify_emails = notify_emails.unique(false).findAll({
                it != "weblate@checkmk.com" && it.endsWith("@tribe29.com")
            });

            /// fallback - for investigation
            notify_emails = notify_emails ?: [
                "timotheus.bachinger@tribe29.com", "frans.fuerst@tribe29.com"];

            print("|| error-reporting: notify_emails ${notify_emails}");

            mail(
                to: "", // no direct contact
                cc: "", // the code owner maybe
                bcc: "${notify_emails.join(',')}",
                from: "\"Greetings from CI\" <${JENKINS_MAIL}>",
                replyTo: "\"Team CI\" <${TEAM_CI_MAIL}>",
                subject: "Exception in ${env.JOB_NAME}",
                body: ("""
    |The following build failed:
    |    ${env.BUILD_URL}
    |
    |The error message was:
    |    ${error}
    |
    |If you wonder why you got this mail, please reply and let's together find out what went wrong
    |""".stripMargin()),
           )
        }

    } catch(Exception exc) {
        print("Could not report error by mail - got ${exc}");
    }

    // Disabled for the moment. It currently does not work because of some
    // wrong configuration.
    //
    // From the build logs:
    //
    // [Pipeline] slackSend
    // Slack Send Pipeline step running, values are - baseUrl: <empty>,
    // teamDomain: <empty>, channel: build-notifications, color: danger,
    // botUser: true, tokenCredentialId: <empty>, iconEmoji <empty>, username
    // <empty>
    //ERROR: Slack notification failed with exception: java.lang.IllegalArgumentException: the token with the provided ID could not be found and no token was specified
    //
    //slack_build_failed(error)
    // after notifying everybody, the error needs to be thrown again
    // This ensures that the build status is set correctly

    StackTraceUtils.sanitize(error);
    print("ERROR: ${error.stackTrace.head()}: ${error}");
    throw error;
}

return this;
