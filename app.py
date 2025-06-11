import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Mongo URI from environment variable
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Connect to MongoDB
mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello from Fragrantica API!"

@app.route("/search")
def search_perfume():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = mongo.db.perfumes.find({"name": {"$regex": query, "$options": "i"}})
    perfumes = []
    for perfume in results:
        perfume["_id"] = str(perfume["_id"])  # Convert ObjectId to string
        perfumes.append(perfume)

    if not perfumes:
        return jsonify({"error": "No perfumes found"}), 404

    return jsonify(perfumes)

if __name__ == "__main__":
    app.run(debug=True)
