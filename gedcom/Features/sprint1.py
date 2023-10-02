from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from utils import compare_dates

individuals, families = get_gedcom_df('example.ged')


# US01: Dates before current date

# US02: Birth before marriage


# US03: Birth before death

# US04: Marriage before divorce

# US05: Marriage before death
def check_marriage_before_death(individuals, family):
    
    def get_death(df, spouse):
        return df[df['ID'] == df[spouse]]['DEAT'].values[0]
    
    def getErrors(row, key):
        spouse = "husband" if key=="HUSB" else "wife"
        if compare_dates(husband_death, row['MARR']) == 1:
            errMsg = (f"ERROR: FAMILY: US05: {row['ID']} Married {row['MARR']} after {spouse}'s ( {row[key]} death on {get_death(individuals, key)}")
        return errMsg
    
    allErrors=[]
    
    for _, row in family.iterrows():
        if row['MARR'] != pd.NA:
            husband_death = get_death(individuals, 'HUSB')
            wife_death = get_death(individuals, 'WIFE')
            if husband_death != pd.NA:
                allErrors.append(getErrors(row, key = 'HUSB'))
            if wife_death != pd.NA:
                allErrors.append(getErrors(row, key = 'WIFE'))
    return allErrors

# write 5 unit test cases for US05
print(check_marriage_before_death(individuals, families))

# 1. husband dead before marriage


# US06: Divorce before death

# step 1: loop through each person's id
# step 2: get their col1 (e.g. birth)
# step 3: go to df 2 and look at person's col2 (e.g. marriage) using id from df1
# step 4: compare the two dates. 
