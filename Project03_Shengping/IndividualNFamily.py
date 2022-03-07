from typing import List
from Date import Date
import time


class Individual:
    def __init__(self, individual_id):
        self.id: str = individual_id
        self.name: str = ''
        self.gender: str = ''
        self.birthday: Date or None = None
        self.death_date: Date or None = None
        self.child: List[Individual] = []
        self.spouse: Individual or None = None
        self.father: Individual or None = None
        self.mother: Individual or None = None
        self.is_valid: bool = True
        self.family_list: List[Family] = []

    def get_age(self):
        bir = self.birthday
        if not bir:
            return -1
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
        date_list: List[Date] = []
        for f in self.family_list:
            if f.married_date:
                date_list.append(f.married_date)
        return min(date_list) if date_list else None

    def get_earliest_divorced_date(self):
        if len(self.family_list) == 0:
            return None
        date_list: List[Date] = []
        for f in self.family_list:
            if f.divorced_date:
                date_list.append(f.married_date)
        return min(date_list) if date_list else None


class Family:
    def __init__(self, family_id):
        self.id: str = family_id
        self.married_date: Date or None = None
        self.divorced_date: Date or None = None
        self.husband: Individual or None = None
        self.wife: Individual or None = None
        self.is_valid = True
        self.child: List[Individual] = []

    def is_divorced(self):
        return self.divorced_date is not None
