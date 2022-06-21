from makler import app
from flask import render_template, redirect, url_for, flash, request
from makler.models import Akcje, User
from makler import finnhub_client
from makler.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from makler import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    news = [finnhub_client.general_news('general')[0],finnhub_client.general_news('general')[1],finnhub_client.general_news('general')[2],finnhub_client.general_news('general')[3],finnhub_client.general_news('general')[4],finnhub_client.general_news('general')[5]]
    return render_template('home.html', news=news)


@app.route('/stock')
@login_required
def stock_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    # cena_appl = finnhub_client.quote('AAPL')["c"]
    lista_akcji = finnhub_client.stock_symbols('US')[0:10]
    cena_appl = list()
    id = list(range(1, 10))
    for name in lista_akcji:
        cena_appl.append(finnhub_client.quote(name['symbol'])["c"])
    lista_calosc = zip(id, lista_akcji, cena_appl)
    # for item in lista_calosc:
    #     print(item)

    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Akcje.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Gratulacje! Kupiłeś akcje {p_item_object.name} za {p_item_object.price}$",
                      category='success')
            else:
                flash(f"Niestety nie masz wystarczających środków na zakup {p_item_object.name}!",
                      category='danger')
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Akcje.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Gratulacje! Sprzedałeś {s_item_object.name}!", category='success')
            else:
                flash(f"Coś przebiegło nieprawidłowo ze sprzedażą akcji {s_item_object.name}", category='danger')

        return redirect(url_for('stock_page'))


    if request.method == "GET":
        items = lista_calosc
        owned_items = Akcje.query.filter_by(owner=current_user.id)
        return render_template('stock.html', lista_calosc=lista_calosc, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)

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
