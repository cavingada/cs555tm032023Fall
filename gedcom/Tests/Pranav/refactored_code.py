from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import get_age, compare_dates
from datetime import datetime
from dateutil.relativedelta import relativedelta
from gedcom.Features.utils import get_error_msg
import os


def check_less_than_150_years_old(individuals):
    allErrors = []
    for _, row in individuals.iterrows(): 
        age = get_age(row['BIRT'])
        if age > 150:
            allErrors.append(f"ERROR: INDIVIDUAL: US07: {row['ID']} is too old")
    return allErrors

def compare_dates_divorce(birth_date, divorce_date):
    birth = datetime.strptime(birth_date, "%d %b %Y")
    divorce = datetime.strptime(divorce_date, "%d %b %Y")
    divorce_adjusted = divorce + relativedelta(months=9)
    if birth > divorce_adjusted:
        return 1
    return 0

def get_date(df, id, type):
    val = ((df[df['ID'] == id][type]).values)[0]
    if pd.isnull(val):
        return ""
    return str(val)

def check_birth_before_marriage(individuals, families):
    allErrors = []

    for _, row in families.iterrows():
        children = row['CHIL']
        marriage_date = get_date(families, row['ID'], 'MARR')
        divorce_date = get_date(families, row['ID'], 'DIV')
        for child in children:
            birth_date = ((individuals[individuals['ID'] == child]['BIRT']).values)[0]
            if compare_dates(marriage_date, birth_date) == 1:
                allErrors.append("ERROR: INDIVIDUAL: US08: " + child + " is born before the marriage of the parents")
            if divorce_date != "":
                if compare_dates_divorce(birth_date, divorce_date) == 1:
                    allErrors.append("ERROR: INDIVIDUAL: US08: " + child + " is born after the divorce of the parents")
    return allErrors