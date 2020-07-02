# -*- encoding: utf-8
# yapf: disable


checkname = 'apc_rackpdu_power'


info = [[[u'pb-n15-115', u'420']],
        [[u'2']],
        [[u'1', u'20', u'1'], [u'2', u'10', u'1'], [u'3', u'9', u'1']]]


discovery = {'': [(u'Bank 2', {}), (u'Bank 3', {}), (u'Device pb-n15-115', {})]}


checks = {'': [(u'Bank 2',
                {},
                [(0, 'Current: 1.0 A', [('current', 1.0, None, None, None, None)]),
                 (0, 'load normal', [])]),
               (u'Bank 3',
                {},
                [(0, 'Current: 0.9 A', [('current', 0.9, None, None, None, None)]),
                 (0, 'load normal', [])]),
               (u'Device pb-n15-115',
                {},
                [(0, 'Current: 2.0 A', [('current', 2.0, None, None, None, None)]),
                 (0, 'load normal', []),
                 (0, 'Power: 420.0 W', [('power', 420.0, None, None, None, None)])])]}