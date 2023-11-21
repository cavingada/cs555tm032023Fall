from gedcom.gedcom_parse import get_gedcom_df, print_pretty_table
from gedcom.Features.sprint1 import *
from gedcom.Features.sprint2 import *
from gedcom.Features.sprint3 import *
from gedcom.Features.sprint4 import *

gedcom_file = f'{cwd}/gedcom/example.ged'
individuals, families = get_gedcom_df(gedcom_file)

print_pretty_table(individuals, 'Individuals','sprint1_output.txt')
print_pretty_table(families, 'Families', 'sprint1_output.txt')
printAllSprint1Errors(individuals, families, 'sprint1_output.txt')


print_pretty_table(individuals, 'Individuals','sprint2_output.txt')
print_pretty_table(families, 'Families', 'sprint2_output.txt')
printAllSprint2Errors(individuals, families, 'sprint2_output.txt')

print_pretty_table(individuals, 'Individuals','sprint3_output.txt')
print_pretty_table(families, 'Families', 'sprint3_output.txt')
printAllSprint3Errors(individuals, families, 'sprint3_output.txt')

print_pretty_table(individuals, 'Individuals','sprint4_output.txt')
print_pretty_table(families, 'Families', 'sprint4_output.txt')
printAllSprint4Errors(individuals, families, 'sprint4_output.txt')