# app.py

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo
mongo = PyMongo(app)

# Enable CORS
CORS(app)

# Register Blueprints
from routes import user_bp, test_bp
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(test_bp, url_prefix='/api/test')

# Define a simple home route
@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the Local Parties App API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
