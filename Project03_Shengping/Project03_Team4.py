from typing import List, Dict
import time
import prettytable
from enum import Enum


month_abbrev = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}


class GEDReader:
    def __init__(self):
        self.individual_dic: Dict[str, Individual] = {}
        self.family_dic: Dict[str, Family] = {}
        self.__cur_individual: Individual or None = None
        self.__cur_family: Family or None = None

    def read_ged_data(self, file_path):
        # Function that reads the content of the file
        try:
            f = open(file_path)
        except FileNotFoundError:
            print('FIle path is invalid!')
            return

        lines: List[str] = f.readlines()
        self.process_line(lines)

    def process_line(self, lines: List[str]):
        # Function that processes each line of the file according to its key word
        for i, line in enumerate(lines):
            words = line.split()
            if len(words) >= 3 and words[2] == 'INDI':
                self.add_data()
                self.__cur_individual = Individual(words[1].strip('@'))
            elif len(words) >= 3 and words[2] == 'FAM':
                self.add_data()
                self.__cur_family = Family(words[1].strip('@'))
            elif len(words) >= 2 and words[1] == 'DATE':
                year = int(words[-1])
                month = words[-2]
                if month not in month_abbrev.keys():
                    month = None
                else:
                    month = month_abbrev[month]
                day = words[-3]
                if not month:
                    day = None
                else:
                    try:
                        day = int(day)
                    except ValueError:
                        day = None
                date: Date = Date(year, month, day)
                last_line = lines[i-1].split()
                if last_line[1] == 'BIRT' and self.__cur_individual:
                    self.__cur_individual.birthday = date
                elif last_line[1] == 'DEAT' and self.__cur_individual:
                    self.__cur_individual.death_date = date
                elif last_line[1] == 'MARR' and self.__cur_family:
                    self.__cur_family.married_date = date
                elif last_line[1] == 'DIV' and self.__cur_family:
                    self.__cur_family.divorced_date = date
            elif len(words) >= 3 and words[1] == 'NAME' and self.__cur_individual:
                self.__cur_individual.name = ' '.join(words[2:])
            elif len(words) >= 3 and words[1] == 'SEX' and self.__cur_individual:
                self.__cur_individual.gender = 'Male' if words[2] == 'M' else 'Female'
            elif len(words) >= 3 and words[1] == 'HUSB' and self.__cur_family:
                self.__cur_family.husband = self.individual_dic[words[2].strip('@')]
            elif len(words) >= 3 and words[1] == 'WIFE' and self.__cur_family:
                self.__cur_family.wife = self.individual_dic[words[2].strip('@')]
            elif len(words) >= 3 and words[1] == 'CHIL' and self.__cur_family:
                self.__cur_family.child.append(self.individual_dic[words[2].strip('@')])
        self.post_process()

    def post_process(self):
        # Post process the child and spouse variable of each individual
        for family in self.family_dic.values():
            family.husband.family_list.append(family)
            family.wife.family_list.append(family)
            if not family.is_divorced():
                family.husband.spouse = family.wife
                family.wife.spouse = family.husband
            for c in family.child:
                family.husband.child.append(c)
                family.wife.child.append(c)
        for individual in self.individual_dic.values():
            individual.check_validity()

    def add_data(self):
        # When a new individual or family object is created, add the current data to the field dictionary
        if self.__cur_individual:
            self.individual_dic[self.__cur_individual.id] = self.__cur_individual
        if self.__cur_family:
            self.family_dic[self.__cur_family.id] = self.__cur_family
        self.__cur_family, self.__cur_individual = None, None

    def print_info(self):
        # print info with PrettyTable
        individual_pt: prettytable = prettytable.PrettyTable()
        individual_pt.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive',
                                     'Death', 'Child', 'Spouse', 'Valid']
        for k, v in self.individual_dic.items():
            individual_pt.add_row([k, v.name, v.gender, str(v.birthday), v.get_age(),
                                   v.is_alive(), v.death_date, ','.join([c.id for c in v.child]),
                                   v.spouse.id if v.spouse else None, v.is_valid])
        print(individual_pt)
        family_pt: prettytable = prettytable.PrettyTable()
        family_pt.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name',
                                 'Wife ID', 'Wife Name', 'Children']
        for k, v in self.family_dic.items():
            family_pt.add_row([k, v.married_date, v.is_divorced(), v.husband.id, v.husband.name, v.wife.id, v.wife.name,
                               ','.join([c.id for c in v.child])])
        print(family_pt)


class Individual:
    def __init__(self, individual_id):
        self.id: str = individual_id
        self.name: str = ''
        self.gender: str = ''
        self.birthday: Date or None = None
        self.death_date: Date or None = None
        self.child: List[Individual] = []
        self.spouse: Individual or None = None
        self.is_valid: bool = True
        self.family_list: List[Family] = []

    def get_age(self):
        bir = self.birthday
        if self.is_alive():
            t = time.localtime()
            age = t.tm_year - bir.year
            if t.tm_mon < bir.month or (t.tm_mon == bir.month and t.tm_mday < bir.day):
                age -= 1
            return age
        else:
            death = self.death_date
            age = death.year - bir.year
            if death.month < bir.month or (death.month == bir.month and death.day < bir.day):
                age -= 1
            return age

    def is_alive(self):
        return self.death_date is None

    def get_earliest_marriage_date(self):
        if len(self.family_list) == 0:
            return None
        return min([f.married_date for f in self.family_list])

    def get_earliest_divorced_date(self):
        if len(self.family_list) == 0:
            return None
        return min([f.divorced_date for f in self.family_list])

    def check_validity(self):
        # Check marriage date and birthday
        marriage_date: Date = self.get_earliest_marriage_date()
        if marriage_date and marriage_date < self.birthday:
            self.is_valid = False
            return


class Family:
    def __init__(self, family_id):
        self.id: str = family_id
        self.married_date: Date or None = None
        self.divorced_date: Date or None = None
        self.husband: Individual or None = None
        self.wife: Individual or None = None
        self.child: List[Individual] = []

    def is_divorced(self):
        return self.divorced_date is not None


class Date:
    def __init__(self, year=1, month=1, day=1):
        self.year = year
        self.month = month if month else 1
        self.day = day if day else 1

    def __str__(self):
        if self.month is None and self.day is None:
            return str(self.year)
        elif self.day is None:
            return str(self.year) + '-' + str(self.month)
        else:
            return str(self.year) + '-' + str(self.month) + '-' + str(self.day)

    def compare(self, other):
        if not other:
            return 1
        if self.year != other.year:
            return -1 if self.year < other.year else 1
        elif self.month != other.month:
            return -1 if self.month < other.month else 1
        elif self.day != other.day:
            return -1 if self.day < other.day else 1
        return 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __lt__(self, other):
        return self.compare(other) == -1

    def __gt__(self, other):
        return self.compare(other) == 1


if __name__ == '__main__':
    file_name = input('Please input the file name: ')
    reader = GEDReader()
    reader.read_ged_data(file_name)
    reader.print_info()
