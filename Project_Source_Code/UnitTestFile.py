import unittest
from GEDReader import GEDReader


class GEDReaderTest(unittest.TestCase):
    def test_us25(self):
        # Unit Test for User Story 25
        reader_us25: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS25.ged')
        self.assertFalse(reader_us25.get_individual('I8').is_valid)

    def test_us26(self):
        # Unit Test for User Story 26
        reader_us26: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS26.ged')
        self.assertFalse(reader_us26.get_individual('I4').is_valid)
        self.assertFalse(reader_us26.get_individual('I5').is_valid)

    def test_us28(self):
        # Unit Test for User Story 28
        reader_us28: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS28.ged')
        f = reader_us28.get_family('F3')
        ordered_siblings = f.order_siblings_by_age()
        self.assertEqual(ordered_siblings, ['Qiaoqiao /Xi/', 'Anan /Xi/', 'Jinping /Xi/', 'Yuanping /Xi/'])

    def test_us08(self):
        # Unit Test for User Story 08
        reader_us08: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS08.ged')
        self.assertFalse(reader_us08.get_individual('I1').is_valid)

    def test_us35(self):
        # Unit Test for User Story 35
        reader_us35: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS35.ged')
        recent_birth = reader_us35.list_recent_birth()
        self.assertEqual([i.name for i in recent_birth], ['Mingze /Xi/'])

    def test_us36(self):
        # Unit Test for User Story 36
        reader_us36: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS36.ged')
        recent_death = reader_us36.list_recent_death()
        self.assertEqual([i.name for i in recent_death], ['Zhongxun /Xi/'])

    def test_us37(self):
        # Unit Test for User Story 37
        reader_us37: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS37.ged')
        recent_survivors = reader_us37.list_recent_survivors()
        self.assertEqual(sorted([i.name for i in recent_survivors]), ['Anan /Xi/',
                                                                      'Jinping /Xi/',
                                                                      'Mingze /Xi/',
                                                                      'Qiaoqiao /Xi/',
                                                                      'Xin /Qi/',
                                                                      'Yuanping /Xi/'])

    def test_us41(self):
        # Unit Test for User Story 41
        reader_us41: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS41.ged')
        i = reader_us41.get_individual('I1')
        self.assertEqual(str(i.birthday), '1953-1-1')

    def test_us32(self):
        # Unit Test for User Story 32
        reader_us32: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS32.ged')
        multibirths = reader_us32.list_multiple_births()
        self.assertEqual([[i.name for i in l] for l in multibirths], [['Jinping /Xi/', 'Yuanping /Xi/']])

    def test_us33(self):
        # Unit Test for User Story 33
        reader_us33: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS33.ged')
        orphans = reader_us33.list_orphans()
        self.assertEqual([i.name for i in orphans], ['Mingze /Xi/'])

    def test_us34(self):
        # Unit Test for User Story 34
        reader_us34: GEDReader = GEDReader('UnitTestGEDFile/UnitTestUS34.ged')
        large_gap_couples = reader_us34.list_spouse_age_gap_large()
        self.assertEqual([[i.name for i in p] for p in large_gap_couples], [['Jinping /Xi/', 'Liyuan /Peng/']])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
