"""electricity endpoint"""

from flask import Flask
from flask_smorest import Api
from resources.home_api import blp as home_api

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Store data home REST API"
app.config["API_VERSION"] = "v2.0.0"
app.config["OPENAPI_VERSION"] = "3.1.1"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(home_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100)