from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb+srv://fragrantica_user:ruZmud-bovhyr-nipci9@cluster0-shard-00-00.mongodb.net:27017,cluster0-shard-00-01.mongodb.net:27017,cluster0-shard-00-02.mongodb.net/perfumes_db?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin"
mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello from Fragrantica API!"

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    # Case-insensitive search in 'name' field
    results = mongo.db.perfumes.find({"name": {"$regex": query, "$options": "i"}})
    perfumes = list(results)
    if not perfumes:
        return jsonify({"error": "No perfumes found"}), 404

    return dumps(perfumes), 200

if __name__ == "__main__":
    app.run(debug=True)
