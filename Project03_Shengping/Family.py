from typing import List, Dict
import IndividualNFamily
from Date import Date
import time

Individual = IndividualNFamily.Individual

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