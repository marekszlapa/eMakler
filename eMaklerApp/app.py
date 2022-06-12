from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/stock')
def stock_page():
    stocks = [
        {'id': 1, 'name': 'Akcja1', 'price': 100},
        {'id': 2, 'name': 'Akcja2', 'price': 200},
        {'id': 3, 'name': 'Akcja3', 'price': 300}
    ]
    return render_template('stock.html', stocks=stocks)
