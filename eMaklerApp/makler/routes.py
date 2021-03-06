from makler import app
from flask import render_template, redirect, url_for, flash
from makler.models import Akcje, User
from makler import finnhub_client
from makler.forms import RegisterForm, LoginForm
from makler import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    news = [finnhub_client.general_news('general')[0],finnhub_client.general_news('general')[1],finnhub_client.general_news('general')[2],finnhub_client.general_news('general')[3],finnhub_client.general_news('general')[4],finnhub_client.general_news('general')[5]]
    return render_template('home.html', news=news)


@app.route('/stock')
@login_required
def stock_page():
    # cena_appl = finnhub_client.quote('AAPL')["c"]
    lista_akcji = finnhub_client.stock_symbols('US')[0:10]
    cena_appl = list()
    for nazwa in lista_akcji:
        cena_appl.append(finnhub_client.quote(nazwa['symbol'])["c"])
    lista_calosc = zip(lista_akcji, cena_appl)
    # for item in lista_calosc:
    #     print(item)

    return render_template('stock.html', lista_calosc=lista_calosc)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Konto zostało utworzone. Zalogowano jako: {user_to_create.username}', category='success')
        return redirect(url_for('stock_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Zalogowano jako: {attempted_user.username}', category='success')
            return redirect(url_for('stock_page'))
        else:
            flash('Złe hasło i/lub nazwa użytkownika. Spróbuj ponownie.', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Zostałeś wylogowany.", category='info')
    return redirect(url_for("home_page"))
