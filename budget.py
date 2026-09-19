import csv
from pathlib import Path
import datetime
#import pandas as pd
from tabulate import tabulate

    
class BudgetAndExpense():
    def __init__(self, filename="budget.csv"):
        self.budget_file = filename
        self.file_path = Path(self.budget_file)
        self.headers = ["category", "name", "price", "date"]
        self.date_format = "%Y-%m-%d"
    
    
    def addExpense(self):
        files_exists = self.file_path.exists()
        expense = self.getExpenseInfo()
        if expense is None: #if addexpense returns None, user input was invalid and we should return to main menu
            return

        with open(self.file_path, 'a', newline="") as csvfile: #append will create the file if it does not already exist
            csv_writer = csv.writer(csvfile)
            
            if not files_exists: #if no file exists, writes a file containing the headers and the first expense
                csv_writer.writerow(self.headers)

            csv_writer.writerow(expense)          



    def deleteExpense(self):
        files_exists = self.file_path.exists()
        item_found = False #bool to see if item was found
        self.displayBudgetInfo()
        print("What item would you like to delete")
        to_delete = input()
        rows_to_keep = []

        #checks to see if file exists
        if not files_exists:
            print("No File Found!")
            return        
        
        else:        
            with open(self.file_path, 'r') as csvfile:  #gets all the rows we want to keep
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    if row.get("name") == to_delete: #gets the name from the csv and compares it to to_delete
                         item_found = True
                    elif any(row.values()): #checks too see if the isnt just blank before keeping it
                        rows_to_keep.append(row)
                
            if not item_found:  #all rows check no item found, file stays as is 
                print(f"{to_delete} was not found, returning to main menu")
                return

                
            with open(self.file_path, 'w', newline="") as csvfile: #item was found so rewriting file with valid rows 
                csv_writer= csv.writer(csvfile, fieldnames=self.headers)
                csv_writer.writeheder()
                csv_writer.writerow(rows_to_keep)

            print(f"{to_delete} has been removed")


    def getExpenseInfo(self):    
        temp_list = []
        #checks if date is being enteted, if so formats date to date object for easier use later
        for header in self.headers:
            if header.lower() == 'date':
                print(f"Enter {header} (YYYY-MM-DD): ")
                temp_list.append(self.formatDate(input()))
            else:
                print(f"Enter {header}: ")
                temp_list.append(input())

        try:
            price = float(temp_list[2]) #trys to cast price to float to ensure it is valid
        except:
            print(f"{temp_list[2]} is not a valid price, returning to main menu")
            return


        if temp_list[3] is None: #checks if date is valid, if not returns to main menu
            print(f"{temp_list[3]} is not a valid date, returning to main menu")
            return

        return temp_list

    def displayBudgetInfo(self):
        #uses tabulate to print a clean looking grid 
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)

            print(tabulate(data, tablefmt = "fancy_grid")) #headers not supplied as reader will read them right out of the csv filef

        except FileNotFoundError:
            print("No budget file exists. Please Add an expense to start a file")

    
    def searchEntry(self) -> list:
        """Return every expense whose name matches the requested entry."""
        entry = input("Enter an entry name to search for: ").strip().lower()
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", newline="") as csvfile:
            return [
                row for row in csv.DictReader(csvfile)
                if row.get("name", "").strip().lower() == entry
            ]

    def searchCategory(self) -> list:
        """Return every expense in the requested category."""
        category = input("Enter a category to search for: ").strip().lower()
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", newline="") as csvfile:
            return [
                row for row in csv.DictReader(csvfile)
                if row.get("category", "").strip().lower() == category
            ]

    def searchByPrice(self) -> list:
        """Return expenses matching a requested price and comparison operator."""
        criteria = input("Enter a price criterion (=, >=, or <=): ").strip()
        if criteria not in ("=", ">=", "<="):
            print("Please enter one of: =, >=, <=")
            return []

        try:
            price = float(input("Enter a price: ").strip())
        except ValueError:
            print("Please enter a valid price")
            return []

        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", newline="") as csvfile:
            matches = []
            for row in csv.DictReader(csvfile):
                try:
                    row_price = float(row.get("price", ""))
                except ValueError:
                    continue

                if (
                    criteria == "=" and row_price == price
                    or criteria == ">=" and row_price >= price
                    or criteria == "<=" and row_price <= price
                ):
                    matches.append(row)

            return matches

    def searchbyPrice(self) -> list:
        """Compatibility alias for the spelling used by the command description."""
        return self.searchByPrice()
         

    def formatDate(self, date: str) -> datetime:
        #checks that user atleast entered M-D-YYYY
        #rather than trying to format bad strings just catches bad strings, EAFP
        try:
            return datetime.datetime.strptime(date, self.date_format).date()
        except ValueError:
            print(f"{date} is invalid! Needs to be YYYY-MM-DD")
            return None
    
        
        

    def expenseSumDateRange(self) -> int:
        expense_sum = 0
        first_date = input("Enter the starting date of the range (YYYY-MM-DD): ")
        last_date = input("Enter the ending date of the range (YYYY-MM-DD): ")
        
        formattedFirstDate= self.formatDate(first_date)
        formattedLastDate = self.formatDate(last_date)

        if formattedFirstDate is None or formattedLastDate is None:
            print("Invalid date format, please try again")
            return

        if formattedFirstDate > formattedLastDate:
            print("First date must be before last date")
            return

        #iterates through csv rows expenses from dates in valid range
        with open(self.budget_file, "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if formattedFirstDate <= datetime.date.strptime(row["date"],self.date_format) <= formattedLastDate: 
                    expense_sum += float(row["price"])

        return expense_sum
