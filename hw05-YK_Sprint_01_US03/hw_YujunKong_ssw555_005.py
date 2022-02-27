# ===== Python - UTF-8 ===== #
"""/*
School: Stevens Institute of Technology
---------------------------------------
Course: SSW 555 - WS
Instructor: Prof. Richard Ens
----------------------------------------------------------------
Homework: # 05 / Summary birth before death from the GEDCOM file
----------------------------------------------------------------
Coder with CWID: Yujun Kong / 1046 6820
Team with members # 04: Kristin Allocco / Shengping Xu / Yujun Kong
*/"""
# ===== CODING BEGINS ===== #

# * import the supporting types, libraries, modules
import sys
from typing import Any, List, Dict, Optional, IO
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

        welcoming = "-== Welcome to ' Summary birth before death from the GEDCOM file ' ==-"
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

        self.label_keys: List = ['ID', 'Birthday', 'Passdate', 'Name', 'Gender']

        self.lines = self.get_gedcom_file_lines()
        
        self.get_individuals_with_brithNdeath_info()        
        self.format_individuals_with_brithNdeath_info()

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
    def get_individuals_with_brithNdeath_info(self) -> Optional[List]:

        individuals_head_index: int
        individuals_tail_index: int
        cur_index: int = 0
        for line in self.lines:
                cur_index += 1
                if line == '0 @I1@ INDI':
                    individuals_head_index = cur_index
                elif line == '0 @F1@ FAM':
                    individuals_tail_index = cur_index
        
        individuals_block: List = self.lines[individuals_head_index - 1 : individuals_tail_index - 1]
        individuals_block = individuals_block + ['0 End of INDI 0']

        each_individual_combination: List = []
        unit_cur_index: int = 0
        unit_head_index: int = 0
        each_individual: List = []
        for unit in individuals_block[unit_head_index : ]:                
            unit_cur_index += 1
            if ('0' and 'INDI' in unit) and (unit != individuals_block[unit_head_index]):
                each_individual = individuals_block[unit_head_index : unit_cur_index - 1]                    
                unit_head_index = unit_cur_index - 1                
                each_individual_combination.append(each_individual)

        dead_individual_with_birth_and_death_combination: List = []
        for individual in each_individual_combination:
            if 'BIRT' in individual[6]:
                if 'DEAT' in individual[8]:
                    dead_individual_with_birth_and_death_combination.append(individual)

        #print(dead_individual_with_birth_and_death_combination)
        return dead_individual_with_birth_and_death_combination
    # ((/))

    # ((method)) 02
    def format_individuals_with_brithNdeath_info(self) -> Optional[List]:

        birth_before_death_info_rows: List = []
        _birthday: datetime.date()
        _deathday: datetime.date()

        cur_idx: int = 0
        cur_ID: int = 0
        for dead_individual in self.get_individuals_with_brithNdeath_info():
            formatted_row: Dict = dict.fromkeys(self.label_keys)

            cur_ID += 1
            if cur_ID <= 9:
                formatted_row['ID'] = 'I' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                formatted_row['ID'] = 'I' + str(cur_ID)

            for item in dead_individual:

                if 'BIRT' in item:
                    b_date: datetime = datetime.strptime(dead_individual[7][7:], '%d %b %Y')
                    formatted_row['Birthday'] = str(b_date.date())

                if 'DEAT' in item:
                    d_date: datetime = datetime.strptime(dead_individual[9][7:], '%d %b %Y')
                    formatted_row['Passdate'] = str(d_date.date())

                if 'NAME' in item:
                    formatted_row['Name'] = item[7:]

                if 'SEX' in item:
                    formatted_row['Gender'] = item[6:]

            birth_before_death_info_rows.append(formatted_row)

        return birth_before_death_info_rows
    # ((/))

    # ((method)) 0E
    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """
                  
        birth_before_death_table: PrettyTable = PrettyTable(self.label_keys)
        i: Dict
        for i in self.format_individuals_with_brithNdeath_info():
            birth_before_death_table.add_row([v for k, v in i.items()])
        
        print('Birth Before Death:')
        print(birth_before_death_table)
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