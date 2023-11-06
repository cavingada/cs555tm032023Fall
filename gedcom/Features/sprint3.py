from gedcom.gedcom_parse import get_gedcom_df, print_pretty_table
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
def check_siblings_spacing(individuals, families):
    
    def compare_dates_siblings(sibling1, sibling2):
        s1 = datetime.strptime(sibling1, "%d %b %Y")
        s2 = datetime.strptime(sibling2, "%d %b %Y")
        if s1 + relativedelta(months=8) > s2:
            if s1 + relativedelta(days=2) <= s2:
                return 1
            return 0
        return 0
    
    allErrors = []

    for _, row in families.iterrows():
        children = row['CHIL']
        length = len(children)
        for i in range(length):
            s1 = ((individuals[individuals['ID'] == children[i]]['BIRT']).values)[0]
            for j in range(length):
                if i != j:
                    s2 = ((individuals[individuals['ID'] == children[j]]['BIRT']).values)[0]
                    if compare_dates_siblings(s1, s2) == 1:
                        allErrors.append(f"ERROR: FAMILY: US13: {children[i]} and {children[j]} are born less than 8 months of each other and are not twins")
    return allErrors

#US14: Multiple births <=5
def check_multiple_births(individuals, families):
    allErrors = []
    for _, row in families.iterrows():
        children = row['CHIL']
        length = len(children)
        if length > 5:
            birth_dates = {}
            for i in range(length):
                s1 = datetime.strptime(((individuals[individuals['ID'] == children[i]]['BIRT']).values)[0], "%d %b %Y")
                if s1 in birth_dates.keys():
                    birth_dates[s1] += 1
                else:
                    birth_dates[s1] = 1
            for key in birth_dates:
                if birth_dates[key] > 5:
                    allErrors.append(f"ERROR: FAMILY: US14: {row['ID']} has more than 5 children born on {key}")
    return allErrors

# US15: Fewer than 15 siblings


# US16: Male last names

# US17: No marriages to descendants


# US18: Sibligns should not marry


def printAllSprint3Errors(individuals, families, destination):
    US13ERRORS = check_siblings_spacing(individuals, families)
    US14ERRORS = check_multiple_births(individuals, families)
    US15ERRORS = []
    US16ERRORS = []
    US17ERRORS = []
    US18ERRORS = []

    # combine all 6 lists above
    allErrors = US13ERRORS + US14ERRORS + US15ERRORS + US16ERRORS + US17ERRORS + US18ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)