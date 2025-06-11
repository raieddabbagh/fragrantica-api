from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://fragrantica_user:ruZmud-bovhyr-nipci9@cluster0.mongodb.net/perfumes_db?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/')
def index():
    return "Hello from Fragrantica API!"

@app.route('/search')
def search_perfume():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    perfumes = mongo.db.perfumes.find({"name": {"$regex": query, "$options": "i"}})
    results = []
    for perfume in perfumes:
        results.append({
            "name": perfume.get("name", ""),
            "brand": perfume.get("brand", ""),
            "main_accords": perfume.get("main_accords", []),
            "longevity": perfume.get("longevity", ""),
            "sillage": perfume.get("sillage", "")
        })

    if not results:
        return jsonify({"error": "No perfumes found"}), 404
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
