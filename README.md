File Descriptions:

app.py: Initializes Flask, connects to MongoDB, registers Blueprints, and defines the home route.
config.py: Loads environment variables from .env and defines the Config class.
requirements.txt: Lists all Python dependencies.
.env: Stores environment variables like MONGO_URI and SECRET_KEY.
.gitignore: Specifies files/directories to ignore in Git.
models/:
__init__.py: Initializes the models package and imports the User model.
user.py: Defines the User class with CRUD operations.
routes/:
__init__.py: Initializes the routes package and imports Blueprints.
user_routes.py: Contains API endpoints for user-related operations.
test_routes.py: Contains a test route to verify MongoDB connectivity.
utils/:
__init__.py: Initializes the utils package and imports helper functions.
helpers.py: Defines helper functions like match_users.