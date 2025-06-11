from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB connection URI
app.config["MONGO_URI"] = "mongodb://fragrantica_user:ruZmud-bovhyr-nipci9@cluster0-shard-00-00.mongodb.net:27017,cluster0-shard-00-01.mongodb.net:27017,cluster0-shard-00-02.mongodb.net:27017/dbname?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin"
mongo = PyMongo(app)

@app.route("/")
def home():
    return "Hello from Fragrantica API!"

@app.route("/search")
def search_perfume():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    perfumes_collection = mongo.db.perfumes
    results = perfumes_collection.find({
        "name": {"$regex": query, "$options": "i"}
    })

    perfumes = []
    for perfume in results:
        perfume["_id"] = str(perfume["_id"])
        perfumes.append(perfume)

    if not perfumes:
        return jsonify({"error": "No perfumes found"}), 404

    return jsonify(perfumes)

if __name__ == "__main__":
    app.run(debug=True)
