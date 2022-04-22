 # ===== Python - UTF-8 ===== #
"""/*
School: Stevens Institute of Technology
---------------------------------------
Course: SSW 555 - WS
Instructor: Prof. Richard Ens
-------------------------------------------
Project: # 08 / User Stories: 038, 039, 040
-------------------------------------------
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

        welcoming = "-== Welcome to ' User Stories: 038, 039, 040 ' ==-"
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
        self.birthday_lables: List = ['ID', 'Name', 'Gender', 'Birthday']
        self.anniversary_lables: List = ['Family', 'Husband', 'Wife', 'Anniversary']
        self.error_line_lables: List = ['Error Line Number', 'Content of the Error Line']

        self.lines = self.get_gedcom_file_lines()
        self.individuals_and_families = self.get_individuals_and_families()

        self.upcoming_birthdays = self.list_upcoming_birthdays()
        self.upcoming_anniversaries = self.list_upcoming_anniversaries()
        self.error_lines = self.list_error_lines()

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

        sum_of_error_line_numbers: List = []
        content_of_error_line: List = []
        individuals_head_index: int
        individuals_tail_index: int
        families_head_index: int
        families_tail_index: int
        cur_index: int = 0
        for line in self.lines:
            cur_index += 1

            if str(line).strip() == '':
                sum_of_error_line_numbers.append(str(cur_index))
                content_of_error_line.append(str("''"))
            elif [i for i in str(line).split(' ')][0] not in ('0', '1', '2'):
                sum_of_error_line_numbers.append(str(cur_index))
                content_of_error_line.append(str("'" + line + "'"))

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
        individuals_and_families.append(sum_of_error_line_numbers)
        individuals_and_families.append(content_of_error_line)

        #print(individuals_and_families[3]) # !<- Temporate Print Testing
        return individuals_and_families
    # ((/))

    # ((method)) 02 <- User Story #38
    def list_upcoming_birthdays(self) -> Optional[List]:

        happy_birthday_persons: List = []
        living_individuals: List = []
        item: str
        cur_year: datetime = datetime.today().year
        today: datetime = datetime.today()

        for individual in self.individuals_and_families[0]:
            flatted_info = ''.join([i for i in individual])
            if 'DEAT' in flatted_info:
                continue
            living_individuals.append(individual)
        
        for person in living_individuals:
            formatted_row: Dict = dict.fromkeys(self.birthday_lables)
            for item in person:
                cur_item = [i for i in item.split(' ')]
                if len(cur_item) == 5:
                    mod_item = [cur_item[2] + ' ' + cur_item[3] + ' ' + str(cur_year)]
                    b_date: datetime = datetime.strptime(''.join(mod_item), '%d %b %Y')
                    if 0 < (b_date - today).days < 31:
                        formatted_row['ID'] = [i for i in str(person[0]).split(' ')][1].strip('@')
                        formatted_row['Name'] = str(person[1][7:]).replace('/', '')
                        formatted_row['Gender'] = str(person[5][6:])
                        formatted_row['Birthday'] = datetime.strptime(cur_item[2] + ' ' + cur_item[3] + ' ' + cur_item[4], '%d %b %Y').date()
            
            if formatted_row['ID'] == None:
                continue
            happy_birthday_persons.append(formatted_row)

        return happy_birthday_persons
    # ((/))

    # ((method)) 03 <- User Story #39
    def list_upcoming_anniversaries(self) -> Optional[List]:

        happy_anniversary_persons: List = []
        living_people: List = []
        living_couples: List = []
        elem: str
        cur_year: datetime = datetime.today().year
        today: datetime = datetime.today()

        for individual in self.individuals_and_families[0]:
            flatted_info = ''.join([i for i in individual])
            if 'DEAT' in flatted_info:
                continue
            living_people.append([i for i in str(individual[0]).split(' ')][1].strip('@'))
        
        for family in self.individuals_and_families[1]:
            formatted_row: Dict = dict.fromkeys(self.anniversary_lables)
            if [i for i in str(family[1]).split(' ')][2].strip('@') in living_people:
                if [i for i in str(family[2]).split(' ')][2].strip('@') in living_people:
                    living_couples.append([i for i in str(family[1]).split(' ')][2].strip('@'))
                    living_couples.append([i for i in str(family[2]).split(' ')][2].strip('@'))
                    formatted_row['Family'] = [i for i in str(family[0]).split(' ')][1].strip('@')
                    m_date_line = [k for k in str(family[5]).split(' ')][2:4]
                    m_date: datetime = datetime.strptime(' '.join(m_date_line) + ' ' + str(cur_year), '%d %b %Y')
                    if 0 < (m_date - today).days < 31:
                        for human in self.individuals_and_families[0]:
                            if [i for i in str(family[1]).split(' ')][2].strip('@') in [j for j in str(human[0]).split(' ')][1].strip('@'):
                                formatted_row['Husband'] = str(human[1][7:]).replace('/', '')
                            if [i for i in str(family[2]).split(' ')][2].strip('@') in [j for j in str(human[0]).split(' ')][1].strip('@'):
                                formatted_row['Wife'] = str(human[1][7:]).replace('/', '')
                        formatted_row['Anniversary'] = datetime.strptime(' '.join([k for k in str(family[5]).split(' ')][2:]), '%d %b %Y').date()

            if formatted_row['Anniversary'] == None:
                continue
            happy_anniversary_persons.append(formatted_row)

        return happy_anniversary_persons
    # ((/))

    # ((method)) 04 <- User Story #40
    def list_error_lines(self) -> Optional[List]:

        error_lines: List = []
        pre_index: int = 0
        for unit in self.individuals_and_families[2]:
            pre_index += 1
            if pre_index > len(self.individuals_and_families[3]) - 1:
                break
            formatted_row: Dict = dict.fromkeys(self.error_line_lables)
            formatted_row['Error Line Number'] = str(unit)
            formatted_row['Content of the Error Line'] = self.individuals_and_families[3][pre_index]
            

            error_lines.append(formatted_row)
        #print(error_lines)    
        return error_lines
    # ((/))

    # ((method)) 0E_02
    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """

        listing_happy_birthday_people_outcomes: PrettyTable = PrettyTable(self.birthday_lables)
        i: Dict
        for i in self.upcoming_birthdays:
            listing_happy_birthday_people_outcomes.add_row([v for k, v in i.items()])
        print(f'Today: {datetime.today().date()}')
        print('Individual Who Has Upcoming Birthday in 30 Days: < User Story No.38 >')
        print(listing_happy_birthday_people_outcomes)
        BL()

        listing_happy_anniversary_people_outcomes: PrettyTable = PrettyTable(self.anniversary_lables)
        i: Dict
        for i in self.upcoming_anniversaries:
            listing_happy_anniversary_people_outcomes.add_row([v for k, v in i.items()])
        print(f'Today: {datetime.today().date()}')
        print('Couple Whose Upcoming Anniversary in 30 Days: < User Story No.39 >')
        print(listing_happy_anniversary_people_outcomes)
        BL()

        listing_error_lines_outcomes: PrettyTable = PrettyTable(self.error_line_lables)
        i: Dict
        for i in self.error_lines:
            listing_error_lines_outcomes.add_row([v for k, v in i.items()])
        print('Line Which Has Error: < User Story No.40 >')
        print(listing_error_lines_outcomes)
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
    
    File_Analyzer( e.open_file('YKF_ERROR.ged') )
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