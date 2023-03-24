from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Transaction
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profileMgmnt():
    if request.method == 'POST':
        #email = current_user.email
        fullName = request.form.get('fullName')
        add1 = request.form.get('address1')
        add2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        #updating the database
        current_user.fullName = fullName
        current_user.address1 = add1
        current_user.address2 = add2
        current_user.city = city
        current_user.state = state
        current_user.zipcode = zipcode
        db.session.commit()
        
        # print(current_user.email)
        # print(current_user.fullName)
        # print(current_user.address1)
        # print(current_user.address2)
        # print(current_user.city)
        # print(current_user.state)
        # print(current_user.zipcode)



        return redirect(url_for('views.home'))

    return render_template("profile.html", user=current_user)


# @views.route('/price_module', methods=['POST', 'GET'])
# @login_required
# def price_module():
#     if request.method == 'POST': 
#         note = request.form.get('note')#Gets the note from the HTML 

#         if len(note) < 1:
#             flash('Note is too short!', category='error') 
#         else:
#             new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
#             db.session.add(new_note) #adding the note to the database 
#             db.session.commit()
#             flash('Note added!', category='success')

#     return render_template("price_module.html", user=current_user)


@views.route('/price_module', methods=['POST', 'GET'])
@login_required
def price_module():
    if request.method == 'POST': 
        gallons_text = request.form.get('gallons')
        gallons = int(gallons_text)
        address = request.form.get('address')
        delivery_date = request.form.get('date')

        total = 5*gallons
        
        newTransaction = Transaction(gallons=gallons,total=total, delivery_date=delivery_date, user_id=current_user.id)
        db.session.add(newTransaction) 
        db.session.commit()
        flash('Quote added!', category='success')

        print(gallons)
        print(address)
        print(type(delivery_date))
        print(delivery_date)

    return render_template("price_module.html", user=current_user)





@views.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template("history.html", user=current_user)

