from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import compare_dates


import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')


# US01: Dates before current date

# US02: Birth before marriage


# US03: Birth before death

# US04: Marriage before divorce

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

print(check_marriage_before_death(individuals, families))
print(check_divorce_before_death(individuals, families))