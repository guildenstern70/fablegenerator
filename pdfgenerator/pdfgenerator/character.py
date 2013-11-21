'''
PDFGenerator
character.py

@author: Alessio Saltarin
'''

import time
import datetime
import sys

class Character(object):

    def calculate_age(self, born):
        today = datetime.date.today()
        try: 
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_age(self):
        age = -1
        try:
            birth_date = time.strptime(self.birthdate, "%d-%b-%y")
            birth_datetime = datetime.date.fromtimestamp(time.mktime(birth_date))
            age = self.calculate_age(birth_datetime)
        except:
            print sys.exc_info()
            print

        return age

    def __init__(self, cname, csex, cbirthdate):
        self.sex = csex
        self.name = cname
        self.birthdate = cbirthdate
        self.age = self.get_age()
        
        
        
        