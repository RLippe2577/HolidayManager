from datetime import datetime as dt
import json
from bs4 import BeautifulSoup
from pandas import read_json
import requests
from dataclasses import dataclass


class Holiday:
      
    def __init__(self,name, date):
        self.name = name
        self.date = date      
    
    def __str__ (self):
        return f"{self.name} ({self.date})"

    def values(self):
        list = [self.name, self.date]
        return list

           

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
       self.currentHolidays = []
       self.holidayobject = []
   
    def addHoliday(self, holidayname, date):
        holidarray = [holidayname, date]
        if holidarray in self.innerHolidays:
            self.currentHolidays.append(holidarray)
            print('The holiday has been added')
            return 1
        else:
            print('That holiday was not found, returning to main menu')
            return 0


    def removeHoliday(self, HolidayName, Date):
        holidarray = [HolidayName, Date]
        if holidarray in self.currentHolidays:
            self.currentHolidays.remove(holidarray)
            print('The holiday has been removed')
            return 1
        else:
            print('That holiday was not found, returning to main menu')
            return 0


    def read_json(self):
        f = open('HolidayManager\holidays.JSON', 'r')
        load = json.load(f)
        f.close
        temp = []
        dates1 = []
        names = []
        for i in load:
            for x in load[i]:
                temp.append(x)
        for a in temp:
            self.currentHolidays.append([a['name'], a['date']])

    def save_to_json(self): #In the output file TEST, there are no newlines added, but it could be imported the same way as the starting file.
        list1 = []
        for i in self.currentHolidays:
            namedate = i
            list1.append({'name' : namedate[0], 'date' : namedate[1]})
        jsonHolidays = {'Holidays' : list1}
        f = open('HolidayManager\Test.JSON', "w")
        json.dump(jsonHolidays, f)
        f.close()
    
    def datechange(monthday, year): #Returns date in string format, I convert back to date in the scrape function 
        format = dt.strptime((monthday + ' ' + str(year)),'%b %d %Y')
        canadianDateFormat = '%Y-%m-%d'
        aDate = dt.strftime(format, canadianDateFormat)
        return aDate
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024] #All 5 years
        for year in years:
            html = requests.get(f'https://www.timeanddate.com/holidays/us/{year}?hol=33554809')
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            
            for row in rows:
                date = row.find('th').text
                date1 = str(date)
                date2 = HolidayList.datechange(date1, year)
                dateobject = dt.strptime(date2, '%Y-%m-%d')
                name = row.find('a').text
                newholiday = Holiday(name, dateobject)
                self.holidayobject.append(newholiday) #I did this because I wanted to test working with the scraped holidays in different formats
                newholiday1 = [name, date2]
                self.innerHolidays.append(newholiday1)  

    def numHolidays(self): #Didn't need to use this for anything
        total = len(self.innerHolidays)
        return total

    
    def filter_holidays_by_week(self, year, week_number):
        output = list(filter(lambda a: a.values()[1].strftime('%W') == week_number and a.values()[1].strftime('%Y') == year, self.holidayobject))
        return output
            

    def displayHolidaysInWeek(self, holidayList):
        for i in holidayList:
            print(i)

    def viewCurrentWeek(self):  
        today = dt.today()
        iso = today.isocalendar()
        weeknumber = iso[1]
        return weeknumber




def main():
    hidden = HolidayList() #Assigned the class as hidden, because I initially thought of the holiday list as hidden from the user
    hidden.read_json()
    changes = 0
    stop = 0
    hidden.scrapeHolidays()
    while stop == 0:
        print('Holiday Menu \n'
    '================ \n'
    '1. Add a Holiday \n'
    '2. Remove a Holiday \n'
    '3. Save Holiday List \n'
    '4. View Holidays \n'
    '5. Exit')
        input1 = input('Please enter a number for options 1-5 : ')
        if input1 == '5':
            if changes == 0:
                print('You have no unsaved changes, have a nice day')
                stop = 1
            else:
                print('You have unsaved changes, would you like to save?')
                input2 = input('Please enter yes or no : ')
                if input2 == 'no':
                    print('Very well, have a nice day')
                    stop = 1
                elif input2 == 'yes':
                    hidden.save_to_json()
                    print('Your changes have been saved, have a nice day')
                    stop = 1
                else:
                    print('invalid input, please try again from main menu')
        elif input1 == '3':
            if changes == 0:
                print('There were no changes to save, returning to main menu')
            else:
                hidden.save_to_json()
                print('Your changes have been saved, returning to menu')
                changes = 0
        elif input1 == '2':
            input3 = input('Please enter a valid Holiday to remove (case sensitive, capitilize the start of each word): ')
            input4 = input('Please enter the date for the holiday in YYYY-MM-DD (include dashes) : ')
            success = hidden.removeHoliday(input3, input4)
            if success == 1:
                changes = 1
        elif input1 == '1':
            input5 = input('Please enter a valid Holiday to add (case sensitive, capitilize the start of each word): ')
            input6 = input('Please enter the date for the holiday in YYYY-MM-DD (include dashes) : ')
            success = hidden.addHoliday(input5, input6)
            if success == 1:
                changes = 1
        elif input1 == '4':
            validyear = ['2020','2021','2022','2023','2024']
            input7 = input('Please enter a valid year from 2020-2024: ')
            input8 = input('Please enter a week from 1-52, or blank for current week : ')
            if input7 not in validyear:  #Input checking
                print('Error, that is not a valid year, please try again from the main menu')
            elif input8 == '':
                week = hidden.viewCurrentWeek()
                filtered = hidden.filter_holidays_by_week(input7, str(week))
                if filtered == []:
                    print('There are no Holidays this week')
                else:
                    hidden.displayHolidaysInWeek(filtered)
            elif len(input8) != 2: #Input checking
                print('Error, please enter a double digit week number, try again from the main menu')
            else:
                filtered = hidden.filter_holidays_by_week(input7, input8)
                if filtered == []:
                    print('There are no Holidays this week')
                else:
                    hidden.displayHolidaysInWeek(filtered)

                    
        else:
            print('Error, invalid input, please try again')


main()


