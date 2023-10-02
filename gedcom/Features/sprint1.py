from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import compare_dates
import datetime


import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')


# US01: Dates before current date
def check_dates_before_current(individuals, families):
    current_datetime = datetime.date.today()
    allErrors = []

    for _, row in individuals.iterrows():
        if not pd.isna(row['BIRT']) and row['BIRT'] != 'NA':
            if compare_dates(row['BIRT'], current_datetime.strftime("%d %b %Y")) == 1:
                allErrors.append(f"ERROR: INDIVIDUAL: US01: {row['ID']}: Birthday {row['BIRT']} occurs in the future")
        if not pd.isna(row['DEAT']) and row['DEAT'] != 'NA':
            if compare_dates(row['DEAT'], current_datetime.strftime("%d %b %Y")) == 1:
                allErrors.append(f"ERROR: INDIVIDUAL: US01: {row['ID']}: Death {row['DEAT']} occurs in the future")

    for _, row in families.iterrows():
        if not pd.isna(row['MARR']) and row['MARR'] != 'NA':
            if compare_dates(row['MARR'], current_datetime.strftime("%d %b %Y")) == 1:
                allErrors.append(f"ERROR: FAMILY: US01: {row['ID']}: Marriage {row['MARR']} occurs in the future")

        if not pd.isna(row['DIV']) and row['DIV'] != 'NA':
            if compare_dates(row['DIV'], current_datetime.strftime("%d %b %Y")) == 1:
                allErrors.append(f"ERROR: FAMILY: US01: {row['ID']}: Divorce {row['DIV']} occurs in the future")

    return allErrors

# US02: Birth before marriage
def check_birth_before_marriage(individuals, families):
    allErrors = []

    for _, row in families.iterrows():
        if not pd.isna(row['MARR']) and row['MARR'] != 'NA':
            husband_birth = (individuals[individuals['ID'] == row['HUSB']]['BIRT']).values
            wife_birth = (individuals[individuals['ID'] == row['WIFE']]['BIRT']).values
            if len(husband_birth) > 0 and len(wife_birth) > 0:
                husband_birth = str(husband_birth[0])
                wife_birth = str(wife_birth[0])
                if compare_dates(husband_birth, row['MARR']) == 1:
                    allErrors.append(f"ERROR: FAMILY: US02: {row['ID']}: Husband's ({row['HUSB']}) marriage date {row['MARR']} occurs before his birth date {husband_birth}")
                if compare_dates(wife_birth, row['MARR']) == 1:
                    allErrors.append(f"ERROR: FAMILY: US02: {row['ID']}: Wife's ({row['WIFE']}) marriage date {row['MARR']} occurs before her birth date {wife_birth}")

    return allErrors

# US03: Birth before death
def check_birth_before_death(individuals):
    def getErrors(row):
        errMsg = ""
        if compare_dates(row['BIRT'], row['DEAT']) == 1:
            errMsg = (f"ERROR: INDIVIDUAL: US03: {row['ID']}: Died on {row['DEAT']} before born on {row['BIRT']}")
        return errMsg
    
    allErrors = []
    for _, row in individuals.iterrows():
        if not pd.isna(row['BIRT']) and not pd.isna(row['DEAT']):
            errors = getErrors(row)
            if errors: allErrors.append(errors)
    
    return allErrors

# US04: Marriage before divorce
def check_marriage_before_divorce(family):
    def getErrors(row):
        errMsg = ""
        if compare_dates(row['MARR'], row['DIV']) == 1:
            errMsg = (f"ERROR: FAMILY: US04: {row['ID']}: Divorced on {row['DIV']} before married on {row['MARR']}")
        return errMsg
    
    allErrors = []
    for _, row in family.iterrows():
        if not pd.isna(row['MARR']) and not pd.isna(row['DIV']):
            errors = getErrors(row)
            if errors: allErrors.append(errors)
    
    return allErrors
# US05: Marriage before death

def check_marriage_before_death(individuals, family):
    
    def get_death(df, id):
        val = (df[df['ID'] == id]['DEAT']).values
        if len(val) == 0:
            return ""
        return str(val[0])
    
    def getErrors(row, key, death):
        spouse = "husband" if key=="HUSB" else "wife"
        errMsg = ""

        if compare_dates(death, row['MARR']) == -1:
            errMsg = (f"ERROR: FAMILY: US05: {row['ID']}: Married on {row['MARR']} after {spouse}'s ({row[key]}) death on {death}")
        
        return errMsg
    
    allErrors=[]
    
    for _, row in family.iterrows():
        if not pd.isna(row['MARR']) and row['MARR'] != 'NA':
            husband_death = get_death(individuals, row['HUSB'])
            wife_death = get_death(individuals, row['WIFE'])
            if len(husband_death)>0 and husband_death != '<NA>':
                husband_errors = getErrors(row, key = 'HUSB', death = husband_death)
                if husband_errors: allErrors.append(husband_errors)
            if len(wife_death) and wife_death != '<NA>':
                wife_errors = getErrors(row, key = 'WIFE', death=wife_death)
                if wife_errors: allErrors.append(wife_errors)

    return allErrors

# US06: Divorce before death
def check_divorce_before_death(individuals, family):
    
    def get_death(df, id):
        val = (df[df['ID'] == id]['DEAT']).values
        if len(val) == 0:
            return ""
        return str(val[0])
    
    def getErrors(row, key, death):
        spouse = "husband" if key=="HUSB" else "wife"
        errMsg = ""

        if compare_dates(death, row['DIV']) == -1:
            errMsg = (f"ERROR: FAMILY: US05: {row['ID']}: Divorced on {row['DIV']} after {spouse}'s ({row[key]}) death on {death}")
        
        return errMsg
    
    allErrors=[]
    
    for _, row in family.iterrows():
        if not pd.isna(row['DIV']) and row['DIV'] != 'NA':
            husband_death = get_death(individuals, row['HUSB'])
            wife_death = get_death(individuals, row['WIFE'])
            if len(husband_death)>0 and husband_death != '<NA>':
                husband_errors = getErrors(row, key = 'HUSB', death = husband_death)
                if husband_errors: allErrors.append(husband_errors)
            if len(wife_death) and wife_death != '<NA>':
                wife_errors = getErrors(row, key = 'WIFE', death=wife_death)
                if wife_errors: allErrors.append(wife_errors)

    return allErrors
