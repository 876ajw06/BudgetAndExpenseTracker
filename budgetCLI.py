import argparse
from budget import BudgetAndExpense

def main():
    parser = argparse.ArgumentParser(description="Command Line Budget and Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Command: addExpense
    subparsers.add_parser("add", help="Add a new expense")

    # Command: displayBudgetInfo
    subparsers.add_parser("show", help="Display budget info in a grid")

    # Command: deleteExpense
    subparsers.add_parser("delete", help="Delete an expense")

    # Command: search (entry, category, price)
    search_parser = subparsers.add_parser("search", help="Search expenses")
    search_parser.add_argument(
        "type", 
        choices=["entry", "category", "price"], 
        help="Type of search to perform"
    )

    # Command: expenseSumDateRange
    range_parser = subparsers.add_parser("range", help="Get sum of expenses within a date range")
    
    # Parse arguments and instantiate the app
    args = parser.parse_args()
    app = BudgetAndExpense()

    #rroute to the appropriate method based on the command
    if args.command == "add":
        app.addExpense()
        
    elif args.command == "show":
        app.displayBudgetInfo()
        
    elif args.command == "delete":
        app.deleteExpense()
        
    elif args.command == "search":
        if args.type == "entry":
            print(app.searchEntry())
        elif args.type == "category":
            print(app.searchCategory())
        elif args.type == "price":
            print(app.searchByPrice())
            
    elif args.command == "range":
        result = app.expenseSumDateRange()
        if result is not None:
            print(f"${result:.2f}")

if __name__ == "__main__":
    main()