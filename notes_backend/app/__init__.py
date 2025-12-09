from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp

# Initialize Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable CORS for all routes (can be tightened later)
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI / Swagger configuration
app.config["API_TITLE"] = "Personal Notes API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Tag metadata for better documentation organization
openapi_tags = [
    {"name": "Health Check", "description": "Health check route"},
    {"name": "Notes", "description": "CRUD operations for personal notes"},
]

app.config["OPENAPI_TAGS"] = openapi_tags

# Initialize Smorest API and register blueprints
api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)
