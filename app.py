from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'xyz123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'broy9501'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'expenseTracker'

mysql = MySQL(app) # Initialise MySQL connection

# Login Route
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
         # Retrieve form values
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        users = cursor.fetchone()

        # Verify the hashed password
        if users and bcrypt.check_password_hash(users['password'], password):
            session['loggedin'] = True
            session['userID'] = users['userID']
            session['email'] = users['email']
            return redirect(url_for('expense'))
        else:
            message = 'Incorrect username or password'

    return render_template('loginSignup.html', msg = message)

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('emailSign')
        password = request.form.get('passwordSign')
        passwordConfirm = request.form.get('passwordConfirm')

        print(f"[DEBUG] Received: Name={name}, Email={email}")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("[DEBUG] Email already exists.")
            return render_template('loginSignup.html', msg='Username already exists!')

        # Validate fields
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            print("[DEBUG] Invalid email format.")
            return render_template('loginSignup.html', msg='Invalid email address!')
        elif not password or not email or not name:
            print("[DEBUG] Missing required fields.")
            return render_template('loginSignup.html', msg='Please fill out the form!')
        elif password != passwordConfirm:
            print("[DEBUG] Passwords do not match.")
            return render_template('loginSignup.html', msg='Passwords not matched!')

        try:
            hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
            print(f"[DEBUG] Hashed password: {hashedPassword}")

            cursor.execute('INSERT INTO users (email, name, password) VALUES (%s, %s, %s)', (email, name, hashedPassword))
            mysql.connection.commit()
            print("[DEBUG] Registration successful.")

            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            print(f"[ERROR] MySQL error: {e}")
            return render_template('loginSignup.html', msg='Error during registration.')
    
    return render_template('loginSignup.html', msg=message)


@app.route('/income', methods=['POST', 'GET'])
def income():
    message = ""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        incomeTitle = request.form.get('incomeTitle')
        incomeAmount = request.form.get('incomeAmount')
        incomeDate = request.form.get('incomeDate')
        incomeType = request.form.get('incomeType')
        incomeReference = request.form.get('incomeReference')
        userid = session['userID']

        print(f"INCOME Data Received")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT into expense (title, amount, incomeData, incomeType, reference, userid) VALUES (%s, %s, %s, %s, %s, %s)", (incomeTitle, incomeAmount, incomeDate, incomeType, incomeReference, userid))

        cursor.execute("SELECT totalIncome FROM totalexpense WHERE userid = %s", (userid,))
        existingIncome = cursor.fetchone()

        if existingIncome:
            cursor.execute("UPDATE totalexpense SET totalIncome = totalIncome + %s WHERE userid = %s", (incomeAmount, userid))
        else:
            cursor.execute("INSERT INTO totalexpense (userid, totalIncome) VALUES (%s, %s)", (userid, incomeAmount))


        mysql.connection.commit()
        print(f"Income Data Inserted and Total Income Updated")

        return redirect(url_for('expense'))
    return render_template('expense.html')

@app.route('/expense', methods=['POST', 'GET'])
def expense():
    message = ""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    userid = session['userID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        expenseTitle = request.form.get('expenseTitle')
        expenseAmount = float(request.form.get('expenseAmount'))
        expenseDate = request.form.get('expenseDate')
        expenseType = request.form.get('expenseType')
        expenseReference = request.form.get('expenseReference')

        print(f"EXPENSE Data Received")

        cursor.execute("INSERT INTO expense (title, amount, incomeData, incomeType, reference, userid) VALUES (%s, %s, %s, %s, %s, %s)",
                       (expenseTitle, -expenseAmount, expenseDate, expenseType, expenseReference, userid))
        
        cursor.execute("SELECT totalIncome FROM totalexpense WHERE userid = %s", (userid,))
        existingIncome = cursor.fetchone()

        if existingIncome:
            cursor.execute("UPDATE totalexpense SET totalIncome = totalIncome - %s WHERE userid = %s", (expenseAmount, userid))
        else:
            cursor.execute("INSERT INTO totalexpense (userid, totalIncome) VALUES (%s, %s)", (userid, -expenseAmount))

        mysql.connection.commit()
        print(f"Expense Data Inserted and Total Income Updated")

        return redirect(url_for('expense'))

    cursor.execute("SELECT * FROM expense WHERE userid = %s", (userid,))
    transactions = cursor.fetchall()
    negativeTransactions = [t for t in transactions if float(t['amount']) < 0]
    sumNegativeTransactions = sum(float(t['amount']) for t in negativeTransactions)

    cursor.execute("SELECT totalIncome FROM totalexpense WHERE userid = %s", (userid,))
    totalIncome = cursor.fetchone()

    cursor.execute("""
    SELECT incomeType, SUM(ABS(amount)) as totalAmount
    FROM expense
    WHERE userid = %s AND amount < 0
    GROUP BY incomeType
    """, (userid,))
    spendingByType = cursor.fetchall()

    labels = [row['incomeType'] for row in spendingByType]
    data = [float(row['totalAmount']) for row in spendingByType]

    cursor.execute("SELECT currencySigns From users WHERE userid = %s", (userid,))
    currencySign = cursor.fetchone()

    return render_template('expense.html', transactions=transactions, sumNegativeTransactions=sumNegativeTransactions, totalIncome=totalIncome, chartLabels=labels,
    chartData=data, currencySign=currencySign)


@app.route('/updateSettings', methods=['POST', 'GET'])
def updateSettings():
    updateEmail = request.form.get('updateEmail')
    updatePassword = request.form.get('updatePassword')
    updateCurrencySign = request.form.get('updateCurrencySign')

    # Get current user from session
    currentEmail = session.get('email')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (currentEmail,))
    currentUser = cursor.fetchone()

    if not currentUser:
        return "User not found", 404

    # Use the updated value or fallback to current
    email = updateEmail or currentUser['email']
    password = bcrypt.generate_password_hash(updatePassword).decode('utf-8') if updatePassword else currentUser['password']
    currencySign = updateCurrencySign or currentUser['currencySigns']

    cursor.execute("""
        UPDATE users
        SET email = %s, password = %s, currencySigns = %s
        WHERE email = %s
    """, (email, password, currencySign, currentEmail))

    mysql.connection.commit()

    # Update session in case email changed
    session['email'] = email

    return redirect(url_for('expense'))


# @app.route('/testdb')
# def testdb():
#     try:
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT 1')
#         return 'Database connected!'
#     except Exception as e:
#         return f'Database error: {e}'


if __name__ == '__main__':
    app.run(debug=True)
