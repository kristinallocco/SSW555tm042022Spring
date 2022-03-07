from typing import List, Dict
import prettytable
from Date import Date
from IndividualNFamily import Individual, Family
from ValidityChecker import ValidityChecker


month_abbrev = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}


class GEDReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.individual_dic: Dict[str, Individual] = {}
        self.family_dic: Dict[str, Family] = {}
        self.__cur_individual: Individual or None = None
        self.__cur_family: Family or None = None
        self.error_log: List[str] = []
        self.__validity_checker = ValidityChecker()
        self.__read_ged_data()

    def __read_ged_data(self):
        # Function that reads the content of the file
        try:
            f = open(self.file_path)
        except FileNotFoundError:
            print('FIle path is invalid!')
            return

        lines: List[str] = f.readlines()
        self.__process_line(lines)

    def __process_line(self, lines: List[str]):
        # Function that processes each line of the file according to its key word
        for i, line in enumerate(lines):
            words = line.split()
            if len(words) >= 3 and words[2] == 'INDI':
                self.__add_data()
                self.__cur_individual = Individual(words[1].strip('@'))
            elif len(words) >= 3 and words[2] == 'FAM':
                self.__add_data()
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
        self.__post_process()

    def __post_process(self):
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
                c.father = family.husband
                c.mother = family.wife

        for individual in self.individual_dic.values():
            self.__validity_checker.check_individual(individual)
        for family in self.family_dic.values():
            self.__validity_checker.check_family(family)

    def __add_data(self):
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
                                 'Wife ID', 'Wife Name', 'Children', 'Valid']
        for k, v in self.family_dic.items():
            family_pt.add_row([k, v.married_date, v.is_divorced(), v.husband.id, v.husband.name, v.wife.id, v.wife.name,
                               ','.join([c.id for c in v.child]), v.is_valid])
        print(family_pt)
        self.print_error_log()

    def print_error_log(self):
        for log in self.__validity_checker.error_log:
            print(log)

    def get_name(self, individual_id: str):
        individual: Individual = self.individual_dic[individual_id]
        return individual.name

    def get_age(self, individual_id: str):
        individual: Individual = self.individual_dic[individual_id]
        return individual.get_age()

    def get_marriage_date(self, family_id: str):
        family: Family = self.family_dic[family_id]
        return str(family.married_date)

    def get_divorced_date(self, family_id: str):
        family: Family = self.family_dic[family_id]
        return str(family.divorced_date)


if __name__ == '__main__':
    file_name = input('Please input the file name: ')
    reader = GEDReader(file_name)
    reader.print_info()
