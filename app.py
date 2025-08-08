from flask import Flask,request,render_template,redirect,url_for
import datetime
app=Flask(__name__)
users={}
statements={}
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        uname=request.form['username']
        password=request.form['password'] #123
        pin_no=request.form['pin'] #1234
        if uname not in users:
            users[uname]={'password':password,'pin_number':pin_no,'amount':0}
            return redirect(url_for('login'))
        else:
            return 'account already existed'
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        loginUser_name=request.form['username']
        login_password=request.form['password']
        login_pin=request.form['pin']
        if loginUser_name in users:
            stored_password=users[loginUser_name]['password']
            if stored_password==login_password:
                stored_pin=users[loginUser_name]['pin_number']
                if stored_pin==login_pin:
                    return redirect(url_for('dashboard',username=loginUser_name))
                else:
                    return "Pin number is incorrect"
            else:
                return "Password is incorrect"
        else:
             return "Username not found"

    return render_template('login.html')
@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html',username=username)
@app.route('/deposit/<username>',methods=['GET','POST'])
def deposit(username):
    if request.method=='POST':
        deposit_amount=int(request.form['amount'])
        if deposit_amount<0:
            return 'invalid amount'
        elif deposit_amount>5000:
            return 'amount exceeded 5000 pls give less than 50k'
        elif deposit_amount>0 and deposit_amount<=5000:
            balance_amount=users[username]['amount']
            users[username]['amount']=balance_amount+deposit_amount
            deposite_date=datetime.datetime.now()
            data=(deposit_amount,deposite_date)
            if username in statements:
                statements[username]['deposit'].append(data)
            else:
                statements[username]={'deposit':[data]}
            return redirect(url_for('balance',username=username))
        else:
            return 'Invalid data'
    return render_template('deposit.html',username=username)
@app.route('/withdraw/<username>',methods=['GET','POST'])
def withdraw(username):
    
    if request.method=='POST':
        withdraw_amount=int(request.form['withdrawAmount'])
        balance_amount=users[username]['amount']
        if withdraw_amount>balance_amount:
            return f'Amount{withdraw_amount} exceeded than the balance{balance_amount}'
        elif withdraw_amount<=0:
             return f'invalid amount {withdraw_amount}'
        elif withdraw_amount>0 and withdraw_amount<=balance_amount:
            users[username]['amount']=users[username]['amount']-withdraw_amount
            withdraw_date=datetime.datetime.now()
            data=(withdraw_amount,withdraw_date)
            if 'withdraw' in statements[username]:
                statements[username]['withdraw'].append(data)
            else:
                statements[username]['withdraw']=[data]
            return redirect(url_for('balance',username=username))
            # return f'{statements}'
        else:
            return 'invalid data'
    return render_template('withdraw.html',username=username)
@app.route('/balance/<username>')
def balance(username):
    balance_amount=users[username]['amount']
    return render_template('balance.html',balance_amount=balance_amount,username=username)
@app.route('/statementsdata/<username>')
def statementsdata(username):
    if username in statements:
        user_statements=statements[username]
        return render_template('statements.html',user_statements=user_statements,username=username)
    else:
        return 'No Statements Found'
@app.route('/adminlogout')
def logout():
    return redirect(url_for('login'))
@app.route('/accountdelete/<username>')
def accountdelete(username):
    users.pop(username)
    return redirect(url_for('home'))
app.run(debug=True,use_reloader=True)




