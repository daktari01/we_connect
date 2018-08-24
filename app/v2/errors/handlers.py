from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(e):
    return jsonify({"message": "The page you are looking for "+
                                    "does not exist."}), 404

@errors.app_errorhandler(400)
def error_400(e):
    return jsonify({"message": "WeConnect encountered an error while "+
                            "processing your request. Kindly try again"}), 400

@errors.app_errorhandler(401)
def error_401(e):
    return jsonify({"message": "The resource you are trying to access"+
                                        " requires more privileges."}), 401

@errors.app_errorhandler(500)
def error_500(e):
    return jsonify({"message": "WeConnect was unable to process your "+
                                        "request. Kindly try again"}), 500