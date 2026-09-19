# BudgetAndExpenseTracker
A lightweight python command line application to track personal budget and expenses

**Add Expenses**: Record new expenses with details including, category, name, price, and date.

**View Budget**: Display all saved expenses in a cleanly formatted terminal grind using tabulate.

**Delete Expenses**: Easily remove incorrect or outdated entries by name.

**Targeted Search**: Find specific expenses by name, category, or by price threshold (=, >=, <=).

**Date Range Summaries**: Calculate the total sum of expenses within a specific timeframe.

##Prequisites
Python 3.x

tabulate library

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tabulate.

```bash
pip install tabulate
```

##Useage

| Command | Description | Example |
| -------- | -------- | -------- |
| Add   | Prompts user to enter a new expense  | budget> add |
| show  | Allows user to view all recorded expenses  | budget> show  |
|delete | Prompts user for an item and removes item if found| budget> show|
|search <type> | Allows user to search for a price, name, or category | budget> search price |
|range | Allows user to get expense total from a range of dates | budget> range |
|-h or help |Brings up a menu of all commands | budget> help |
|quit or exit | Quits the program | budget> exit |
