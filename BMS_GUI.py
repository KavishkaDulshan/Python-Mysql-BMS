import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date

# Database connection setup 
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='',
    database='bank'
)

cursor = conn.cursor()

# Tkinter root window setup
root = tk.Tk()
root.title("Banking System")
root.geometry("600x400")

# Functions for database operations
def create_account():
    try:
        nic = simpledialog.askinteger("Input", "Enter customer NIC")
        name = simpledialog.askstring("Input", "Enter customer name")
        city = simpledialog.askstring("Input", "Enter customer city")
        branch_code = simpledialog.askinteger("Input", "Enter branch code")

        cursor.execute("SELECT nic FROM customer WHERE nic = %s", (nic,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Error", "Customer already exists")
            return

        cursor.execute("INSERT INTO customer (nic, name, city, branch_code) VALUES (%s, %s, %s, %s)",
                       (nic, name, city, branch_code))
        conn.commit()

        cursor.execute("SELECT customer_id FROM customer WHERE nic = %s", (nic,))
        customer = cursor.fetchone()
        customer_id = customer[0]

        account_types = {1: "savings", 2: "current", 3: "fixed"}
        typ = simpledialog.askinteger("Input", "Savings = 1\nCurrent = 2\nFixed deposit = 3\n\nEnter account type")
        if typ not in account_types:
            messagebox.showerror("Error", "Invalid choice")
            return

        balance = simpledialog.askinteger("Input", "Enter amount")
        cursor.execute("INSERT INTO account (type, balance, branch_code, customer_id) VALUES (%s, %s, %s, %s)",
                       (account_types[typ], balance, branch_code, customer_id))
        conn.commit()

        messagebox.showinfo("Success", "Account created successfully")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        conn.rollback()

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter the correct values.")

def show_customers():
    try:
        cursor.execute("SELECT customer_id, name, nic FROM customer")
        result = cursor.fetchall()
        output = "\n".join(f"ID: {customer[0]}, Name: {customer[1]}, NIC: {customer[2]}" for customer in result)
        messagebox.showinfo("Customers", output)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def show_accounts():
    try:
        cursor.execute("SELECT acc_no, customer_id FROM account")
        result = cursor.fetchall()
        output = "\n".join(f"Account No: {account[0]}, Customer ID: {account[1]}" for account in result)
        messagebox.showinfo("Accounts", output)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def delete_account():
    show_accounts()
    try:
        acc_no = simpledialog.askinteger("Input", "Enter account number")

        cursor.execute("SELECT customer_id FROM account WHERE acc_no = %s", (acc_no,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Account does not exist.")
            return

        customer_id = result[0]

        cursor.execute("DELETE FROM transaction WHERE acc_no = %s", (acc_no,))
        cursor.execute("DELETE FROM account WHERE acc_no = %s", (acc_no,))
        cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
        conn.commit()
        messagebox.showinfo("Success", "Account and associated customer deleted successfully")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        conn.rollback()

def check_balance():
    try:
        acc_no = simpledialog.askinteger("Input", "Enter account number")

        cursor.execute("SELECT balance FROM account WHERE acc_no = %s", (acc_no,))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Balance", f"Account balance = {result[0]}")
        else:
            messagebox.showerror("Error", "Account does not exist.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def transactions():
    try:
        typ = simpledialog.askinteger("Input", "Deposit = 1\nWithdraw = 2\n\nEnter transaction type")
        if typ not in [1, 2]:
            messagebox.showerror("Error", "Invalid input")
            return

        typ_str = "deposit" if typ == 1 else "withdraw"
        amount = simpledialog.askinteger("Input", "Enter amount")
        today = date.today()
        show_accounts()
        acc_no = simpledialog.askinteger("Input", "Enter account number")

        cursor.execute("SELECT customer_id, balance FROM account WHERE acc_no = %s", (acc_no,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Account does not exist.")
            return

        customer_id, balance = result

        cursor.execute("INSERT INTO transaction (type, amount, date, acc_no, customer_id) VALUES (%s, %s, %s, %s, %s)",
                       (typ_str, amount, today, acc_no, customer_id))
        new_balance = balance + amount if typ_str == "deposit" else balance - amount

        cursor.execute("UPDATE account SET balance = %s WHERE acc_no = %s", (new_balance, acc_no))
        conn.commit()

        messagebox.showinfo("Success", "Transaction successful")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        conn.rollback()

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter the correct values.")

def trans_history():
    try:
        acc_no = simpledialog.askinteger("Input", "Enter account number")

        cursor.execute("SELECT t.trans_id, t.type, t.date, t.amount, c.name FROM transaction t "
                       "JOIN customer c ON t.customer_id = c.customer_id "
                       "WHERE t.acc_no = %s", (acc_no,))
        result = cursor.fetchall()
        output = "\n".join(f"ID: {record[0]}, Type: {record[1]}, Date: {record[2]}, Amount: {record[3]}, Customer: {record[4]}" for record in result)
        messagebox.showinfo("Transaction History", output)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def loan():
    show_customers()
    try:
        customer_id = simpledialog.askinteger("Input", "Enter customer ID")
        amount = simpledialog.askinteger("Input", "Enter loan amount")
        loan_types = {1: "Personal", 2: "Housing", 3: "Business", 4: "Vehicle", 5: "Education"}
        typ_id = simpledialog.askinteger("Input", "Personal loan = 1\nHousing loan = 2\nBusiness loan = 3\nVehicle loan = 4\nEducation loan = 5\n\nEnter loan type")
        if typ_id not in loan_types:
            messagebox.showerror("Error", "Invalid loan type")
            return

        cursor.execute("SELECT branch_code FROM customer WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Customer does not exist.")
            return

        branch_code = result[0]

        cursor.execute("INSERT INTO loan (amount, branch_code, customer_id, type_id) VALUES (%s, %s, %s, %s)",
                       (amount, branch_code, customer_id, typ_id))
        conn.commit()
        messagebox.showinfo("Success", "Loan granted successfully")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        conn.rollback()

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter the correct values.")

def show_loans():
    try:
        customer_id = simpledialog.askinteger("Input", "Enter customer ID")

        cursor.execute("SELECT loan_id, amount FROM loan WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchall()
        output = "\n".join(f"Loan ID: {loan[0]}, Amount: {loan[1]}" for loan in result)
        messagebox.showinfo("Loans", output)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def reset():
    try:
        cursor.execute("TRUNCATE TABLE transaction")
        cursor.execute("TRUNCATE TABLE loan")
        cursor.execute("DELETE FROM account")
        cursor.execute("DELETE FROM customer")
        conn.commit()
        messagebox.showinfo("Success", "System reset successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        conn.rollback()

# GUI Components
frame = tk.Frame(root)
frame.pack(pady=20)

btn_show_customers = tk.Button(frame, text="Show Customers", command=show_customers)
btn_show_customers.grid(row=0, column=0, padx=10, pady=10)

btn_show_accounts = tk.Button(frame, text="Show Accounts", command=show_accounts)
btn_show_accounts.grid(row=0, column=1, padx=10, pady=10)

btn_check_balance = tk.Button(frame, text="Check Balance", command=check_balance)
btn_check_balance.grid(row=0, column=2, padx=10, pady=10)

btn_create_account = tk.Button(frame, text="Create Account", command=create_account)
btn_create_account.grid(row=1, column=0, padx=10, pady=10)

btn_delete_account = tk.Button(frame, text="Delete Account", command=delete_account)
btn_delete_account.grid(row=1, column=1, padx=10, pady=10)

btn_transactions = tk.Button(frame, text="Do Transaction", command=transactions)
btn_transactions.grid(row=2, column=0, padx=10, pady=10)

btn_trans_history = tk.Button(frame, text="Transaction History", command=trans_history)
btn_trans_history.grid(row=2, column=1, padx=10, pady=10)

btn_loan = tk.Button(frame, text="Grant Loan", command=loan)
btn_loan.grid(row=3, column=0, padx=10, pady=10)

btn_show_loans = tk.Button(frame, text="Show Loans", command=show_loans)
btn_show_loans.grid(row=3, column=1, padx=10, pady=10)

btn_reset = tk.Button(frame, text="Reset System", command=reset)
btn_reset.grid(row=4, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
