
from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient
import random
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#connect to database
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']
collection = db['employees']


# Predefined set of usernames and passwords

users = {
    'admin': '123'
}
#employees = []

#login routes
@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('create_staff'))
        else:
            message = 'Invalid username or password'
    return render_template('login.html', message=message)

@app.route("/create_employee", methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        IDnumber = request.form['IDnumber']
        #branchname
        #photo
        #membership number

        #generate random registration number
        registration_number = ''.join(random.choices('0123456789', k=6))
        #time created y/m/d
        reg_date = datetime.datetime.now().replace(second=0, microsecond=0)
        


        employee = {
            'registration_number': registration_number,
            'name': name,
            'department': department,
            'IDnumber': IDnumber,
            'reg_date': reg_date
        }
        #employees.append(employee)
        collection.insert_one(employee)
        return render_template('success.html', employee=employee)
    return render_template('create_employee.html')

@app.route('/employees')
def display_employees():
    employees = collection.find()
    return render_template('employees.html', employees=employees)


# admin route: admin to capture the staff members who will be capturing
# the detail of members
@app.route('/admin', methods=['GET', 'POST'])
def create_staff():
    if request.method == 'POST':
        staff_number = request.form['staff_number']
        username = request.form['username']
        password = request.form['password']
        registration_date = request.form['registration_date']
        status = request.form['status']
        branch = request.form['branch']
        title = request.form['title']
        created_at = datetime.datetime.now()

        staff_data = {
            "staff_number": staff_number,
            "username": username,
            "password": password,
            "registration_date": registration_date,
            "status": status,
            "branch": branch,
            "title": title,
            "created_at": created_at
        }

        collection.insert_one(staff_data)

        return redirect(url_for('create_staff'))

    return render_template('create_staff.html')

@app.route("/admin/list-staff", methods=["GET"])
def staff_list():
    staff_members = collection.find()
    return render_template('display_staff.html', staff_members=staff_members)

# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)