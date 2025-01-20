
import mysql.connector as ms

# Establish connection
mycom = ms.connect(
    host="127.0.0.1",
    user="dbadmin",
    password="dbadmin123",
    database="SIMPLE_BANK"
)
def sql_connector_check(mycom):
    if mycom.is_connected():
        print("Connected successfully")
    else:
        print("Some issue occurred")

# Function to show login screen
def show_login():
    print("=================")
    print("Simple Banking LOGIN")
    print("=================")

# Function to show title
def show_title():
    print("=================")
    print("Welcome to Simple Bank")
    print("=================")

# Main menu
def show_main_menu():
    show_title()
    print("1. Customer Management")
    print("2. Account Management")
    print("3. Exit")

# Customer management menu
def show_customer_mgmt_menu():
    show_title()
    print("1. Create Customer")
    print("2. Update Customer")
    print("3. List Customers")
    print("4. Exit")

# Account management menu
def show_account_mgmt_menu():
    show_title()
    print("1. Open Account")
    print("2. Freeze Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check Balance")
    print("6. Exit")

    global login_user_name

def login_info_chk():
    global login_user_name
    login_user_name = input("Enter your user name: ")
    w = input("Enter your password: ")

    def authenticate(username, password):
        try:
            conn = mycom
            my_cursor = conn.cursor()
            query = "SELECT * FROM user WHERE user_name=%s AND passwd=%s"
            my_cursor.execute(query, (username, password))
            users = my_cursor.fetchall()
            my_cursor.close()
            return users if users else None
        except:
            print("An error occurred:")
            return None

    check = authenticate(login_user_name, w)
    if check is None:
        print('Invalid credentials')
        return False
    else:
        return True
def account_exists(account_no):
    try:
        my_cursor = mycom.cursor()
        query = "SELECT * FROM ACCOUNT WHERE ACCOUNT_NO = %s"
        my_cursor.execute(query, (account_no,))
        account = my_cursor.fetchone()
        return True if account else False
    except:
        print("An error occurred:")
        return False
    finally:
        my_cursor.close()
def check_account_status(account_no):
    try:
        my_cursor = mycom.cursor()
        query = "SELECT ACCOUNT_STATUS FROM ACCOUNT WHERE ACCOUNT_NO = %s"
        my_cursor.execute(query, (account_no,))
        result = my_cursor.fetchone()

        if result:
            return True if result[0] == "Active" else False
        else:
            print(f"No account found with account number {account_no}")
            return False
    except:
        print("An error occurred")
        return False
    finally:
        my_cursor.close()

# Get max customer ID from the database
def max_customer_id_in_db(table_name: str):
    try:
        my_cursor = mycom.cursor()
        query = f"SELECT MAX(ID) FROM {table_name}"
        my_cursor.execute(query)
        max_cust_id_rec = my_cursor.fetchone()
        max_cust_id = 1 if max_cust_id_rec[0] is None else max_cust_id_rec[0] + 1
    except :
        print("An error occurred")
    finally:
        my_cursor.close()
    return max_cust_id

# Create customer input and insert into the database
def create_customer_input():
    print("====== CREATE CUSTOMER ========")
    ID = max_customer_id_in_db('CUSTOMER')
    if login_user_name.lower() == "admin":
        bank_code = "KCB"
    else:
        bank_code = "IND"
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email_address = input("Email Address: ").strip()
    customer_identifier = input("Customer Identifier (Passport No/Aadhar No): ").strip()
    created_by = login_user_name
    customer_no = max_customer_id_in_db('CUSTOMER')

    try:
        my_cursor = mycom.cursor()
        insert_query = """
            INSERT INTO CUSTOMER (ID, BANK_CODE, CUSTOMER_NO, FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, CUSTOMER_IDENTIFIER, CREATED_DATE, CREATED_BY)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        values = (ID, bank_code, customer_no, first_name, last_name, email_address, customer_identifier, created_by)
        my_cursor.execute(insert_query, values)
        mycom.commit()
        print("Customer created successfully!")
        print(f"Customer Number is :{ID}")
        l = input("press any key to continue......")
    except :
        print("An error occurred")
        l = input("press any key to continue......")
    finally:
        my_cursor.close()
def customer_exists(customer_no):
    try:
        my_cursor = mycom.cursor()
        query = "SELECT * FROM CUSTOMER WHERE CUSTOMER_NO = %s"
        my_cursor.execute(query, (customer_no,))
        customer = my_cursor.fetchone()
        if customer is None:
            return False
        else:
            return True
    except :
        print("An error occurred")
    finally:
        my_cursor.close()
def update_customer():
    print("====== UPDATE CUSTOMER ========")
    customer_no = input("Enter the customer number to update: ").strip()
    if customer_exists(customer_no) == False:
        print("Customer does not exist")
    else:
        try:
            my_cursor = mycom.cursor()
            query = "SELECT * FROM CUSTOMER WHERE CUSTOMER_NO = %s"
            my_cursor.execute(query, (customer_no,))
            customer = my_cursor.fetchone()
            first_name = input("First Name: ").strip() or customer[3]
            last_name = input("Last Name: ").strip() or customer[4]
            email_address = input("Email Address: ").strip() or customer[5]
            customer_identifier = input("Customer Identifier: ").strip() or customer[6]

            # Prepare update query
            update_query = """
                UPDATE CUSTOMER 
                SET FIRST_NAME = %s, LAST_NAME = %s, EMAIL_ADDRESS = %s, CUSTOMER_IDENTIFIER = %s
                WHERE CUSTOMER_NO = %s
            """
            update_values = (first_name, last_name, email_address, customer_identifier, customer_no)

            # Execute update
            my_cursor.execute(update_query, update_values)
            mycom.commit()
            print("Customer updated successfully!")

        except :
            print("An error occurred")
            l=input("Press any key to continue......")
        finally:
            my_cursor.close()


def list_customer():
    try:
        cur = mycom.cursor()
        cur.execute("SELECT CUSTOMER_NO, FIRST_NAME FROM CUSTOMER;")
        data = cur.fetchall()
        for i in data:
            print(i)
    except :
        print("An error occurred")
    finally:
        cur.close()

def insert_account_data():
    ID = max_customer_id_in_db('ACCOUNT')
    customer_no = input("Customer Number: ").strip()
    account_no = input("Account Number: ").strip()
    account_type = input("Account Type (SAV/CHK): ").strip().upper()
    currency = "INR"
    account_status = "Active"
    created_by = login_user_name

    try:
        my_cursor = mycom.cursor()
        insert_query = """
            INSERT INTO ACCOUNT (ID, CUSTOMER_NO, ACCOUNT_NO, Account_TYPE, CURRENCY, ACCOUNT_STATUS, CREATED_DATE, CREATED_BY)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        values = (ID, customer_no, account_no, account_type, currency, account_status, created_by)
        my_cursor.execute(insert_query, values)
        mycom.commit()
        print("Account created successfully!")
        l = input("press any key to continue......")
    except:
        print("An error occurred")
        l = input("press any key to continue......")
    finally:
        my_cursor.close()

def freeze_account():
    f2 = input("Enter the account number to freeze: ")
    try:
        cur = mycom.cursor()
        query = """
            UPDATE ACCOUNT
            SET ACCOUNT_STATUS = %s
            WHERE ACCOUNT_NO = %s
        """
        # Set account status to "Inactive"
        cur.execute(query, ('Inactive', f2))
        mycom.commit()
        print("Account status updated to 'Inactive' successfully.")
    except:
        print("An error occurred")
        l = input("press any key to continue......")
    finally:
        cur.close()

def deposit(account_no):
    ID = max_customer_id_in_db("TRANSACTION")
    amount = float(input("Amount: "))
    credit_debit_ind = "CR"
    trans_by = login_user_name

    try:
        my_cursor = mycom.cursor()
        insert_query = """
            INSERT INTO TRANSACTION (ID, ACCOUNT_NO, AMOUNT, CREDIT_DEBIT_IND, TRANS_DATE, TRANS_BY)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """
        values = (ID, account_no, amount, credit_debit_ind, trans_by)
        my_cursor.execute(insert_query, values)
        mycom.commit()
        print("Successfully deposited !")
        l = input("enter any key to continue.........")
    except :
        print("An error occurred")
        l = input("press any key to continue......")
    finally:
        my_cursor.close()

def check_balance(account_no):
    try:
        my_cursor = mycom.cursor()

        chk_dep = """
            SELECT SUM(AMOUNT)
            FROM TRANSACTION
            WHERE ACCOUNT_NO = %s AND CREDIT_DEBIT_IND = 'CR';
        """
        chk_withdraw = """
            SELECT SUM(AMOUNT)
            FROM TRANSACTION
            WHERE ACCOUNT_NO = %s AND CREDIT_DEBIT_IND = 'DR';
        """

        my_cursor.execute(chk_dep, (account_no,))
        deposit_sum = my_cursor.fetchone()[0] or 0

        my_cursor.execute(chk_withdraw, (account_no,))
        withdrawal_sum = my_cursor.fetchone()[0] or 0

        balance = deposit_sum - withdrawal_sum

        print(f"The current balance for account {account_no} is: {balance:.2f}")
        l = input("enter any key to continue.........")
    except:
        print("An error occurred")
    finally:
        my_cursor.close()
def withdraw(account_no):
    ID = max_customer_id_in_db("TRANSACTION")
    amount = float(input("Amount: "))
    credit_debit_ind = "DR"
    trans_by = login_user_name
    try:
        my_cursor = mycom.cursor()
        insert_query = """
            INSERT INTO TRANSACTION (ID, ACCOUNT_NO, AMOUNT, CREDIT_DEBIT_IND, TRANS_DATE, TRANS_BY)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """
        values = (ID, account_no, amount, credit_debit_ind, trans_by)
        my_cursor.execute(insert_query, values)
        mycom.commit()
        print("Successful Withdrawal!.")
        l = input("press any key to continue.........")
    except:
        print("An error occurred")
        l = input("press any key to continue......")
    finally:
        my_cursor.close()

#MAIN
sql_connector_check(mycom)
while True:
    show_login()
    if login_info_chk():
        continue
    else:
        while True:
            show_main_menu()
            choice = input("Choose an option: ")
            if choice == '1':
                while True:
                    show_customer_mgmt_menu()
                    customer_choice = input("Choose an option: ")
                    if customer_choice == '1':
                        create_customer_input()
                    elif customer_choice == '2':
                        update_customer()
                    elif customer_choice == '3':
                        list_customer()
                    elif customer_choice == '4':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '2':
                while True:
                    show_account_mgmt_menu()
                    account_choice = input("Choose an option: ")
                    if account_choice == '1':
                        account_no = input("Enter Account Number: ").strip()
                        if account_exists(account_no):
                            insert_account_data()
                        else:
                            print(f"No account found with account number {account_no}")
                    elif account_choice == '2':
                        freeze_account()
                    elif account_choice == '3':
                        account_no = input("Enter Account Number: ").strip()
                        if account_exists(account_no):
                            if check_account_status(account_no):
                                deposit(account_no)
                            else:
                                print("Cannot check balance for the account as it has been frozen.")
                        else:
                            print("No account found")
                            input("Enter any key to continue.........")
                    elif account_choice == '4':
                        account_no = input("Enter Account Number: ").strip()
                        if account_exists(account_no):
                            if check_account_status(account_no):
                                withdraw(account_no)
                            else:
                                print("Cannot check balance for the account as it has been frozen.")
                        else:
                            print("No account found")
                            input("Press any key to continue.........")
                    elif account_choice == '5':
                        account_no = input("Enter Account Number: ").strip()
                        if account_exists(account_no):
                            if check_account_status(account_no):
                                check_balance(account_no)
                            else:
                                print("Cannot check balance for the account as it has been frozen.")
                        else:
                            print("No account found")
                            input("Press any key to continue.........")
                    elif account_choice == '6':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '3':
                break
            else:
                print("Invalid choice, please try again.")
    break
mycom.close()