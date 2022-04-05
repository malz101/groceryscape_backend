from flask import jsonify


def create_error_response(message,description,status):
    response = jsonify({'message': message, 'description': description, 'status': status})
    response.status_code = status
    return response