from typing import List, Dict
from IndividualNFamily import Individual, Family
from Date import Date
import time
from collections import defaultdict


class ValidityChecker:
    def __init__(self):
        self.error_log: List[str] = []

    def check_individual(self, individual: Individual):
        self.__check_birthday_and_other_dates(individual)
        self.__check_dates_before_current_date(individual)
        self.__check_age_validity(individual)
        self.__check_birth_and_death_of_parents(individual)
        self.__check_marriage_validity(individual)
        self.__check_bigamy(individual)
        self.__check_parent_too_old(individual)
        self.__check_siblings_space(individual)
        self.__check_multi_birth(individual)
        self.__check_sibling_marriage(individual)
        self.__check_no_marriage_to_descendants(individual)

    def check_family(self, family: Family):
        self.__check_marriage_date_and_divorced_date(family)
        self.__check_siblings_num(family)
        self.__check_correct_gender(family)
        self.__check_males_carry_last_name(family)
        self.__check_birth_before_marriage_of_parent(family)
        self.__check_unique_first_names_in_families(family)

    def set_invalid_individual(self, individual: Individual, error_msg: str):
        individual.is_valid = False
        self.error_log.append(error_msg.format(name=individual.name))

    def set_invalid_family(self, family: Family, error_msg: str):
        family.is_valid = False
        self.error_log.append(error_msg.format(id=family.id))

    # -------------------------------------Individual check functions------------------------------------------------- #

    def __check_birthday_and_other_dates(self, individual: Individual):
        # Check birthday date and other dates
        if individual.death_date and individual.death_date < individual.birthday:
            self.set_invalid_individual(individual, 'ERROR: The death date of {name} is later than his/her birthday!')
        marriage_date: Date = individual.get_earliest_marriage_date()
        if marriage_date and marriage_date < individual.birthday:
            self.set_invalid_individual(individual,
                                        'ERROR: The marriage date of {name} is earlier than his/her birthday!')
        divorced_date: Date = individual.get_earliest_divorced_date()
        if divorced_date and divorced_date < individual.birthday:
            self.set_invalid_individual(individual,
                                        'ERROR: The divorced date of {name} is earlier than his/her birthday!')

    def __check_dates_before_current_date(self, individual: Individual):
        t = time.localtime()
        curr_date: Date = Date(t.tm_year, t.tm_mon, t.tm_mday)
        if individual.birthday and individual.birthday > curr_date:
            self.set_invalid_individual(individual, 'ERROR: The birthday of {name} is later than current date!')
        if individual.death_date and individual.death_date > curr_date:
            self.set_invalid_individual(individual, 'ERROR: The death date of {name} is later than current date!')
        marriage_date = individual.get_earliest_marriage_date()
        if marriage_date and marriage_date > curr_date:
            self.set_invalid_individual(individual, 'ERROR: The marriage date of {name} is later than current date!')
        divorced_date = individual.get_earliest_divorced_date()
        if divorced_date and divorced_date > curr_date:
            self.set_invalid_individual(individual, 'ERROR: The divorced date of {name} is later than current date!')

    def __check_age_validity(self, individual: Individual):
        if individual.get_age() > 150:
            self.set_invalid_individual(individual, 'WARNING: The age of {name} is larger than 150')

    def __check_birth_and_death_of_parents(self, individual: Individual):
        father: Individual = individual.father
        mother: Individual = individual.mother
        if (father and father.death_date and father.death_date < individual.birthday) or \
                (mother and mother.death_date and mother.death_date < individual.birthday):
            self.set_invalid_individual(individual, 'ERROR: The birthday of {name} is'
                                                    ' later than the death date of his/her parent')

    def __check_marriage_validity(self, individual: Individual):
        family_list: List[Family] = individual.family_list
        for family in family_list:
            if family.married_date and family.married_date - individual.birthday < 14:
                self.set_invalid_individual(individual, 'WARNING: The marriage date of {name} is younger than 14.')
                break

    def __check_bigamy(self, individual: Individual):
        family_list: List[Family] = individual.family_list
        family_list.sort(key=lambda f: f.married_date)
        for i in range(1, len(family_list)):
            f1, f2 = family_list[i-1], family_list[i]
            if (f2.married_date and f1.divorced_date and f2.married_date < f1.divorced_date) or not f1.is_divorced():
                self.set_invalid_individual(individual, 'WARNING: Bigamy happens in the data of {name}.')
                break

    def __check_parent_too_old(self, individual: Individual):
        mother, father = individual.mother, individual.father
        if not individual.birthday:
            return
        if mother and mother.birthday and mother.birthday - individual.birthday > 60:
            self.set_invalid_individual(individual, 'WARNING: Mother of {name} is too old.')
        if father and father.birthday and father.birthday - individual.birthday > 80:
            self.set_invalid_individual(individual, 'WARNING: Father of {name} is too old.')

    def __check_siblings_space(self, individual: Individual):
        if not individual.birthday:
            return
        for s in individual.siblings:
            if not s.birthday:
                continue
            diff = individual.birthday.datetime - s.birthday.datetime
            if 1 < abs(diff.days) < 240:
                self.set_invalid_individual(individual, 'ERROR: Siblings space of {name} is incorrect.')
                break

    def __check_multi_birth(self, individual: Individual):
        if not individual.birthday:
            return
        multi_birth_num = 0
        for s in individual.siblings:
            if not s.birthday:
                continue
            diff = individual.birthday.datetime - s.birthday.datetime
            if abs(diff.days) <= 1:
                multi_birth_num += 1
        if multi_birth_num > 5:
            self.set_invalid_individual(individual, 'WARNING: 5 or more siblings are born in the data of {name}.')

    def __check_no_marriage_to_descendants(self, individual: Individual):
        spouse = individual.spouse
        if not spouse:
            return
        descendants = individual.get_all_descendants()
        if spouse in descendants:
            self.set_invalid_individual(individual, 'WARNING: {name} is married to one of his/her descendants!')
            return
        for s in individual.past_spouse:
            if s in descendants:
                self.set_invalid_individual(individual, 'WARNING: {name} is married to one of his/her descendants!')
                return

    def __check_sibling_marriage(self, individual: Individual):
        spouse = individual.spouse
        if not spouse:
            return
        if spouse in individual.siblings:
            self.set_invalid_individual(individual, 'WARNING: {name} is married to one of their siblings!')

    # -------------------------------------Family check functions----------------------------------------------------- #

    def __check_marriage_date_and_divorced_date(self, family: Family):
        if family.is_divorced() and family.married_date > family.divorced_date:
            self.set_invalid_family(family, 'ERROR: The marriage date of {id} is later than their divorced date!')

    def __check_siblings_num(self, family: Family):
        if len(family.child) > 15:
            self.set_invalid_family(family, 'WARNING: The siblings number of {id} is more than 15!')

    def __check_correct_gender(self, family: Family):
        husband, wife = family.husband, family.wife
        if husband and husband.gender != 'Male':
            self.set_invalid_family(family, 'WARNING: The husband of {id} is not a male!')

    def __check_males_carry_last_name(self, family: Family):
        husband = family.husband
        if not husband:
            return
        family_name = family.husband.name.split()[1]
        for c in family.child:
            if c.gender == 'Male' and c.name.split()[1] != family_name:
                self.set_invalid_individual(c, 'WARNING: The last name of {name} is different from his/her father!')

    def __check_birth_before_marriage_of_parent(self, family: Family):
        marriage_date = family.married_date
        for c in family.child:
            if c .birthday < marriage_date:
                self.set_invalid_individual(c, 'WARNING: The birthday of {name} is earlier'
                                               ' than the marriage date of his/her parents!')

    def __check_unique_first_names_in_families(self, family: Family):
        lis = list(family.child)
        lis.append(family.husband)
        lis.append(family.wife)
        memo = defaultdict(list)
        for c in lis:
            if c.name not in memo.keys():
                memo[c.name].append(c)
            else:
                for indi in memo[c.name]:
                    if indi.birthday == c.birthday:
                        self.set_invalid_individual(c, 'WARNING: There are multiple {name} with '
                                                       'the same birthday in a single family!')
