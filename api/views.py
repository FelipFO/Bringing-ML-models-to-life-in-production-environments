import os

import settings
import utils
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from middleware import model_predict
import app
import json

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)

        if file and utils.allowed_file(file.filename):
            # In order to correctly display the image in the UI and get model
            # predictions you should implement the following:
            #   1. Get an unique file name using utils.get_file_hash() function
            #   2. Store the image to disk using the new name
            #   3. Send the file to be processed by the `model` service
            #   4. Update `context` dict with the corresponding values
            file_hash = utils.get_file_hash(file)
            # dst_filepath = os.path.join(settings.UPLOAD_FOLDER, file_hash)
            dst_filepath = settings.UPLOAD_FOLDER+file_hash
            print(dst_filepath)
            if not os.path.exists(dst_filepath):
                file.save(dst_filepath)
        
                
            flash("Image successfully uploaded and displayed below")
            prediction, score = model_predict(file_hash)
            context = {
                "prediction": prediction,
                "score": score,
                "filename": file_hash,
            }
            return render_template("index.html", filename=file_hash, context=context)
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif")
            return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", settings.UPLOAD_FOLDER + filename), code=301)


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image
    #   2. Store the image to disk
    #   3. Send the file to be processed by the `model` service
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    rpse = {"success": False, "prediction": None, "score": None}

    if "file" in request.files and utils.allowed_file(request.files["file"].filename):
        file = request.files["file"]
        file_hash = utils.get_file_hash(file)

        dst_filepath = settings.UPLOAD_FOLDER+file_hash
        print(dst_filepath)
        if not os.path.exists(dst_filepath):
            file.save(dst_filepath)
        prediction, score = model_predict(file_hash)
        rpse["success"] = True
        rpse["prediction"] = prediction
        rpse["score"] = round(float(score),settings.DECIMAL_PRECISION)
        return jsonify(rpse)

    return jsonify(rpse), 400


@router.route("/feedback", methods=["GET","POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a plain text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    if request.method == 'GET':
        try:
            file_path = settings.FEEDBACK_FILEPATH

            if not os.path.isfile(file_path):
                return jsonify({'error': 'File not found'}), 404

            with open(file_path, 'r') as file:
                content = file.read()
                return jsonify({'report': content})
        except Exception as e:
            flash(f"An error occurred while submitting feedback: {str(e)}")

    if request.method == 'POST':
        try:
            with open(settings.FEEDBACK_FILEPATH, "a") as file:
                file.write(request.form['report']+"\n")

            flash("Feedback submitted successfully.")
        except Exception as e:
            flash(f"An error occurred while submitting feedback: {str(e)}")


    # Don't change this line
    return render_template("index.html")
