import mysql.connector
from datetime import date

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='',
    database='bank'
)

cursor = conn.cursor()


# -----------------------   CREATING ACCOUNT AND ADDING CUSTOMERS   -------------------------------------------------


def create_account():
    nic = int(input("Enter customer NIC : "))
    name = input("Enter customer name : ")
    city = input("Enter customer city : ")
    branch_code = int(input("Enter branch code : "))
    data = [nic, name, city, branch_code]

    cursor.execute("select nic from customer")
    result = cursor.fetchall()
    list1 = []
    for i in result:
        list1.append(i[0])
    if nic in list1:
        print("\nCustomer already exist")
    else:
        query = ("insert into customer"
                 "(nic,name,city,branch_code)"
                 "values(%s,%s,%s,%s)")
        cursor.execute(query, data)
        conn.commit()

    data2 = [name, nic]
    query2 = "select customer_id from customer where name =" "%s" " and " "nic =" "%s"
    cursor.execute(query2, data2)
    customer = cursor.fetchall()
    new = customer[0][0]
    conn.commit()

    typ = int(input("\nSavings = 1\nCurrent = 2\nFixed deposit = 3\n\nEnter account type: "))
    if typ == 1:
        typ = "savings"
    elif typ == 2:
        typ = "current"
    elif typ == 3:
        typ = "fixed"
    else:
        print("Invalid choice")

    balance = int(input("Enter amount: "))
    data3 = [typ, balance, branch_code, new]
    query3 = ("INSERT INTO account "
              "(type, balance, branch_code, customer_id) "
              "VALUES (%s, %s, %s, %s)")
    cursor.execute(query3, data3)
    conn.commit()


# ---------------------------     SHOW CUSTOMERS    -------------------------------------------------------------------

def show_customer():
    query = "select customer_id, name, nic from customer"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        print(i)


# -----------------------------     SHOW ACCOUNTS      ----------------------------------------------------------------


def show_account():
    query = "select acc_no, customer_id from account"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        print(i)


# ----------------------    REMOVE ACCOUNTS AND CUSTOMERS      --------------------------------------------------------

def delete_account():
    show_account()
    acc_no = int(input("Enter account number : "))
    data0 = [acc_no]
    query1 = "delete from transaction where acc_no = " "%s"
    query2 = "delete from account where acc_no = " "%s"
    query3 = "select customer_id from account where acc_no = " "%s"
    query4 = "delete from customer where customer_id = " "%s"

    cursor.execute(query3, data0)
    result = cursor.fetchall()
    customer_id = result[0][0]
    data1 = [customer_id]
    print(data1)
    conn.commit()

    cursor.execute(query1, data0)
    conn.commit()

    cursor.execute(query2, data0)
    conn.commit()

    cursor.execute(query4, data1)
    conn.commit()


# -------------------------------   CHECK ACCOUNT BALANCE   -----------------------------------------------------------

def check_balance():
    acc_no = int(input("Enter account number : "))
    data = [acc_no]
    query1 = "select balance from account where acc_no =" "%s"
    cursor.execute(query1, data)
    result = cursor.fetchall()
    acc_ball = result[0][0]
    print("Account balance = ", acc_ball)
    conn.commit()


# --------------------------    DOING TRANSACTIONS AND UPDATING ACCOUNT BALANCE     ------------------------------------


def transactions():
    typ = int(input("Deposit = 1\nWithdraw = 2\n\nEnter transaction type : "))
    if typ == 1:
        typ = "deposit"
    elif typ == 2:
        typ = "withdraw"
    else:
        print("Invalid input")
    amount = int(input("Enter amount : "))
    today = date.today()
    show_account()
    account_no = int(input("Enter account number : "))

    data0 = [account_no]
    query1 = "select customer_id from account where acc_no =" "%s"
    cursor.execute(query1, data0)
    result = cursor.fetchall()
    customer_id = result[0][0]
    conn.commit()

    data = [typ, amount, today, account_no, customer_id]
    query2 = ("INSERT INTO transaction "
              "(type, amount, date, acc_no, customer_id)"
              "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query2, data)
    conn.commit()

    query3 = "select balance from account where acc_no=" "%s"
    cursor.execute(query3, data0)
    result2 = cursor.fetchall()
    balance = result2[0][0]
    conn.commit()

    if typ == "deposit":
        new_bal = balance + amount
        data2 = [new_bal, account_no]
        query4 = "UPDATE account SET balance = " "%s" " where acc_no =" "%s"
        cursor.execute(query4, data2)
        conn.commit()

    elif typ == "withdraw":
        new_bal = balance - amount
        data2 = [new_bal, account_no]
        query4 = "UPDATE account SET balance = " "%s" " where acc_no =" "%s"
        cursor.execute(query4, data2)
        conn.commit()


# -----------------------------     TRANSACTION HISTORY     ------------------------------------------------------------


def trans_history():
    acc_no = int(input("Enter account number : "))
    data0 = [acc_no]

    query = "select customer_id from transaction where acc_no = " "%s"
    cursor.execute(query, data0)
    result = cursor.fetchall()
    customer_id = [result[0][0]]

    query2 = "select name from customer where customer_id = " "%s"
    cursor.execute(query2, customer_id)
    result2 = cursor.fetchall()
    name = [result2[0][0]]
    conn.commit()

    query3 = "select trans_id, type, date, amount, customer_id from transaction where acc_no = " "%s"
    cursor.execute(query3, data0)
    result3 = cursor.fetchall()
    conn.commit()
    print(result3, name)


# --------------------    HANDLING LOAN TABLE     ----------------------------------------------------------------------

def loan():
    show_customer()
    customer_id = int(input("Enter customer ID : "))
    amount = int(input("Enter loan amount : "))
    typ_id = int(input("\nPersonal loan = 1\nHousing loan = 2\nBusiness loan = 3\nVehicle loan = 4\nEducation loan = "
                       "5\n\nEnter loan type : "))
    data0 = [customer_id]
    query1 = "select branch_code from customer where customer_id =" "%s"
    cursor.execute(query1, data0)
    result = cursor.fetchall()
    conn.commit()

    branch_code = result[0][0]
    data1 = [amount, branch_code, customer_id, typ_id]
    query2 = ("insert into loan"
              "(amount, branch_code, customer_id, type_id)"
              "values(%s, %s, %s, %s)")
    cursor.execute(query2, data1)
    conn.commit()


# ---------------------------------     SHOW LOANS      ---------------------------------------------------------------

def show_loans():
    customer_id = int(input("Enter customer ID : "))
    data = [customer_id]
    query = "select loan_id,amount from loan where customer_id =" "%s"
    cursor.execute(query, data)
    result = cursor.fetchall()
    print(result)


# -------------------------     RESET SYSTEM    -----------------------------------------------------------------------

def reset():
    cursor.execute("truncate table transaction")
    cursor.execute("truncate table loan")
    cursor.execute("delete from account")
    cursor.execute("delete from customer")
    conn.commit()


# -----------------------------     CALCULATE ACCOUNT INTEREST     ----------------------------------------------------

def dinterest():
    query = "select rate, acc_type from dinterest where type_id = 1 or type_id = 2 or type_id = 3 "
    cursor.execute(query)
    result = cursor.fetchall()
    savings_rate = result[0][0]
    current_rate = result[1][0]
    fixed_rate = result[2][0]

    cursor.execute("select acc_no, type, balance from account")
    result2 = cursor.fetchall()
    savings = []
    current = []
    fixed = []
    for i in result2:
        if i[1] == "savings":
            savings.append([i[0], i[2]])
        elif i[1] == "current":
            current.append([i[0], i[2]])
        elif i[1] == "fixed":
            fixed.append([i[0], i[2]])

    for j in savings:
        amount = j[1]
        acc_no = j[0]
        interest = (amount / 100) * savings_rate
        new_amount = amount + interest
        data = [new_amount, acc_no]
        query3 = "update account set balance=" "%s" "where acc_no =" "%s"
        cursor.execute(query3, data)
        conn.commit()

    for m in current:
        amount = m[1]
        acc_no = m[0]
        interest = (amount / 100) * current_rate
        new_amount = amount + interest
        data = [new_amount, acc_no]
        query3 = "update account set balance=" "%s" "where acc_no =" "%s"
        cursor.execute(query3, data)
        conn.commit()

    for n in fixed:
        amount = n[1]
        acc_no = n[0]
        interest = (amount / 100) * fixed_rate
        new_amount = amount + interest
        data = [new_amount, acc_no]
        query3 = "update account set balance=" "%s" "where acc_no =" "%s"
        cursor.execute(query3, data)
        conn.commit()


# -------------------------------   LOAN INTEREST CALCULATE     -------------------------------------------------------

def loan_interest():
    query = "select * from interest"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    personal_rate = [result[0][2], result[0][0]]
    housing_rate = [result[1][2], result[1][0]]
    business_rate = [result[2][2], result[2][0]]
    vehicle_rate = [result[3][2], result[3][0]]
    education_rate = [result[4][2], result[4][0]]

    query2 = "select amount, type_id ,loan_id from loan"
    cursor.execute(query2)
    result2 = cursor.fetchall()
    conn.commit()

    for i in result2:
        if i[1] == personal_rate[1]:
            interest = (i[0]/100)*personal_rate[0]
            new_amount = i[0] + interest
            data2 = [new_amount, i[2]]
            query3 = "update loan set amount=" "%s" "where loan_id =" "%s"
            cursor.execute(query3, data2)
            conn.commit()

    for i in result2:
        if i[1] == housing_rate[1]:
            interest = (i[0]/100)*housing_rate[0]
            new_amount = i[0] + interest
            data2 = [new_amount, i[2]]
            query3 = "update loan set amount=" "%s" "where loan_id =" "%s"
            cursor.execute(query3, data2)
            conn.commit()

    for i in result2:
        if i[1] == business_rate[1]:
            interest = (i[0]/100)*business_rate[0]
            new_amount = i[0] + interest
            data2 = [new_amount, i[2]]
            query3 = "update loan set amount=" "%s" "where loan_id =" "%s"
            cursor.execute(query3, data2)
            conn.commit()

    for m in result2:
        if m[1] == vehicle_rate[1]:
            interest = (m[0]/100)*vehicle_rate[0]
            new_amount = m[0] + interest
            data2 = [new_amount, m[2]]
            query3 = "update loan set amount=" "%s" "where loan_id =" "%s"
            cursor.execute(query3, data2)
            conn.commit()

        for i in result2:
            if i[1] == education_rate[1]:
                interest = (i[0] / 100) * education_rate[0]
                new_amount = i[0] + interest
                data2 = [new_amount, i[2]]
                query3 = "update loan set amount=" "%s" "where loan_id =" "%s"
                cursor.execute(query3, data2)
                conn.commit()

# --------------------     CLI SETTINGS    ----------------------------------------------------------------------------


while 1 == 1:
    choice = int(input("\nAccount settings = 1\nTransaction settings = 2\nLoan settings = 3\nCalculate interest = "
                       "4\nReset system = 5\n\nEnter"
                       "selection here : "))

    if choice == 1:
        select = int(input("\nShow customers = 1\nShow accounts = 2\nCheck balance = 3\nCreate account = 4\nDelete "
                           "account = 5\n\nEnter"
                           "selection here : "))
        if select == 1:
            show_customer()
        elif select == 2:
            show_account()
        elif select == 3:
            check_balance()
        elif select == 4:
            create_account()
        elif select == 5:
            delete_account()
    elif choice == 2:
        select = int(input("\nDo a transaction = 1\nShow transaction history = 2\n\nEnter selection here : "))
        if select == 1:
            transactions()
        elif select == 2:
            trans_history()
    elif choice == 3:
        select = int(input("\nShow loans = 1\nUpdate loans = 2\nEnter selection here : "))
        if select == 1:
            show_loans()
        elif select == 2:
            loan()
    elif choice == 4:
        select = int(input("Calculate deposit interest = 1\nCalculate loan interest = 2\n\nEnter selection here : "))
        if select == 1:
            dinterest()
        elif select == 2:
            loan_interest()
        else:
            print("Invalid selection")
    elif choice == 5:
        reset()
    else:
        print("Invalid choice")
