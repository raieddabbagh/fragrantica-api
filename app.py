import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Use MONGO_URI from Render environment variable
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Connect to MongoDB
mongo = PyMongo(app)

@app.route("/")
def home():
    return "Hello from Fragrantica API!"

@app.route("/search")
def search_perfumes():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        perfumes = mongo.db.perfumes.find({"name": {"$regex": query, "$options": "i"}})
        results = [{"name": p["name"], "brand": p.get("brand", "")} for p in perfumes]

        if not results:
            return jsonify({"error": "No perfumes found"}), 404

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
