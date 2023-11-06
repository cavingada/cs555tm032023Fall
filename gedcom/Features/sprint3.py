from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import get_age, compare_dates
from datetime import datetime
from dateutil.relativedelta import relativedelta
from gedcom.Features.utils import get_error_msg
import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')

#US13: Siblings spacing

#US14: Multiple births <=5


# US15: Fewer than 15 siblings



# US16: Male last names

# US17: No marriages to descendants


# US18: Sibligns should not marry


def printAllSprint3Errors(individuals, families, destination):
    US13ERRORS = check_less_than_150_years_old(individuals)
    US14ERRORS = check_birth_before_marriage(individuals, families)
    US15ERRORS = check_birth_before_death_of_parents(individuals, families)
    US16ERRORS = check_marriage_after_14(individuals, families)
    US17ERRORS = check_bigamy(individuals, families)
    US18ERRORS = check_parents_too_old(individuals)

    # combine all 6 lists above
    allErrors = US13ERRORS + US14ERRORS + US15ERRORS + US16ERRORS + US17ERRORS + US18ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)