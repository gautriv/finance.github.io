from flask import render_template, request, jsonify
from app import app
from app.stock_analyzer import analyze_all_stocks

@app.route('/', methods=['GET'])
def index():
    stock_data = analyze_all_stocks()  # Fetch data for all stocks
    return render_template('index.html', stock_data=stock_data)
