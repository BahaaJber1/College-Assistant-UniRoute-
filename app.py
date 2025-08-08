from flask import Flask
from routes.auth_routes import auth_routes
from models.setup_db import initialize_database

app = Flask(__name__, static_folder="static")


# Secret key for session management
app.secret_key = "123"  # Replace with a strong, random secret key

# Register Blueprints
app.register_blueprint(auth_routes)

if __name__ == "__main__":
    app.run(debug=True)
