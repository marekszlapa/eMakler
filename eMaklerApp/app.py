from flask import Flask, render_template
import finnhub
app = Flask(__name__)
finnhub_client = finnhub.Client(api_key="caitgjqad3i2a9kcigrg")

# Stock candles


@app.route('/')
@app.route('/home')
def home_page():
    news = finnhub_client.general_news('general')[0]
    return render_template('home.html', news=news)


@app.route('/stock')
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
