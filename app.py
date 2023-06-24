from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'listings.db'
CSV_FILE = 'data.csv'

def load_data():
    data = pd.read_csv(CSV_FILE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS listings')

    cursor.execute('''CREATE TABLE IF NOT EXISTS listings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        homeDetailUrl TEXT,
                        price_to_rent_ratio REAL,
                        imgSrc TEXT,
                        country TEXT,
                        currency TEXT,
                        homeStatus TEXT,
                        price INTEGER,
                        state TEXT,
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        zipcode TEXT,
                        city TEXT,
                        streetName TEXT
                        )''')

    data.to_sql('listings', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

@app.route('/listing/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM listings WHERE id = ?', (listing_id,))
    row = cursor.fetchone()

    if row:
        listing = {
            'id': row['id'],
            'homeDetailUrl': row['homeDetailUrl'],
            'price_to_rent_ratio': row['price_to_rent_ratio'],
            'imgSrc': row['imgSrc'],
            'country': row['country'],
            'currency': row['currency'],
            'homeStatus': row['homeStatus'],
            'price': row['price'],
            'state': row['state'],
            'bedrooms': row['bedrooms'],
            'bathrooms': row['bathrooms'],
            'zipcode': row['zipcode'],
            'city': row['city'],
            'streetName': row['streetName']
        }
        return jsonify(listing)
    else:
        return jsonify({'message': 'Listing not found'})

@app.route('/listings', methods=['GET'])
def get_all_listings():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM listings')
    rows = cursor.fetchall()

    listings = []
    for row in rows:
        listing = {
            'id': row['id'],
            'homeDetailUrl': row['homeDetailUrl'],
            'price_to_rent_ratio': row['price_to_rent_ratio'],
            'imgSrc': row['imgSrc'],
            'country': row['country'],
            'currency': row['currency'],
            'homeStatus': row['homeStatus'],
            'price': row['price'],
            'state': row['state'],
            'bedrooms': row['bedrooms'],
            'bathrooms': row['bathrooms'],
            'zipcode': row['zipcode'],
            'city': row['city'],
            'streetName': row['streetName']
        }
        listings.append(listing)

    return jsonify(listings)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Real Estate Listing API'})

if __name__ == '__main__':
    load_data()
    app.run(debug=True)
