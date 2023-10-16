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
        brith_date = row['BIRT']
        birth_date = datetime.strptime(brith_date, "%d %b %Y")
        age = relativedelta(datetime.now(), birth_date).years
        if age > 150:
            allErrors.append(f"ERROR: INDIVIDUAL: US07: {row['ID']} is too old")
    return allErrors

def check_birth_before_marriage(individuals, families):
    allErrors = []

    def compare_dates_divorce(birth_date, divorce_date):
        birth = datetime.strptime(birth_date, "%d %b %Y")
        divorce = datetime.strptime(divorce_date, "%d %b %Y")
        divorce_adjusted = divorce + relativedelta(months=9)
        if birth > divorce_adjusted:
            return 1
        return 0
    
    def get_divorce_date(df, id):
        val = ((df[df['ID'] == id]['DIV']).values)[0]
        if pd.isnull(val):
            return ""
        return str(val)
    
    for _, row in families.iterrows():
        children = row['CHIL']
        marriage_date = row['MARR']
        divorce_date = get_divorce_date(families, row['ID'])
        for child in children:
            birth_date = ((individuals[individuals['ID'] == child]['BIRT']).values)[0]
            if compare_dates(marriage_date, birth_date) == 1:
                allErrors.append("ERROR: INDIVIDUAL: US08: " + child + " is born before the marriage of the parents")
            if divorce_date != "":
                if compare_dates_divorce(birth_date, divorce_date) == 1:
                    allErrors.append("ERROR: INDIVIDUAL: US08: " + child + " is born after the divorce of the parents")
    return allErrors