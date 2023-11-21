from gedcom.Features.sprint4 import check_first_cousins_marry, check_aunts_uncles_marry
import unittest
from gedcom.gedcom_parse import get_gedcom_df
import os


class TestUS(unittest.TestCase):

    def setUp(self):
        cwd = os.getcwd()
        self.individuals, self.families = get_gedcom_df(f'{cwd}/gedcom/Tests/Pranav/sprint4errors.ged')
        self.errors = check_first_cousins_marry(self.individuals, self.families)
        self.errors += check_aunts_uncles_marry(self.individuals, self.families)
        print(self.errors)


    def test_first_cousins_marry(self):
        self.assertEqual(self.errors[0], 'ERROR: FAMILY: US19: @I1@ and @I2@ are first cousins and should not marry')

    def test_aunts_uncles_marry(self):
        self.assertEqual(self.errors[1], 'ERROR: FAMILY: US20: @I9@ and @I10@ are aunt/uncle and nephew/niece and should not marry')

    def test_no_errors(self):
        cwd = os.getcwd()
        individuals, families = get_gedcom_df(f'{cwd}/gedcom/Tests/Pranav/sprint4_noerrors.ged')
        errors = check_first_cousins_marry(individuals, families)
        errors += check_aunts_uncles_marry(individuals, families)
        self.assertEqual(len(errors), 0)




if __name__ == '__main__':
    unittest.main()