from datetime import datetime as dt
import json
from bs4 import BeautifulSoup
from pandas import read_json
import requests
from dataclasses import dataclass



# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        self.name = name
        self.date = date      
    
    def __str__ (self):
        return (self.__name, self.__date)
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
       self.currentHolidays = []
   
    def addHoliday(self, holidayname, date):
        holidarray = [holidayname, date]
        if holidarray in self.innerHolidays:
            self.currentHolidays.append(holidarray)
            print('The holiday has been added')
            return 1
        else:
            print('That holiday was not found, returning to main menu')
            return 0
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    # def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName, Date):
        holidarray = [HolidayName, Date]
        if holidarray in self.currentHolidays:
            self.currentHolidays.remove(holidarray)
            print('The holiday has been removed')
            return 1
        else:
            print('That holiday was not found, returning to main menu')
            return 0
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

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
        #print(type(temp[1]['name'])) #Testing print statements
        #print(temp[1]['date'])
        #print(temp)
        for a in temp:
            self.currentHolidays.append([a['name'], a['date']])
        #Array formated as (Name, Date), (Name, Date)
        #return self.currentHolidays
        
            # Read in things from json file location
            # Use addHoliday function to add holidays to inner list.

    def save_to_json(self):
        list1 = []
        for i in self.currentHolidays:
            namedate = i
            list1.append({'name' : namedate[0], 'date' : namedate[1]})
        jsonHolidays = {'Holidays' : list1}
        f = open('HolidayManager\Test.JSON', "w")
        json.dump(jsonHolidays, f)
        f.close()
    
    def datechange(monthday, year):
        format = dt.strptime((monthday + ' ' + str(year)),'%b %d %Y')
        canadianDateFormat = '%Y-%m-%d'
        aDate = dt.strftime(format, canadianDateFormat)
        return aDate
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            html = requests.get(f'https://www.timeanddate.com/holidays/us/{year}?hol=33554809')
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            
            for row in rows:
                date = row.find('th').text
                date1 = str(date)
                date2 = HolidayList.datechange(date1, year)
                name = row.find('a').text
                newholiday = Holiday(name, date2)
                newholiday1 = [name, date2]
                self.innerHolidays.append(newholiday1)  

    def numHolidays(self):
        total = len(self.innerHolidays)
        return total
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(year, week_number):
        print('working on it')
        Holidayweek = list(filter(lambda a:7))
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    #def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    #def getWeather(weekNum): #No Weather API will be used 
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    #def viewCurrentWeek():  
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week




def main():
    hidden = HolidayList()
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
            input7 = input('Please enter a valid year from 2020-2024: ')
            input8 = input('Please enter a week from 1-52, or blank for current week : ')

        else:
            print('Error, invalid input, please try again')

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


#if __name__ == "__main__":
    #main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.



main()

#stuff = HolidayList()
#rest = stuff.read_json()
#rest
