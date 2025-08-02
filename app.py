from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_FILE = 'queries.db'

if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        case_type TEXT,
                        case_number TEXT,
                        filing_year TEXT,
                        response TEXT,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']
        try:
            parsed_data, raw_html = fetch_case_data(case_type, case_number, filing_year)
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (case_type, case_number, filing_year, response, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (case_type, case_number, filing_year, raw_html, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return render_template('result.html', data=parsed_data)
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('index'))
    return render_template('index.html')

def fetch_case_data(case_type, case_number, filing_year):
    url = "https://delhihighcourt.nic.in/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data. Court website might be down.")
    soup = BeautifulSoup(response.content, 'html.parser')
    parsed_data = {
        'parties': 'John Doe vs Jane Doe',
        'filing_date': '2023-02-14',
        'next_hearing': '2025-08-12',
        'latest_order_pdf': '/mock-order.pdf'
    }
    return parsed_data, response.text

@app.route('/download/<path:filename>')
def download_file(filename):
    return redirect(f"https://delhihighcourt.nic.in/{filename}")

if __name__ == '__main__':
    app.run(debug=True)
