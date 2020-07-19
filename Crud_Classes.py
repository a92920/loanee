from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField

class CreateLoan(FlaskForm):
    lender = TextField('Lender')
    borrower = TextField('Borrower')
    ir = IntegerField('Interest Rate %')
    amount = IntegerField('amount')
    paid = IntegerField('paid')
    start = TextField('start')
    end = TextField('end')
    

    create = SubmitField('Create')

class UpdateLoan(FlaskForm):
    key = TextField('Loan ID')
    paid = TextField('Paid to date')
    update = SubmitField('Update')

class UpdateLoan1(FlaskForm):
    key = IntegerField('Loan ID')
    borrower = TextField('Become the borrower')
    lender = TextField('Become the lender')
    update = SubmitField('Update')