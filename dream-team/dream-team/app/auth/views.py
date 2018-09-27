from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import exc

from . import auth
from .forms import LoginForm, RegisterationForm
from .. import db
from ..models import Employee

@auth.route('/register',methods=['GET','POST'])
def register():
    # Add employee deatils to the database
    form = RegisterationForm()
    if form.validate_on_submit():
        employee = Employee(email = form.email.data,
                            username = form.username.data,
                            first_name = form.first_name.data,
                            last_name = form.last_name.data,
                            password = form.password.data)
        db.session.add(employee)
        try:
            db.session.commit()
            flash("You have registered Successfully! You can now Login")
            return redirect(url_for('auth.login'))
        except exc.IntegrityError:
            #flash("Email aleady exists")
            db.session.rollback()
            return render_template('auth/register.html',form=form,title = 'Register')

    #load registeration render_template
    return render_template('auth/register.html',form=form,title = 'Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the dashboard page after login
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
