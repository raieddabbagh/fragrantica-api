from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MongoDB connection from environment variable
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Initialize PyMongo
mongo = PyMongo(app)

@app.route('/')
def home():
    return jsonify({"message": "Fragrantica API is running"})

@app.route('/search')
def search_perfumes():
    query = request.args.get('query', '')

    if not mongo.db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Attempt to query the perfumes collection
        results = mongo.db.perfumes.find({"name": {"$regex": query, "$options": "i"}})
        perfumes = list(results)

        if not perfumes:
            return jsonify({"error": "No perfumes found"}), 404

        return jsonify({"results": perfumes})

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
