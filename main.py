import os
print("Current working directory:", os.getcwd())
import json
import sqlite3

expenses = []
def init_db():
    print("init_db is running...")
    conn = sqlite3.connect("expenses.db")
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

init_db()


def load_from_file():
    global expenses
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []

def save_to_file():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def add_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    date = input("Enter date (YYYY-MM-DD): ")

    # 👇 ADD CATEGORY VALIDATION HERE
    while True:
        category = input("Enter category: ").strip()
        if category:
            break
        else:
            print("Category cannot be empty.")

    amount = float(input("Enter amount: "))

    cursor.execute("""
        INSERT INTO expenses (date, category, amount)
        VALUES (?, ?, ?)
    """, (date, category, amount))

    conn.commit()
    conn.close()

    print("Expense added successfully!")
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No expenses found.\n")
        return

    print("\nID  Date         Category      Amount")
    print("-" * 40)

    for row in rows:
        print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | Amount: ₹{row[3]}")

    print()
def category_total():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    category = input("Enter category: ")

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE category = ?",
        (category,)
    )

    result = cursor.fetchone()[0]

    if result:
        print(f"\nTotal for {category}: ₹{result}")
    else:
        print("No expenses found for this category.")

    conn.close()
def calculate_total():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()[0]

    if result:
        print(f"\nTotal Expenses: ₹{result}")
    else:
        print("No expenses recorded.")

    conn.close()

def edit_expense():
    expense_id = input("Enter ID of expense to edit: ")

    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_category = input("Enter new category: ")

    while True:
        try:
            new_amount = float(input("Enter new amount: "))
            break
        except ValueError:
            print("Enter valid number.")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET date = ?, category = ?, amount = ?
        WHERE id = ?
    """, (new_date, new_category, new_amount, expense_id))

    conn.commit()

    if cursor.rowcount == 0:
        print("No expense found with that ID.\n")
    else:
        print("Expense updated successfully.\n")

    conn.close()
def delete_expense():
    expense_id = input("Enter ID of expense to delete: ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("No expense found with that ID.\n")
    else:
        print("Expense deleted successfully.\n")

    conn.close()

def search_by_category():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    category = input("Enter category to search: ")

    cursor.execute(
        "SELECT * FROM expenses WHERE category = ?",
        (category,)
    )

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No expenses found.")

    conn.close()
def monthly_summary():
    month_input = input("Enter month (YYYY-MM): ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE date LIKE ?
    """, (month_input + "%",))

    result = cursor.fetchone()
    conn.close()

    total = result[0]

    if total is None:
        print("No expenses found for that month.\n")
    else:
        print(f"Total expense for {month_input}: {total}\n")

def category_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses found.\n")
        return

    print("\nCategory-wise Summary:")
    print("-" * 30)

    for row in rows:
        print(f"{row[0]} : {row[1]}")

    print()

while True:
    print("==== Welcome to Expense Tracker ====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Category-wise Total")
    print("5. Edit Expense")
    print("6. Delete Expense")

    print("7. Search by Category")
    print("8. Monthly Summary")
    print("9. Category Summary")
    print("10. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        calculate_total()
    elif choice == "4":
        category_total()
    elif choice == "5":
        edit_expense()
    elif choice == "6":
        delete_expense()

    elif choice == "7":
        search_by_category()

    elif choice == "8":
        monthly_summary()
    elif choice == "9":
        category_summary()
    elif choice == "10":
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Try again!!!1")



