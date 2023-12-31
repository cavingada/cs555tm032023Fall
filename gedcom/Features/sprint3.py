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
def check_fewer_than_15_siblings(families):
    allErrors = []
    for _, row in families.iterrows():
        children = row['CHIL']
        length = len(children)
        if length > 15:
            allErrors.append(f"ERROR: FAMILY: US15: {row['ID']} has more than 15 children")
    return allErrors

# US16: Male last names
def check_male_last_names(individuals, families):
    allErrors = []
    for _, row in families.iterrows():
        children = row['CHIL']
        length = len(children)
        last_name = row['HUSB NAME'].split('/')[1]
        for i in range(length):
            child = (individuals[individuals['ID'] == children[i]])
            if child['SEX'].values[0] != 'M':
                continue
            else:
                if child['NAME'].values[0].split('/')[1] != last_name:
                    allErrors.append(f"ERROR: FAMILY: US16: {row['ID']} has children with different last names")
    
    return allErrors

# US17: No marriages to descendants
def check_marriage_to_descendants(families):
    allErrors = []
    for _, row in families.iterrows():
        husband = row['HUSB']
        wife = row['WIFE']
        children = row['CHIL']
        for child in children:
            if child == husband or child == wife:
                allErrors.append(f"ERROR: FAMILY: US17: {row['ID']} has a marriage to a descendant")
    return allErrors

# US18: siblings should not marry
def check_siblings_marry(families):
    allErrors = []
    # get a dictionary of all husband and wives
    husband_wife = {}
    for _, row in families.iterrows():
        husband_wife[row['HUSB']] = row['WIFE']
    
    # check if each husband and wife (key, value) in the dictionary are both present in each CHIL column in families
    for key, value in husband_wife.items():
        for _, row in families.iterrows():
            if key in row['CHIL'] and value in row['CHIL']:
                allErrors.append(f"ERROR: FAMILY: US18: {key} and {value} are siblings and should not marry")
    return allErrors

def printAllSprint3Errors(individuals, families, destination):
    US13ERRORS = check_siblings_spacing(individuals, families)
    US14ERRORS = check_multiple_births(individuals, families)
    US15ERRORS = check_fewer_than_15_siblings(families)
    US16ERRORS = check_male_last_names(individuals, families)
    US17ERRORS = check_marriage_to_descendants(families)
    US18ERRORS = check_siblings_marry(families)

    # combine all 6 lists above
    allErrors = US13ERRORS + US14ERRORS + US15ERRORS + US16ERRORS + US17ERRORS + US18ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)