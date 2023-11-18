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

#US19: First Cousins should not marry
def get_parents(individuals, id):
        if id == "":
            return ""
        val = ((individuals[individuals['ID'] == id]['FAMC']).values)[0]
        if len(val) == 0:
            return ""
        return val
    
def get_spouse(families, id, type):
    if id == "":
        return ""
    val = ((families[families['ID'] == id][type]).values)[0]
    if pd.isnull(val):
        print(id, "NULL")
        return ""
    return str(val)

def check_if_siblings(individuals, id1, id2):
    if id1 == "" or id2 == "" or id1 == id2:
        return 0
    val1 = get_parents(individuals, id1)
    val2 = get_parents(individuals, id2)
    if val1 == val2 and val1 != "":
        return 1
    return 0

def check_first_cousins_marry(individuals, families):
    allErrors = []
    
    for _, row in families.iterrows():
        if not pd.isnull(row['HUSB']) and not pd.isnull(row['WIFE']):
            husband = row['HUSB']
            wife = row['WIFE']

            husband_parents = get_parents(individuals, husband)
            wife_parents = get_parents(individuals, wife)
           

            if husband_parents != "" and wife_parents != "":
                husband_father = get_spouse(families, husband_parents[0], 'HUSB')
                husband_mother = get_spouse(families, husband_parents[0], 'WIFE')
                wife_father = get_spouse(families, wife_parents[0], 'HUSB')
                wife_mother = get_spouse(families, wife_parents[0], 'WIFE')


                if check_if_siblings(individuals, husband_father, wife_father) == 1:
                    allErrors.append(f"ERROR: FAMILY: US19: {husband} and {wife} are first cousins and should not marry")
                if check_if_siblings(individuals, husband_mother, wife_mother) == 1:
                    allErrors.append(f"ERROR: FAMILY: US19: {husband} and {wife} are first cousins and should not marry")
                if check_if_siblings(individuals, husband_father, wife_mother) == 1:
                    allErrors.append(f"ERROR: FAMILY: US19: {husband} and {wife} are first cousins and should not marry")
                if check_if_siblings(individuals, husband_mother, wife_father) == 1:
                    allErrors.append(f"ERROR: FAMILY: US19: {husband} and {wife} are first cousins and should not marry")
    
    return allErrors

#US20: Aunts and uncles should not marry their nieces or nephews
def check_aunts_uncles_marry(individuals, families):
    allErrors = []
    for _, row in families.iterrows():
        if not pd.isnull(row['HUSB']) and not pd.isnull(row['WIFE']):
            husband = row['HUSB']
            wife = row['WIFE']

            husband_parents = get_parents(individuals, husband)
            wife_parents = get_parents(individuals, wife)

            if husband_parents != "" and wife_parents != "":
                husband_father = get_spouse(families, husband_parents[0], 'HUSB')
                husband_mother = get_spouse(families, husband_parents[0], 'WIFE')
                wife_father = get_spouse(families, wife_parents[0], 'HUSB')
                wife_mother = get_spouse(families, wife_parents[0], 'WIFE')

                if check_if_siblings(individuals, husband_father, wife) == 1:
                    allErrors.append(f"ERROR: FAMILY: US20: {husband} and {wife} are aunt/uncle and nephew/niece and should not marry")
                if check_if_siblings(individuals, husband_mother, wife) == 1:
                    allErrors.append(f"ERROR: FAMILY: US20: {husband} and {wife} are aunt/uncle and nephew/niece and should not marry")
                if check_if_siblings(individuals, husband, wife_father) == 1:
                    allErrors.append(f"ERROR: FAMILY: US20: {husband} and {wife} are aunt/uncle and nephew/niece and should not marry")
                if check_if_siblings(individuals, husband, wife_mother) == 1:
                    allErrors.append(f"ERROR: FAMILY: US20: {husband} and {wife} are aunt/uncle and nephew/niece and should not marry")
    return allErrors

#US21: Correct gender for role

#US22: Unique IDs

#US23: Unique name and birth date

#US24: Unique families by spouses


def printAllSprint4Errors(individuals, families, destination):
    US19ERRORS = check_first_cousins_marry(individuals, families)
    US20ERRORS = check_aunts_uncles_marry(individuals, families)
    # US21ERRORS = check_fewer_than_15_siblings(families)
    # US22ERRORS = check_male_last_names(individuals, families)
    # US23ERRORS = check_marriage_to_descendants(families)
    # US24ERRORS = check_siblings_marry(families)

    # combine all 6 lists above
    allErrors = US19ERRORS + US20ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)


# print_pretty_table(individuals, 'Individuals','sprint4_output.txt')
# print_pretty_table(families, 'Families', 'sprint4_output.txt')
# printAllSprint4Errors(individuals, families, 'sprint4_output.txt')