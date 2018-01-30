import os
import pytest
import re
from remote import actual_output, config, remotetest, wait_agent, write_config


@pytest.fixture
def testfile():
    return os.path.basename(__file__)


@pytest.fixture
def testconfig(config):
    section = 'wmi_cpuload'
    config.set("global", "sections", section)
    config.set("global", "crash_debug", "yes")
    return config


@pytest.fixture
def expected_output():
    return [
        re.escape(r'<<<wmi_cpuload:sep(44)>>>'),
        re.escape(r'[system_perf]'),
        (r'AlignmentFixupsPersec,Caption,ContextSwitchesPersec,Description,'
         r'ExceptionDispatchesPersec,FileControlBytesPersec,'
         r'FileControlOperationsPersec,FileDataOperationsPersec,'
         r'FileReadBytesPersec,FileReadOperationsPersec,FileWriteBytesPersec,'
         r'FileWriteOperationsPersec,FloatingEmulationsPersec,Frequency_Object,'
         r'Frequency_PerfTime,Frequency_Sys100NS,Name,'
         r'PercentRegistryQuotaInUse,PercentRegistryQuotaInUse_Base,Processes,'
         r'ProcessorQueueLength,SystemCallsPersec,SystemUpTime,Threads,'
         r'Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS'),
        (r'\d+,,\d+,,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,,\d+,'
         r'\-?\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+'),
        re.escape(r'[computer_system]'),
        (r'AdminPasswordStatus,AutomaticManagedPagefile,'
         r'AutomaticResetBootOption,AutomaticResetCapability,BootOptionOnLimit,'
         r'BootOptionOnWatchDog,BootROMSupported,BootStatus,BootupState,'
         r'Caption,ChassisBootupState,ChassisSKUNumber,CreationClassName,'
         r'CurrentTimeZone,DaylightInEffect,Description,DNSHostName,Domain,'
         r'DomainRole,EnableDaylightSavingsTime,FrontPanelResetStatus,'
         r'HypervisorPresent,InfraredSupported,InitialLoadInfo,InstallDate,'
         r'KeyboardPasswordStatus,LastLoadInfo,Manufacturer,Model,Name,'
         r'NameFormat,NetworkServerModeEnabled,NumberOfLogicalProcessors,'
         r'NumberOfProcessors,OEMLogoBitmap,OEMStringArray,PartOfDomain,'
         r'PauseAfterReset,PCSystemType,PCSystemTypeEx,'
         r'PowerManagementCapabilities,PowerManagementSupported,'
         r'PowerOnPasswordStatus,PowerState,PowerSupplyState,'
         r'PrimaryOwnerContact,PrimaryOwnerName,ResetCapability,ResetCount,'
         r'ResetLimit,Roles,Status,SupportContactDescription,SystemFamily,'
         r'SystemSKUNumber,SystemStartupDelay,SystemStartupOptions,'
         r'SystemStartupSetting,SystemType,ThermalState,TotalPhysicalMemory,'
         r'UserName,WakeUpType,Workgroup'),
        (r'\d+,\d+,\d+,\d+,\d*,\d*,\d+,[^,]*,[^,]+,[\w-]+,\d+,,\w+,\d+,\d+,'
         r'[^,]+,[\w-]+,[^,]+,\d+,\d+,\d+,\d+,\d+,,,\d+,,[^,]+(, [^,]+)?,[^,]+,'
         r'[\w-]+,,\d+,\d+,\d+,,[^,]+,\d+,\-?\d+,\d+,\d+,,,\d+,\d+,\d+,,[\w-]+,'
         r'\d+,\-?\d+,\-?\d+,[^,]+,\w+,,[^,]*,,,,,[^,]+,\d+,\d+,[^,]*,\d+,\w*')
    ]


def test_section_wmi_cpuload(testconfig, expected_output, actual_output,
                             testfile):
    remotetest(expected_output, actual_output, testfile)
