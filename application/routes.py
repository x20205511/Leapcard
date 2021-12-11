from logging import log
from flask import Flask, render_template, flash, redirect, request, url_for
from flask.globals import session
from application import application, db, bcrypt
from application.forms import CardForm, LogForm, RegForm, UpdateForm
from application.models import User, Card
from flask_login import login_user, current_user, logout_user, login_required


@application.route("/home")
@login_required
def home():
    currentcard = Card.query.filter_by(user_id= current_user.id).first() 
    return render_template("home.html",card=currentcard)

@application.route("/error")
def error():
    return "Server error occureed"

@application.route("/", methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LogForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                # print(current_user)
                # next_page = request.args.get('next')
                # return redirect(next_page) if next_page else 
                return redirect(url_for('home'))
            else:
                flash('Login failed. Please check credentials', 'danger')
    except:
        return redirect(url_for('error'))
    return render_template("login.html", form = form)

@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The account is successfully created for {form.email.data}!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form = form)

@application.route("/apply", methods=['GET', 'POST'])
@login_required
def apply():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(balance = form.balance.data, user_id = current_user.id) 
        print(card)
        db.session.add(card)
        db.session.commit()
        # currentcard = Card.query.filter_by(user_id= current_user.id).first() 
        # flash(f'The card number is generated for {currentcard.cardnum}!')
        return redirect(url_for('carddetails'))
    return render_template("apply.html", form = form)

@application.route("/carddetails", methods=['GET', 'POST'])
@login_required
def carddetails():
    form = UpdateForm()
    currentcard = Card.query.filter_by(user_id= current_user.id).first()
    if form.add_submit.data:
        currentcard.balance += form.amount.data
        db.session.commit()
        redirect(url_for('carddetails'))
    if form.withdraw_submit.data:
        currentcard.balance -= form.amount.data
        db.session.commit()
    return render_template("carddetails.html", firstname = current_user.firstname, card = currentcard, form = form)

@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@application.route("/deleteaccount")
def deleteaccount():
    user = User.query.filter_by(id= current_user.get_id()).first()
    currentcard = Card.query.filter_by(user_id= current_user.id).first() #To retrieve the current card number of the current user
    logout()
    db.session.delete(currentcard)
    db.session.delete(user)
    db.session.commit()
    flash('The account has been deleted. We will miss you on Leap Card site.', 'danger')
    return redirect(url_for("login"))

@application.route("/about")
def about():
    return render_template("about.html")
