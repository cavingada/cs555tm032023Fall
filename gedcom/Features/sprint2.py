from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import get_age
import datetime


import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')


# US12: Parents too old
def check_parents_too_old(individuals):

    allErrors=[]
    
    def get_parent_age(row):
        birthday = row['BIRT']
        # return how old the person is by taking today's date and subtracting birthday
        return get_age(birthday)
    
    for _, row in individuals.iterrows():
        if not pd.isna(row['ID']) and row['ID'] != 'NA': 
            numChildren = len(row['FAMC'])
            isParent = numChildren > 0
            age = get_parent_age(row)
            if isParent and age > 100:
                error = f"ERROR: INDIVIDUAL: US12: {row['ID']} is a parent and too old"
                allErrors.append(error)

    return allErrors

def printAllSprint2Errors(individuals, families, destination):
    """US07ERRORS = check_dates_before_current(individuals, families)
    US08ERRORS = check_birth_before_marriage(individuals, families)
    US09ERRORS = check_birth_before_death(individuals)
    US10ERRORS = check_marriage_before_divorce(families)
    US11ERRORS = check_marriage_before_death(individuals, families)"""
    US12ERRORS = check_parents_too_old(individuals)

    # combine all 6 lists above
    allErrors = US12ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)