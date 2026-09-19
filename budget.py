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

        file_needs_header = (
            not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        )

        with open(self.file_path, 'a', newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            if file_needs_header:
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

                
            with open(self.file_path, 'w', newline="") as csvfile:
                csv_writer = csv.DictWriter(
                    csvfile,
                    fieldnames=self.headers
                )
                csv_writer.writeheader()
                csv_writer.writerows(rows_to_keep)

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
            price = float(temp_list[2]) #trys to cast to float to ensure validity 
        except ValueError:
            print(f"{temp_list[2]} is not a valid price, returning to main menu")
            return

        temp_list[2] = str(price)

        if temp_list[3] is None:
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

    
    def searchEntry(self, entry: str | None = None) -> list:
        if entry is None:
            entry = input("Enter an entry name to search for: ").strip()

        target = entry.strip().lower()
        if not target or not self.file_path.exists():
            return []

        with open(self.file_path, "r", newline="") as csvfile:
            return [
                row for row in csv.DictReader(csvfile)
                if row.get("name", "").strip().lower() == target
            ]

    def searchCategory(self, category: str | None = None) -> list:
        if category is None:
            category = input("Enter a category to search for: ").strip()

        target = category.strip().lower()
        if not target or not self.file_path.exists():
            return []

        with open(self.file_path, "r", newline="") as csvfile:
            return [
                row for row in csv.DictReader(csvfile)
                if row.get("category", "").strip().lower() == target
            ]

    def searchByPrice(self) -> list:
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

    def formatDate(self, date: str) -> datetime:
        #checks that user atleast entered M-D-YYYY
        #rather than trying to format bad strings just catches bad strings, EAFP
        try:
            return datetime.datetime.strptime(date, self.date_format).date()
        except ValueError:
            print(f"{date} is invalid! Needs to be YYYY-MM-DD")
            return None
    
        
        

    def expenseSumDateRange(self, first_date: str | None = None, last_date: str | None = None) -> float:
        #Return the sum of all expenses between two dates inclusive
        if first_date is None:
            first_date = input("Enter the starting date of the range (YYYY-MM-DD): ").strip()
        if last_date is None:
            last_date = input("Enter the ending date of the range (YYYY-MM-DD): ").strip()

        formatted_first_date = self.formatDate(first_date)
        formatted_last_date = self.formatDate(last_date)

        if formatted_first_date is None or formatted_last_date is None:
            print("Invalid date format, please try again")
            return 0.0

        if formatted_first_date > formatted_last_date:
            print("First date must be before last date")
            return 0.0

        if not self.file_path.exists():
            return 0.0

        expense_sum = 0.0
        with open(self.file_path, "r", newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                try:
                    row_date = datetime.datetime.strptime(row["date"], self.date_format).date()
                    row_price = float(row["price"])
                except (KeyError, TypeError, ValueError):
                    continue

                if formatted_first_date <= row_date <= formatted_last_date:
                    expense_sum += row_price

        return expense_sum
