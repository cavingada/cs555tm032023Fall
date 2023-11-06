from gedcom.Features.sprint3 import check_multiple_births, check_siblings_spacing
import unittest
from gedcom.gedcom_parse import get_gedcom_df
import os

class TestUS(unittest.TestCase):
    
    def setUp(self):
        cwd = os.getcwd()
        self.individuals, self.families = get_gedcom_df(f'{cwd}/gedcom/example.ged')
        self.errors = check_siblings_spacing(self.individuals, self.families)
        self.errors += check_multiple_births(self.individuals, self.families)

    
    def test_too_close(self):
        self.assertEqual(self.errors[0], 'ERROR: FAMILY: US13: @I8@ and @I11@ are born less than 8 months of each other and are not twins')
        self.assertEqual(self.errors[1], 'ERROR: FAMILY: US13: @I9@ and @I11@ are born less than 8 months of each other and are not twins')
        self.assertEqual(self.errors[2], 'ERROR: FAMILY: US13: @I10@ and @I11@ are born less than 8 months of each other and are not twins')
        self.assertEqual(self.errors[3], 'ERROR: FAMILY: US13: @I12@ and @I11@ are born less than 8 months of each other and are not twins')
        self.assertEqual(self.errors[4], 'ERROR: FAMILY: US13: @I13@ and @I11@ are born less than 8 months of each other and are not twins')
        self.assertEqual(self.errors[5], 'ERROR: FAMILY: US13: @I14@ and @I11@ are born less than 8 months of each other and are not twins')

    
    def test_multiple_births(self):
        self.assertEqual(self.errors[6], 'ERROR: FAMILY: US14: @F1@ has more than 5 children born on 1999-01-01 00:00:00')

    def test_no_errors(self):
        cwd = os.getcwd()
        ind, fam = get_gedcom_df(f'{cwd}/gedcom/Tests/Pranav/sprint3_no_errors.ged')
        errors = check_siblings_spacing(ind, fam)
        errors += check_multiple_births(ind, fam)
        self.assertEqual(len(errors), 0)

if __name__ == '__main__':
    unittest.main()