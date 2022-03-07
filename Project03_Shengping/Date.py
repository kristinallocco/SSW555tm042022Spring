from typing import List, Dict


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

    def __compare(self, other):
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
        return self.__compare(other) == 0

    def __lt__(self, other):
        return self.__compare(other) == -1

    def __gt__(self, other):
        return self.__compare(other) == 1

    def __sub__(self, other):
        res = self.year - other.year
        if self.month < other.month or (self.month == other.month and self.day < other.day):
            res += 1
        return res
