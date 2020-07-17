from flask import Flask, render_template, redirect
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
    print(key)
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

if __name__ == '__main__':
    #webapp.jinja_env.auto_reload = True
    #webapp.config['TEMPLATES_AUTO_RELOAD'] = True
    webapp.run(debug=True, host='0.0.0.0')