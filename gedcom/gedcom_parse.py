import pandas as pd
from prettytable import PrettyTable
key_words = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

def get_gedcom_df(filename):
    with open(filename, 'r') as file:
        # print the unique identifiers and names of each of the individuals 
        # in order by their unique identifiers. 
        individuals = pd.DataFrame(columns=['ID', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS'])
        families = pd.DataFrame(columns=['ID', 'MARR', 'DIV', 'HUSB', 'HUSB NAME', 'WIFE', 'WIFE NAME', 'CHIL'])

        curr_id = ''
        isIndividual = False
        isBirth = True
        isMarried = True
        for line in file:
            line_words = line.split()
            if not line_words:
                continue
            # get the first element since at is the tag of line
            level = line_words[0].strip()
            try:
                if line_words[2].strip() == "INDI" or line_words[2].strip() == "FAM":
                    if line_words[2] == "INDI":
                        isIndividual = True
                    else:
                        isIndividual = False
                    line_tag = line_words[2].strip()
                    arguments = line_words[1].strip()
            
                else:
                    line_tag = line_words[1].strip()
                    arguments = line.split(line_tag)[-1].strip() 
            except:
                line_tag = line_words[1].strip()
                arguments = line.split(line_tag)[-1].strip()
            
            # check if that is present in the keywords
            if line_tag in key_words:
                if line_tag == "NOTE" or line_tag == "TRLR":
                    continue
                if (isIndividual):
                    if level == "0": # new block, individual or fam
                        curr_id = arguments
                        new_row = pd.DataFrame([{'ID': curr_id, 'NAME':pd.NA, 'SEX':pd.NA, 'BIRT':pd.NA, 'DEAT':pd.NA, 'FAMC':[], 'FAMS':[]}])
                        individuals = pd.concat([individuals, new_row], ignore_index=True)
                    if level == "1" and (line_tag != 'BIRT' or line_tag!= 'DEAT' or line_tag!="INDI"):
                        index_to_modify = individuals[individuals['ID'] == curr_id].index[0]
                        if line_tag == "FAMC" or line_tag == "FAMS":
                            individuals.loc[index_to_modify, line_tag].append(arguments)
                        else:
                            individuals.loc[index_to_modify, line_tag] = arguments
                    if level == "2":
                        index_to_modify = individuals[individuals['ID'] == curr_id].index[0]
                        if isBirth:
                            individuals.loc[index_to_modify, 'BIRT'] = arguments
                        else:
                            individuals.loc[index_to_modify, 'DEAT'] = arguments
                    else:
                        if line_tag == "BIRT":
                            isBirth = True
                        elif line_tag == "DEAT":
                            isBirth = False
                else:
                    if level == "0":
                        curr_id = arguments
                        new_row = pd.DataFrame([{'ID': curr_id, 'MARR':pd.NA, 'DIV':pd.NA, 'HUSB':pd.NA, 'WIFE':pd.NA, 'CHIL':[] }])
                        families = pd.concat([families, new_row], ignore_index=True)
                    if level == "1":
                        index_to_modify = families[families['ID'] == curr_id].index[0]
                        if line_tag == "CHIL":
                            families.loc[index_to_modify, line_tag].append(arguments)
                        else:
                            if line_tag == "MARR":
                                isMarried = True
                            elif line_tag == "DIV":
                                isMarried = False
                            else:
                                if line_tag == "HUSB":
                                    families.loc[index_to_modify, 'HUSB NAME'] = individuals[individuals['ID'] == arguments]['NAME'].values[0]
                                if line_tag == "WIFE":
                                    families.loc[index_to_modify, 'WIFE NAME'] = individuals[individuals['ID'] == arguments]['NAME'].values[0]
                                families.loc[index_to_modify, line_tag] = arguments
                    if level == "2":
                        index_to_modify = families[families['ID'] == curr_id].index[0]
                        if isMarried:
                            families.loc[index_to_modify, 'MARR'] = arguments
                        else:
                            families.loc[index_to_modify, 'DIV'] = arguments
            else:
                valid = 'N'

        return individuals, families

def print_pretty_table(df, title):
    table = PrettyTable()
    table.field_names = df.columns.to_list()
    for index, row in df.iterrows():
        table.add_row(row.to_list())
    with open('output.txt', 'a') as f:
        print(title, file=f)
        print(table, file=f)
    return table