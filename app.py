from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://mongo:27017/')
client = MongoClient(mongodb_uri)
db = client.mydatabase
collection = db.mycollection

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        if data:
            result = collection.insert_one(data)
            return jsonify({"message": "Data received", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "No data provided"}), 400
    else:
        data = list(collection.find())
        # Convert ObjectId to string for JSON serialization
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')