import unittest
from GEDReader import GEDReader
from typing import List


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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
