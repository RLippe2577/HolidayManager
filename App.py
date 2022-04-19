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
   
    def addHoliday(self, holidayObj):
        correct = 0
        while correct == 0:
            if type(holidayObj) == object:
                correct = 1
            else:
                self.innerHolidays.append(holidayObj)
                print('You have added a holiday')
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    # def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

    #def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json():
        f = open('HolidayManager\holidays.JSON', 'r')
        load = json.load(f)
        f.close
        temp = []
        currentHolidays = []
        dates1 = []
        names = []
        for i in load:
            for x in load[i]:
                temp.append(x)
        #print(type(temp[1]['name'])) #Testing print statements
        #print(temp[1]['date'])
        #print(temp)
        for a in temp:
            currentHolidays.append([temp[1]['name'], temp[1]['date']])
        print(currentHolidays) #Array formated as (Name, Date), (Name, Date)
            # Read in things from json file location
            # Use addHoliday function to add holidays to inner list.

    def save_to_json(self):
        f = open('HolidayManager\Test.JSON', "w")
        json.dump(self.innerHolidays, f)
        f.close()
    
    def datechange(monthDay, year):
        format = dt.strptime((monthDay + ' ' + year),'%b %d %Y')
        canadianDateFormat = '%Y-%m-%d'
        aDate = dt.strftime(format, canadianDateFormat)
        print(aDate)
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            html = requests.get(f'https://www.timeanddate.com/holidays/us/'year'?hol=33554809')
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            
            for row in rows:
                date = self.datechange(row.find('th').text, year)
                name = row.find('a').text
                newholiday = Holiday(name, date)
                self.innerHolidays.append(newholiday)  

    def numHolidays(self):
        total = len(self.innerHolidays)
        return total
        # Return the total number of holidays in innerHolidays
    
    #def filter_holidays_by_week(year, week_number):
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

    #def viewCurrentWeek():  #No Weather API will be used 
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



#def main():
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




