import settings
from flask import Flask
from views import router
import logging

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
app.secret_key = "secret key"
app.register_blueprint(router)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)
    
"""

    TODO: Test feedback: AssertionError: 2 != 1
    TODO: Test predict Eskimo_dog: AssertionError: 0.9345517 != 0.9346 within 5 places (4.82841491699082e-05 difference)
"""
