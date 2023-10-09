from gedcom.gedcom_parse import get_gedcom_df
import pandas as pd
from gedcom.Features.utils import get_age, compare_dates
from datetime import datetime
from dateutil.relativedelta import relativedelta

import os
 
# get current directory
cwd = os.getcwd()
individuals, families = get_gedcom_df(f'{cwd}/gedcom/example.ged')

#US07: Less than 150 years old
def check_less_than_150_years_old(individuals):
    allErrors = []
    for _, row in individuals.iterrows(): 
        age = get_age(row['BIRT'])
        if age > 150:
            allErrors.append(f"ERROR: INDIVIDUAL: US07: {row['ID']} is too old")
    return allErrors

#US08: Birth before marriage of parents
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



# US09: Birth before death of parents
def check_birth_before_death_of_parents(individuals, family):
    
    def get_death(df, id):
        val = ((df[df['ID'] == id]['DEAT']).values)[0]
        if pd.isnull(val):
            return ""
        return str(val)
    
    def compare_husb_to_child(husband_death, birth_date):
        # check if child was born before 9 months after father's death
        husband_death = datetime.strptime(husband_death, "%d %b %Y")
        birth_date = datetime.strptime(birth_date, "%d %b %Y")
        nine_months = husband_death + relativedelta(months=9)
        if birth_date > nine_months:
            return 1
        return 0
    
    
    allErrors = []
    for _, row in family.iterrows():
        if len(row['CHIL']) < 1:
            continue
        else:
            children = row['CHIL']
            husband_id = row['HUSB']
            wife_id = row['WIFE']
            husband_death = get_death(individuals, husband_id)
            wife_death = get_death(individuals, wife_id)
            for child in children:
                birth_date = ((individuals[individuals['ID'] == child]['BIRT']).values)[0]
                if wife_death != "" and compare_dates(birth_date, wife_death) == 1:
                    allErrors.append("ERROR: INDIVIDUAL: US09: " + child + " is born after the death of the mother")
                if husband_death != "" and compare_husb_to_child(husband_death, birth_date) == 1:
                    allErrors.append("ERROR: INDIVIDUAL: US09: " + child + " is born 9 months after the death of the father")
    
    return allErrors

# US10: Marriage after 14
def check_marriage_after_14(individuals, family):
        
        def get_age(marriage_date, birthday):
            # convert date strings into datetime objects
            try:
                d1 = datetime.strptime(marriage_date, "%d %b %Y")
                d2 = datetime.strptime(birthday, "%d %b %Y")
            except ValueError:
                # invalid formats
                raise Exception("Invalid date format")
        
            # Compare and return the age in years
            return ((d1 - d2).days) // 365
        
        allErrors = []
        for _, row in family.iterrows():
            husband_id = row['HUSB']
            wife_id = row['WIFE']
            marriage_date = row['MARR']
            husband_age = get_age(marriage_date, ((individuals[individuals['ID'] == husband_id]['BIRT']).values)[0])
            wife_age = get_age(marriage_date, ((individuals[individuals['ID'] == wife_id]['BIRT']).values)[0])
            if husband_age < 14:
                allErrors.append("ERROR: INDIVIDUAL: US10: " + husband_id + " was married before 14")
            if wife_age < 14:
                allErrors.append("ERROR: INDIVIDUAL: US10: " + wife_id + " was married before 14")
        
        return allErrors
                
    
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
    US07ERRORS = check_less_than_150_years_old(individuals)
    US08ERRORS = check_birth_before_marriage(individuals, families)
    US09ERRORS = check_birth_before_death_of_parents(individuals, families)
    US10ERRORS = check_marriage_after_14(individuals, families)
    US11ERRORS = check_bigamy(individuals, families)
    US12ERRORS = check_parents_too_old(individuals)

    # combine all 6 lists above
    allErrors = US07ERRORS + US08ERRORS + US09ERRORS + US10ERRORS + US11ERRORS + US12ERRORS
    with open(destination, 'a') as f:
        for error in allErrors:
            print(error, file=f)