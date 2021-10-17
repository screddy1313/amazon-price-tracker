from flask import Flask, render_template
from flask.helpers import flash
from price_tracker import price_track as pt
from price_tracker import app
from price_tracker.forms import SearchForm, RegisterForm, LoginForm

@app.route('/')
def home() :
	return render_template('home.html')

@app.route('/search', methods = ['GET', 'POST'])
def prod_search():

    search = SearchForm()
    url = None

    if search.validate_on_submit() :
        url = search.url.data
        search.url.data = ''

        res = pt.price_wrapper(url)

        return render_template('search.html', results=res, form=search, url=url)

    return render_template('search.html', form=search, url=url)

@app.route('/register', methods = ['GET', 'POST'])
def register_page():

    reg_form = RegisterForm()

    if reg_form.validate_on_submit() :
        email = reg_form.email.data
        pswd = reg_form.password.data
        confirm = reg_form.confirm.data

        if pswd == confirm :
            return render_template('home.html')

        
    if reg_form.errors :

        for key in reg_form.errors :
            flash(f'{reg_form.errors[key][0]}', category='danger')

    return render_template('register.html', reg_form = reg_form)

@app.route('/login', methods = ['GET', 'POST'])
def login_page():

    log_form = LoginForm()

    if log_form.validate_on_submit() :

        email = log_form.email.data
        pswd = log_form.password.data

        print(email, pswd)

        if email == 'abc@gmail.com' and pswd == '12345' :
            flash(f' Welcome Back', category='success')
            return render_template('home.html')

    if log_form.errors :
        print(log_form.errors)
        flash(f'Incorrect details... please try again !!', category='danger')


    return render_template('login.html', log_form = log_form)