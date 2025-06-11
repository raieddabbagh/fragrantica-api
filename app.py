import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

@app.route("/search")
def search():
    query = request.args.get("query", "")
    try:
        collection = mongo.db.perfumes  # or whatever your collection name is
        results = collection.find({"name": {"$regex": query, "$options": "i"}})
        perfumes = list(results)
        if not perfumes:
            return jsonify(error="No perfumes found"), 404
        # convert ObjectId to string
        for p in perfumes:
            p["_id"] = str(p["_id"])
        return jsonify(perfumes)
    except PyMongoError as e:
        app.logger.error(f"Mongo error: {e}")
        return jsonify(error="Database error"), 500
    except Exception as e:
        app.logger.error(f"Unhandled error: {e}", exc_info=True)
        return jsonify(error="Internal server error"), 500

@app.route("/")
def root():
    return "Hello from Fragrantica API!"

if __name__ == "__main__":
    app.run()
