# ===== Python - UTF-8 ===== #
"""/*
School: Stevens Institute of Technology
---------------------------------------
Course: SSW 555 - WS
Instructor: Prof. Richard Ens
------------------------------------------------
Project: # 08 / User Stories: 020, 027, 029, 031
------------------------------------------------
Coder with CWID: Yujun Kong / 1046 6820
Team with members # 04: Kristin Allocco / Shengping Xu / Yujun Kong
*/"""
# ===== CODING BEGINS ===== #

# * import the supporting types, libraries, modules
from multiprocessing.dummy.connection import families
import sys
from typing import Any, List, Set, Dict, Optional, IO, Tuple, Iterable
from prettytable import PrettyTable
from datetime import datetime

""" # Global Objects Begin # """
# {format} for to print blank line:
def BL():
    print ()

# {format} for to print a separating line:
def SL():
    print ('-' * 150)

# {format} for to print if some codes are okay:
def OK():
    print ('Okay')
# {/}
""" # /Global Objects End # """

""" # Supporting Classes Begin # """
# <class> define supporting class"ezIO" for to reuse codes:
class ezIO:

    # ([constructor]) define a constructor for class itself:
    def __init__(self):
        pass #! Temporarily, there're no needs.
    
    # ((method)) define a method for to print out the welcoming words:
    def welcome(self):

        welcoming = "-== Welcome to ' User Stories: 020, 027, 029, 031 ' ==-"
        BL()
        print(welcoming)
        print ( '-' * len(welcoming) )
        BL()
    # ((/))

    # ((method)) define a method for to quit the main program:
    def quit_Main(self):

        BL()
        print("--- Thanks for your operating, Bye! ---")
        BL()
        sys.exit()
    # ((/))

    # ((method))
    def open_file(self, file_name: str) -> IO:

        while True:
            try:
                gotten_File: IO = open(file_name, 'r', encoding = 'gbk', errors = 'ignore')
                return gotten_File
            except FileNotFoundError:
                print("The file name is invalid or the file does not exist.")
                BL()
                continue
    # ((/))
# </>
""" # /Supporting Classes End # """


""" # CORE DEFINING BEGINS HERE # """
# --------------------------------- #

""" # 01 Unit """
# <class>
class File_Analyzer:
    """ Analyze and summarize the GEDCOM file and then output as the needed format. """

    # ((method)) Constructor
    def __init__(self, open_file_command: IO) -> Optional[List]:
     
        self.open_file_command = open_file_command
        self.aunts_and_uncles_lables: List = ['ID', 'Name', 'Role']
        self.age_labels: List = ['ID', 'Name', 'Gender', 'Age', 'Birthday', 'Alive', 'Death']
        self.deceased_labels: List = ['ID', 'Name', 'Gender', 'Death']
        self.living_labels: List = ['ID', 'Name', 'Gender', 'Birthday']

        self.lines = self.get_gedcom_file_lines()
        self.individuals_and_families = self.get_individuals_and_families()

        self.aunts_and_uncles = self.list_aunts_and_uncles()
        self.individuals_with_age = self.list_ages_of_individuals()
        self.deceased_individuals = self.list_deceased_individuals()
        self.living_individuals = self.list_living_individuals()

        self.pretty_print()        
    # ((/))

    # ((method)) 0.5
    def get_gedcom_file_lines(self) -> Optional[List]:

        with self.open_file_command:

            wrap_free_lines: List = []
            line: str
            for line in self.open_file_command.readlines():
                line = line.strip('\n')
                wrap_free_lines.append(line)

        return wrap_free_lines
    # ((/))

    # ((method)) 01
    def get_individuals_and_families(self) -> Optional[List]:

        individuals_head_index: int
        individuals_tail_index: int
        families_head_index: int
        families_tail_index: int
        cur_index: int = 0
        for line in self.lines:
            cur_index += 1
            if line == '0 @I1@ INDI':
                individuals_head_index = cur_index
            elif line == '0 @F1@ FAM':
                individuals_tail_index = cur_index
                families_head_index = cur_index
            elif line == '0 TRLR':
                families_tail_index = cur_index
        
        individuals_block: List = self.lines[individuals_head_index - 1 : individuals_tail_index - 1]
        individuals_block = individuals_block + ['0 End of INDI 0']
        families_block: List = self.lines[families_head_index - 1 : families_tail_index -1]
        families_block = families_block + ['0 End of FAM 0']
        
        unit_cur_index: int = 0
        unit_head_index: int = 0
        each_individual_combination: List = []
        each_individual: List = []
        for unit in individuals_block[unit_head_index : ]:                
            unit_cur_index += 1
            if ('0' and 'INDI' in unit) and (unit != individuals_block[unit_head_index]):
                each_individual = individuals_block[unit_head_index : unit_cur_index - 1]                    
                unit_head_index = unit_cur_index - 1                
                each_individual_combination.append(each_individual)

        elem_cur_index: int = 0
        elem_head_index: int = 0
        each_family_combination: List = []
        each_family: List = []
        for elem in families_block[elem_head_index : ]:
            elem_cur_index += 1
            if ('0' and 'FAM' in elem) and (elem != families_block[elem_head_index]):
                each_family = families_block[elem_head_index : elem_cur_index - 1]
                elem_head_index = elem_cur_index - 1
                each_family_combination.append(each_family)

        individuals_and_families: List = []
        individuals_and_families.append(each_individual_combination)
        individuals_and_families.append(each_family_combination)

        #print(individuals_and_families[0])
        return individuals_and_families
    # ((/))

    # ((method)) 02 <- User Story #20
    def list_aunts_and_uncles(self) -> Optional[List]:

        elem: str
        item: str
        unit: str
        each: str
        node: str
        cur_family: List = []
        grand_family: List = []
        all_children: List = []
        cur_parents: List = []
        selected_parents: List = []
        blood_aunts_and_uncles: set = ()
        pair_aunts_and_uncles: List = []
        splitted_aunts_and_uncles: List = []
        aunts_and_uncles: List = []

        for family in self.individuals_and_families[1]: 
            for elem in family:
                cur_elem = [i for i in elem.split(' ')]
                if 'F1' == cur_elem[1].strip('@'):
                    if 'HUSB' in family[1]:
                        cur_family.append(str([i for i in family[1].split(' ')][2]).strip('@'))
                    if 'WIFE' in family[2]:
                        cur_family.append(str([i for i in family[2].split(' ')][2]).strip('@'))
                elif 'F1' != str([i for i in family[0].split(' ')][1]).strip('@'):
                    if 'HUSB' in cur_elem:
                        cur_parents = [cur_elem[2].strip('@')]
                    if 'WIFE' in cur_elem:
                        cur_parents.append(cur_elem[2].strip('@'))         
            selected_parents.append(cur_parents)            
        selected_parents = selected_parents[1:]
                
        for individual in self.individuals_and_families[0]:
            for item in individual:
                cur_item = [i for i in item.split(' ')]
                if str([i for i in individual[0].split(' ')][1]).strip('@') in cur_family:
                    if cur_item[1] == 'FAMC':
                        grand_family.append(cur_item[2].strip('@'))

        for family in self.individuals_and_families[1]:
            for unit in family:
                cur_unit = [i for i in unit.split(' ')]
                if str([i for i in family[0].split(' ')][1]).strip('@') in grand_family:
                    if 'CHIL' in cur_unit:
                        all_children.append(cur_unit[2].strip('@'))

        blood_aunts_and_uncles = set(all_children).difference(cur_family)

        for each in selected_parents:
            for i in each:
                if i in blood_aunts_and_uncles:
                    pair_aunts_and_uncles.append(each)
        
        splitted_aunts_and_uncles = [j for k in pair_aunts_and_uncles for j in k]

        for individual in self.individuals_and_families[0]:
            formatted_row: Dict = dict.fromkeys(self.aunts_and_uncles_lables)
            for node in individual:
                cur_node = [i for i in node.split(' ')]
                if 'INDI' in cur_node:
                    formatted_row['ID'] = cur_node[1].strip('@')
                if 'NAME' in cur_node:
                    formatted_row['Name'] = cur_node[2] + ' ' + cur_node[3].strip('/')
                if 'SEX' in cur_node:
                    if 'M' in cur_node:
                        formatted_row['Role'] = 'Uncle'
                    elif 'F' in cur_node:
                        formatted_row['Role'] = 'Aunt'

            if formatted_row['ID'] not in splitted_aunts_and_uncles:
                continue
            aunts_and_uncles.append(formatted_row)
        return aunts_and_uncles
    # ((/))

    # ((method)) 03 <- User Story #27
    def list_ages_of_individuals(self) -> Optional[List]:

        now: datetime = datetime.today()
        people_with_age: List = []
        item: str
        for individual in self.individuals_and_families[0]:
            formatted_row: Dict = dict.fromkeys(self.age_labels)

            for item in individual:
                cur_item = [i for i in item.split(' ')]

                if 'INDI' in cur_item:
                    formatted_row['ID'] = cur_item[1].strip('@')
                if 'NAME' in cur_item:
                    formatted_row['Name'] = cur_item[2] + ' ' + cur_item[3].strip('/')
                if 'SEX' in cur_item:
                    if 'M' in cur_item:
                        formatted_row['Gender'] = 'M'
                    elif 'F' in cur_item:
                        formatted_row['Gender'] = 'F'
                
                if 'BIRT' not in individual[6]:
                    formatted_row['Birthday'] = 'Unknown'
                elif 'BIRT' in individual[6]:
                    if len(individual[7][7:]) == 4:
                        formatted_row['Birthday'] = str(individual[7][7:])
                    elif len(individual[7][7:]) > 4:
                        b_date: datetime = datetime.strptime(individual[7][7:], '%d %b %Y')
                        formatted_row['Birthday'] = str(b_date.date())
                
                if ('DEAT' in individual[6]) and ('DATE' not in individual[7]):
                    formatted_row['Death'] = 'Unknown'
                    formatted_row['Alive'] = 'False'
                elif ('DEAT' in individual[8]) and ('DATE' in individual[9]):
                    d_date: datetime = datetime.strptime(individual[9][7:], '%d %b %Y')
                    formatted_row['Death'] = str(d_date.date())
                    formatted_row['Alive'] = 'False'
                elif 'DEAT' not in individual[8]:
                    formatted_row['Death'] = 'NA'
                    formatted_row['Alive'] = 'True'
                
                if ('DEAT' in individual[6]) and ('DATE' not in individual[7]):
                    formatted_row['Age'] = 'Unknown'
                elif ('DEAT' in individual[8]) and ('DATE' in individual[9]):
                    d_date: datetime = datetime.strptime(individual[9][7:], '%d %b %Y')
                    formatted_row['Age'] = str(d_date.year - b_date.year)
                elif 'DEAT' not in individual[8]:
                    if len(individual[7][7:]) == 4:
                        formatted_row['Age'] = str(int(now.year) - int(individual[7][7:]))
                    elif len(individual[7][7:]) > 4:
                        b_date: datetime = datetime.strptime(individual[7][7:], '%d %b %Y')
                        formatted_row['Age'] = str(now.year - b_date.year)

            people_with_age.append(formatted_row)

        return people_with_age
    # ((/))

    # ((method)) 04 <- User Story #29
    def list_deceased_individuals(self) -> Optional[List]:

        deceased_people: List = []
        item: str
        for individual in self.individuals_and_families[0]:
            formatted_row: Dict = dict.fromkeys(self.deceased_labels)

            for item in individual:
                cur_item = [i for i in item.split(' ')]

                if 'DEAT' in cur_item:
                    formatted_row['ID'] = [text for text in str(individual[0]).split(' ')][1].strip('@')
                    formatted_row['Name'] = [text for text in str(individual[1]).split(' ')][2] + ' ' + [text for text in str(individual[1]).split(' ')][3].strip('/')
                    formatted_row['Gender'] = [text for text in str(individual[5]).split(' ')][2]
                if len(cur_item) == 5:
                    d_date: datetime = datetime.strptime(cur_item[2] + ' ' + cur_item[3] + ' ' + cur_item[4], '%d %b %Y')
                    formatted_row['Death'] = d_date.date()
                elif formatted_row['Death'] == None:
                    formatted_row['Death'] = 'Unknown'
                
            if formatted_row['ID'] == None:
                continue
            deceased_people.append(formatted_row)
        return deceased_people
    # ((/))

    # ((method)) 05 <- User Story #31
    def list_living_individuals(self) -> Optional[bool]:

        living_people: List = []
        item: str
        for individual in self.individuals_and_families[0]:
            formatted_row: Dict = dict.fromkeys(self.living_labels)

            dead_people: List = []
            for item in individual:
                cur_item = [i for i in item.split(' ')]

                formatted_row['ID'] = [text for text in str(individual[0]).split(' ')][1].strip('@')
                formatted_row['Name'] = [text for text in str(individual[1]).split(' ')][2] + ' ' + [text for text in str(individual[1]).split(' ')][3].strip('/')
                formatted_row['Gender'] = [text for text in str(individual[5]).split(' ')][2]
                if len(cur_item) == 5:
                    b_date: datetime = datetime.strptime(cur_item[2] + ' ' + cur_item[3] + ' ' + cur_item[4], '%d %b %Y')
                    formatted_row['Birthday'] = b_date.date()
                elif formatted_row['Birthday'] == None:
                    formatted_row['Birthday'] = 'Unknown'
                if 'DEAT' in cur_item:
                    dead_people.append([text for text in str(individual[0]).split(' ')][1].strip('@'))

            if formatted_row['ID'] in dead_people:
                continue
            living_people.append(formatted_row)
        return living_people
    # ((/))

    # ((method)) 0E_02
    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """

        listing_aunts_and_uncles_outcomes: PrettyTable = PrettyTable(self.aunts_and_uncles_lables)
        i: Dict
        for i in self.aunts_and_uncles:
            listing_aunts_and_uncles_outcomes.add_row([v for k, v in i.items()])
        print('Aunts and Uncles: < User Story No.20 >')
        print(listing_aunts_and_uncles_outcomes)
        BL()
        
        listing_age_outcomes: PrettyTable = PrettyTable(self.age_labels)
        i: Dict
        for i in self.individuals_with_age:
            listing_age_outcomes.add_row([v for k, v in i.items()])
        print('Individuals with Age: < User Story No.27 >')
        print(listing_age_outcomes)
        BL()

        listing_deceased_outcomes: PrettyTable = PrettyTable(self.deceased_labels)
        i: Dict
        for i in self.deceased_individuals:
            listing_deceased_outcomes.add_row([v for k, v in i.items()])
        print('Individuals are Deceased: < User Story No.29 >')
        print(listing_deceased_outcomes)
        BL()

        listing_living_outcomes: PrettyTable = PrettyTable(self.living_labels)
        i: Dict
        for i in self.living_individuals:
            listing_living_outcomes.add_row([v for k, v in i.items()])
        print('Individuals are Living: < User Story No.31 >')
        print(listing_living_outcomes)
        BL()

    # ((/))

# </>

# ------------------------------- #
""" # CORE DEFINING ENDS HERE # """


"""///*** define main program and execute it below ***///"""

# (((main function)))
def main(): #!! <- Main Program Procedure Flow !!#

    e = ezIO() #! <- Supporting Input/Output Class !#

    e.welcome() #! <- Print Out The Header !#
    
    File_Analyzer( e.open_file('YKF.ged') )
    SL()
    BL()
    
    # // "quit the program"
    e.quit_Main()
# (((/main function)))

"""///*** main program execute below ***///"""

if __name__ == '__main__':
    main()

"""///*** main program define and execution ends ***///"""

# ===== CODING ENDS ===== #
# //


# /// The Coding Experience and Conclusion ///
"""/'

Nope...

'/"""
# ///