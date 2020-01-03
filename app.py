from flask import Flask, render_template, url_for, request, redirect, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from config import Development, Production
from datetime import datetime
from functools import wraps

# create an instance of class Flask called app
app = Flask(__name__)
app.config.from_object(Development)
# app.config.from_object(Production

# create an instance of sqlalchemy
db = SQLAlchemy(app)

from models.Expenses import ExpensesModel
from models.Feeds import FeedsModel
from models.Sheds import ShedsModel
from models.Staffs import StaffsModel
from models.Swines import SwinesModel
from models.Vaccines import VaccinesModel
from models.Auth import AuthModel
from models.Sales import SalesModel


# create tables in our database
@app.before_first_request
def create_tables():
    db.create_all()


@app.before_request
def setg():
    g.user = None
    if session:
        if session['username']:
            g.user = session['username']
        else:
            g.user = None
    else:
        g.user = None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        phone = request.form['phone']
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        confirm_passw = request.form['confirm_passw']
        hashed = AuthModel.generate_hash(passw)

        if passw == confirm_passw:
            if AuthModel.check_email(mail) and AuthModel.check_username(uname):
                flash("Username/Email already exists")
                return render_template("register.html")
            else:
                register = AuthModel(username=uname, email=mail, phone=phone, password=hashed)
                register.insert_records()

                return redirect(url_for("login"))
        else:
            flash("The two passwords do not match!")
            return render_template("register.html")
    return render_template('register.html')

# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        if AuthModel.fetch_by_username(uname):
            if AuthModel.check_password(uname, passw):
                session['username'] = uname
                session['uid'] = AuthModel.fetch_by_username(uname).id
                # session['role'] = 'admin'
                # print(session['role'])
                return redirect(url_for('home'))
        flash("Username does not Exist!")
    return render_template('login.html')


# logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# forgot password
@app.route('/forgot_password')
def forgot_password():
    return render_template('recover.html')


@app.route('/')
@login_required
def home():
    if session:
        print(session['uid'])
        return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sales')
def sales():
    sheds = ShedsModel.fetch_all()
    sales = SalesModel.fetch_all()
    return render_template('sales.html', sheds=sheds, sales=sales)

# new sale
@app.route('/new_sale', methods=['POST'])
def new_sale():
    if request.method == "POST":
        shed_no = request.form['shed_no']
        quantity = request.form['quantity']
        amount = request.form['amount']

        d = datetime.now()

        month = d.month
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October',
                  'November', 'December']
        month = months[month - 1]

        day = d.day
        year = d.year

        date = str(day) + ' ' + month + ' ' + str(year)
        date = str(date)

        this_shed = ShedsModel.fetch_by_shed_no(shed_no)
        print(this_shed.shed_no)

        if int(quantity) <= int(this_shed.quantity):
            new = SalesModel(shed_no=shed_no, quantity=quantity, amount=amount, date=date)
            new.insert_records()

            print(this_shed.id)
            swine_name = this_shed.swine_name
            initial_quantity = this_shed.quantity
            final_quantity = int(initial_quantity) - int(quantity)

            ShedsModel.update_by_id(id=this_shed.id, shed_no=this_shed.shed_no, swine_name=swine_name, quantity=final_quantity)
        else:
            flash("Enter quantity less than or equal to " + str(this_shed.quantity))

        return redirect(url_for('sales'))


@app.route('/shed')
def shed():
    system_user = AuthModel.fetch_by_username(session['username'])
    sheds = system_user.sheds
    # sheds = ShedsModel.fetch_all()
    return render_template('shed.html', sheds=sheds)

# new shed route
@app.route('/new_shed', methods=['POST'])
def new_shed():
    if request.method == "POST":
        shed_no = request.form['shed_no']
        livestock_name = request.form['swine_name']
        quantity = request.form['quantity']

        if ShedsModel.check_shed(shed_no):
            flash('Shed Already in Use!')
            return redirect(url_for('shed'))
        new = ShedsModel(shed_no=shed_no, swine_name=livestock_name, quantity=quantity, system_user_id=session['uid'])
        new.insert_records()
        return redirect(url_for('shed'))

# update shed information
@app.route('/update_shed/<int:id>', methods=['POST'])
def update_shed(id):
    if request.method == "POST":
        shed_no = request.form['shed_no']
        livestock_name = request.form['swine_name']
        quantity = request.form['quantity']

        ShedsModel.update_by_id(id=id, shed_no=shed_no, swine_name=livestock_name, quantity=quantity)

    return redirect(url_for('shed'))

# delete shed
@app.route('/delete_shed/<int:id>')
def delete_shed(id):
    ShedsModel.delete_by_id(id)
    return redirect(url_for('shed'))

# vaccines route
@app.route('/vaccines/<int:id>')
def vaccines(id):
    this_shed = ShedsModel.fetch_by_id(id)
    return render_template('vaccines.html', this_shed=this_shed)

# new vaccine
@app.route('/new_vaccine/<int:sid>', methods=['POST'])
def new_vaccine(sid):
    if request.method == 'POST':
        vaccine_name = request.form['vaccine_name']
        date_administered = request.form['date_administered']
        next_date = request.form['next_date']
        cost = request.form['cost']

        new = VaccinesModel(vaccine_name=vaccine_name, date_administered=date_administered, next_date=next_date, cost=cost, shed_id=sid)
        new.insert_records()

        expense = ExpensesModel(description='Vaccine', amount=cost, date=date_administered)
        expense.insert_records()
    return redirect(url_for('vaccines', id=sid))


@app.route('/food_history')
def food_history():
    foods = FeedsModel.fetch_all()
    return render_template('food_history.html', foods=foods)

# new food
@app.route('/new_food', methods=['POST'])
def new_food():
    if request.method == 'POST':
        food_name = request.form['food_name']
        price = request.form['price']
        quantity = request.form['quantity']
        total = int(price) * int(quantity)

        d = datetime.now()

        month = d.month
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October',
                  'November', 'December']
        month = months[month - 1]

        day = d.day
        year = d.year

        date = str(day) + ' ' + month + ' ' + str(year)
        date = str(date)
        print(date)

        new = FeedsModel(feed_name=food_name, unit_price=price, quantity=quantity, total=total, date=date)
        new.insert_records()

        expense = ExpensesModel(description='Feeds', amount=total, date=date)
        expense.insert_records()

    return redirect(url_for('food_history'))


@app.route('/expenses')
def expenses():
    expenses = ExpensesModel.fetch_all()
    return render_template('expenses.html', expenses=expenses)

# new expenses
@app.route('/new_expense', methods=['POST'])
def new_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']

        d = datetime.now()

        month = d.month
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October',
                  'November', 'December']
        month = months[month - 1]

        day = d.day
        year = d.year

        date = str(day) + ' ' + month + ' ' + str(year)
        date = str(date)
        print(date)

        new = ExpensesModel(description=description, amount=amount, date=date)
        new.insert_records()
    return redirect(url_for('expenses'))


@app.route('/staff')
def staff():
    staffs = StaffsModel.fetch_all()
    return render_template('staff.html', staffs=staffs)

# new staff
@app.route('/new_staff', methods=['POST'])
def new_staff():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']

        new = StaffsModel(name=name, email=email, phone=phone_number)
        new.insert_records()
    return redirect(url_for('staff'))


if __name__ == '__main__':
    app.run()
