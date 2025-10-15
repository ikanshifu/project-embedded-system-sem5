# app.py
from flask import Flask, request, jsonify, render_template
import sqlite3
import json

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('bins.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    # We store the latest status and location for each bin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bins (
            id TEXT PRIMARY KEY,
            fullness INTEGER,
            lat REAL,
            lon REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# API endpoint for the ESP8266 to send data to
@app.route('/api/update_bin', methods=['POST'])
def update_bin():
    data = request.get_json()
    bin_id = data['bin_id']
    fullness = data['fullness']
    
    conn = sqlite3.connect('bins.db')
    cursor = conn.cursor()
    # Use INSERT OR REPLACE to add or update the bin's status
    cursor.execute("INSERT OR REPLACE INTO bins (id, fullness) VALUES (?, ?)", (bin_id, fullness))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"}), 200

# API endpoint for the frontend to get all bin data
@app.route('/api/get_bins', methods=['GET'])
def get_bins():
    conn = sqlite3.connect('bins.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, fullness, lat, lon FROM bins")
    bins = [{"id": row[0], "fullness": row[1], "lat": row[2], "lon": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(bins)

# Route to serve the main dashboard page
@app.route('/')
def index():
    return render_template('index.html') # We will create this HTML file

if __name__ == '__main__':
    init_db() # Create the database on first run
    app.run(host='0.0.0.0', port=5000) # Runs the server