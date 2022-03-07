import unittest
import GEDReader as p2
from typing import List


class GEDReaderTest(unittest.TestCase):
    def test_ged_reader(self):
        reader: p2.GEDReader = p2.GEDReader('Project01_ShengpingXu.ged')
        # General test case
        self.assertEqual(reader.get_name('I1'), 'Jinping /Xi/')
        # Test case that the label is valid
        self.assertEqual(reader.get_name('I2'), 'Zhongxun /Xi/')
        # Test case that the label is invalid
        self.assertEqual(reader.get_age('I10'), 59)
        # Test case of the special INDI label
        self.assertEqual(reader.get_marriage_date('F1'), '1987-9-1')
        # Test case that there are only 2 elements in the line
        self.assertEqual(reader.get_divorced_date('F1'), 'None')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
