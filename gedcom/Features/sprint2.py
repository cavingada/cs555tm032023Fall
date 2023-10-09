from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import get_age, compare_dates
from datetime import datetime


import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')


# US11: No Bigamy
def check_bigamy(individuals, family):
    
    def get_death(df, id):
        val = ((df[df['ID'] == id]['DEAT']).values)[0]
        if pd.isnull(val):
            return ""
        return str(val)
    
    def get_marriage_date_by_partner(df, id, partner_type):
        marriage_date = ((df[df[partner_type] == id]['MARR']).values)[0]
        if pd.isnull(marriage_date):
            return ""
        return str(marriage_date)
    
    def get_divorce_date_by_partner(df, id, partner_type):
        divorce_date = ((df[df[partner_type] == id]['DIV']).values)[0]
        if pd.isnull(divorce_date):
            return ""
        return str(divorce_date)
    
    def has_single_overlap(intervals):
        # convert to date time and sort intervals by start
        time_intervals = [(datetime.strptime(start, "%d %b %Y"), datetime.strptime(end, "%d %b %Y")) for start, end in intervals]
        sorted_intervals = sorted(time_intervals, key=lambda x: x[0])
        
        # curr interval is the first interval
        current_interval = sorted_intervals[0]
        
        # loop through each interval
        for interval in sorted_intervals[1:]:
            if interval[0] <= current_interval[1]:
                # if theres an overlap return true
                return True
            else:
                # if not, assign next interval
                current_interval = interval
        
        # no overlaps found
        return False

    allErrors =[]
    for _, row in individuals.iterrows():
        sex = row['SEX']
        partner = row['FAMS']

        if len(partner) < 2:
            continue

        listOfStartAndEnds = []
        for partner in partner:

            if sex == "M":
                typeOfPartner = "WIFE"
            else:
                typeOfPartner = "HUSB"
            partner_id = (family[family['ID'] == partner][typeOfPartner]).values[0]

            spouse_death = get_death(individuals, partner_id)
            marriage_date = get_marriage_date_by_partner(family, partner_id, typeOfPartner)
            divorce_date = get_divorce_date_by_partner(family, partner_id, typeOfPartner)

            start = marriage_date
            end = ""
            # end date is today 
            if divorce_date == "" and spouse_death == "":
                end = datetime.now().strftime("%d %b %Y")
            elif divorce_date == "":
                end = spouse_death
            elif spouse_death == "":
                end = divorce_date
            listOfStartAndEnds.append((start, end))

        if has_single_overlap(listOfStartAndEnds):
            allErrors.append("ERROR: INDIVIDUAL: US11: " + row['ID'] + " is a bigamist")
            
    return allErrors

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
                error = f"ERROR: INDIVIDUAL: US12: {row['ID']} is a parent and is too old"
                allErrors.append(error)

    return allErrors

def printAllSprint2Errors(individuals, families, destination):
    """US07ERRORS = check_dates_before_current(individuals, families)
    US08ERRORS = check_birth_before_marriage(individuals, families)
    US09ERRORS = check_birth_before_death(individuals)
    US10ERRORS = check_marriage_before_divorce(families)
    US11ERRORS = check_marriage_before_death(individuals, families)"""
    US11ERRORS = check_bigamy(individuals, families)
    US12ERRORS = check_parents_too_old(individuals)

    # combine all 6 lists above
    allErrors = US11ERRORS + US12ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)