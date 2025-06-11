import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# Load Mongo URI from environment variable (set this in Render)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Setup MongoDB connection
mongo = PyMongo(app)

# Default route
@app.route("/")
def index():
    return "Hello from Fragrantica API!"

# Search perfumes
@app.route("/search")
def search():
    query = request.args.get("query", "").strip().lower()

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        perfumes = mongo.db.perfumes.find({
            "name": {"$regex": query, "$options": "i"}
        })
        results = list(perfumes)

        if not results:
            return jsonify({"error": "No perfumes found"}), 404

        return dumps(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
