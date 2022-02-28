import unittest
import Project02_ShengpingXu as p2
from typing import List


class GEDReaderTest(unittest.TestCase):
    def test_ged_reader(self):
        reader: p2.GEDReader = p2.GEDReader()
        ged_data: List[str] = reader.read_ged_data('project01_ShengpingXu.ged')
        # General test case
        self.assertEqual(ged_data[11], '2|NAME|Y|Jinping Xi')
        # Test case that the label is valid
        self.assertEqual(ged_data[5], '1|DATE|Y|6 FEB 2022')
        # Test case that the label is invalid
        self.assertEqual(ged_data[8], '2|VERS|N|5.5.1')
        # Test case of the special INDI label
        self.assertEqual(ged_data[14], '0|INDI|Y|@I1@')
        # Test case that there are only 2 elements in the line
        self.assertEqual(ged_data[1], '0|HEAD|Y|')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
