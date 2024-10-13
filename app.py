# app.py

from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mongo  # Import mongo from extensions.py

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo with the app
mongo.init_app(app)

# Enable CORS
CORS(app)

# Register Blueprints
from routes import user_bp, test_bp, game_bp
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(test_bp, url_prefix='/api/test')
app.register_blueprint(game_bp, url_prefix='/api/game')

# Define a simple home route
@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the Local Parties App API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True)