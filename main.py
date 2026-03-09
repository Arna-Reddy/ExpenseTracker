# -------------------- IMPORTS --------------------
import os
import json
BUDGET_FILE = "expenses.json"
BUDGET_FILE = "budget.json"


def set_budget():
    try:
        budget = float(input("Enter your monthly budget: "))
    except ValueError:
        print("Enter a valid number.")
        return

    data = {"budget": budget}

    with open("budget.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Budget saved successfully!\n")


def get_budget():
    try:
        with open("budget.json", "r") as file:
            data = json.load(file)
            return data["budget"]
    except:
        return None
import sqlite3

print("Current working directory:", os.getcwd())

# -------------------- GLOBAL VARIABLES --------------------
expenses = []
JSON_FILE = "expenses.json"
DB_FILE = "expenses.db"


# -------------------- DATABASE SETUP --------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()
def export_to_json():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    expenses_list = []

    for row in rows:
        expense = {
            "id": row[0],
            "date": row[1],
            "category": row[2],
            "amount": row[3]
        }
        expenses_list.append(expense)

    with open("expenses.json", "w") as file:
        json.dump(expenses_list, file, indent=4)

    conn.close()

    print("Expenses exported to JSON successfully!")


# -------------------- JSON FUNCTIONS --------------------
def save_to_json():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "date": row[1],
            "category": row[2],
            "amount": row[3]
        })

    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    conn.close()


def load_from_json():
    global expenses
    try:
        with open(JSON_FILE, "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []


# -------------------- ADD EXPENSE --------------------
def add_expense():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    date = input("Enter date (YYYY-MM-DD): ")

    while True:
        category = input("Enter category: ").strip()
        if category:
            break
        else:
            print("Category cannot be empty.")

    while True:
        try:
            amount = float(input("Enter amount: "))
            break
        except ValueError:
            print("Enter valid number")

    cursor.execute("""
        INSERT INTO expenses (date, category, amount)
        VALUES (?, ?, ?)
    """, (date, category, amount))

    conn.commit()
    export_to_json()
    conn.close()

    save_to_json()

    print("Expense added successfully!\n")


# -------------------- VIEW EXPENSES --------------------
def view_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No expenses found.\n")
        return

    print("\nID | Date | Category | Amount")
    print("-" * 40)

    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | ₹{row[3]}")

    print()


# -------------------- TOTAL EXPENSE --------------------
def calculate_total():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()[0]

    conn.close()

    if result:
        print(f"\nTotal Expenses: ₹{result}\n")
    else:
        print("No expenses recorded.\n")


# -------------------- CATEGORY TOTAL --------------------
def category_total():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    category = input("Enter category: ").strip()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE category = ?",
        (category,)
    )

    result = cursor.fetchone()[0]
    conn.close()

    if result:
        print(f"Total for {category}: ₹{result}\n")
    else:
        print("No expenses found for this category.\n")


# -------------------- EDIT EXPENSE --------------------
def edit_expense():
    expense_id = input("Enter ID to edit: ")

    new_date = input("Enter new date: ")
    new_category = input("Enter new category: ")

    while True:
        try:
            new_amount = float(input("Enter new amount: "))
            break
        except ValueError:
            print("Enter valid number.")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET date=?, category=?, amount=?
        WHERE id=?
    """, (new_date, new_category, new_amount, expense_id))

    conn.commit()
    export_to_json()

    if cursor.rowcount == 0:
        print("Expense not found.\n")
    else:
        print("Expense updated.\n")

    conn.close()

    save_to_json()


# -------------------- DELETE EXPENSE --------------------
def delete_expense():
    expense_id = input("Enter ID to delete: ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    export_to_json()

    if cursor.rowcount == 0:
        print("Expense not found.\n")
    else:
        print("Expense deleted.\n")

    conn.close()

    save_to_json()


# -------------------- MONTHLY SUMMARY --------------------
def monthly_summary():
    month = input("Enter month (YYYY-MM): ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE date LIKE ?
    """, (month + "%",))

    total = cursor.fetchone()[0]

    conn.close()

    if total:
        print(f"Total for {month}: ₹{total}\n")
    else:
        print("No expenses for that month.\n")


# -------------------- CATEGORY SUMMARY --------------------
def category_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\nCategory Summary")
    print("-" * 30)

    for row in rows:
        print(f"{row[0]} : ₹{row[1]}")

    print()

def check_budget():
    budget = get_budget()

    if budget is None:
        print("Budget not set.\n")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    print("\nMonthly Budget:", budget)
    print("Total Spent:", total)

    if total > budget:
        print("⚠ Budget Exceeded!\n")
    else:
        print("Remaining Budget:", budget - total, "\n")




# -------------------- MAIN MENU --------------------
init_db()

while True:

    print("====== Expense Tracker ======")
    print("1. Set Budget")
    print("2. Add Expense")
    print("3. View Expenses")
    print("4. Total Expenses")
    print("5. Category Total")
    print("6. Edit Expense")
    print("7. Delete Expense")
    print("8. Monthly Summary")
    print("9. Category Summary")

    print("10. Check Budget")
    print("11. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        set_budget()

    elif choice == "2":
        add_expense()

    elif choice == "3":
        view_expenses()

    elif choice == "4":
        calculate_total()

    elif choice == "5":
        category_total()

    elif choice == "6":
        edit_expense()

    elif choice == "7":
        delete_expense()

    elif choice == "8":
        monthly_summary()
    elif choice == "9":
        category_summary()

    elif choice == "10":
        check_budget()

    elif choice == "11":
        print("Goodbye!")
        break


    else:
        print("Invalid choice.\n")