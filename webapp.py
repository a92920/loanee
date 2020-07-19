from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from Crud_Classes import *

webapp = Flask(__name__)
webapp.config['Testing'] = True 
webapp.testing = True
webapp.config.update(dict(SECRET_KEY='yoursecretkey'), TESTING = True)

client = MongoClient('localhost:27017')
db = client.BankeeDB
collection = db.loan 

if db.settings.find({'name': 'loan_id'}).count() <= 0:
    print("loan_id Not found, creating....")
    db.settings.insert_one({'name': 'loan_id', 'value': 0})

def updateLoanID(value):
    loan_id = db.settings.find_one()['value']
    loan_id += value
    db.settings.update_one({'name': 'loan_id'}, {'$set': {'value': loan_id}})

def createLoan(form):
    lender = form.lender.data
    ir = form.ir.data
    borrower = form.borrower.data
    amount = form.amount.data
    paid = form.paid.data
    start = form.start.data
    end = form.end.data
    loan_id = db.settings.find_one()['value']
    

    loan = {'id': loan_id, 'lender': lender, 'borrower': borrower, 'ir': ir, 'amount': amount, 'paid': paid, 'start': start, 'end': end }

    db.loan.insert_one(loan)
    updateLoanID(1)
    return redirect('/')

def updateLoan(form):
    key = form.key.data
    paid = form.paid.data
    db.loan.update_one({"id": int(key)}, {"$set": {"paid": paid}},)
    return redirect('/')




@webapp.route('/', methods=['GET', 'POST'])
def main():
    cform = CreateLoan(prefix='cform')
    uform = UpdateLoan(prefix='uform')
    
    if cform.validate_on_submit() and cform.create.data:
        return createLoan(cform)

    if uform.validate_on_submit() and uform.update.data:
        return updateLoan(uform)
    

    
    docs = db.loan.find()
    data = []
    for i in docs: 
        data.append(i)

    return render_template('layout.html', cform=cform, data=data, uform=uform)

@webapp.route('/create', methods=['POST'])
def create():
    lender = request.form["lender"]
    ir = request.form['ir']
    borrower = request.form['borrower']
    amount = request.form['amount']
    paid = 0
    
    end = request.form['end']
    loan_id = db.settings.find_one()['value']

    loan = {'id': loan_id, 'lender': lender, 'borrower': borrower, 'ir': ir, 'amount': amount, 'paid': paid, 'end': end }
    db.loan.insert_one(loan)
    updateLoanID(1)

    
    return redirect('/')

@webapp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    db.loan.delete_one({"id":id})
    return redirect('/')

@webapp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if(request.form['lender'] != ''):
        db.loan.update_one(
            {"id": int(id)}, 
            {"$set": {"lender": request.form['lender'] } }
        )
    elif(request.form['borrower'] != ''):
       db.loan.update_one(
            {"id": int(id)}, 
            {"$set": {"borrower": request.form['borrower'] } }
        )
    return redirect('/')

@webapp.route('/pay/<int:id>', methods=['POST'])
def pay(id):
    db.loan.update_one(
        {"id": int(id)}, 
        {"$set": {"paid": request.form['paid'] } }
    )
    return redirect('/')

if __name__ == '__main__':
    #webapp.jinja_env.auto_reload = True
    #webapp.config['TEMPLATES_AUTO_RELOAD'] = True
    webapp.run(debug=True, host='0.0.0.0')