from flask import session, current_app

def regenerate_session(app):
    @app.after_request
    def renegerate_session_id(response):
        #regenerate session to prevent session fixation attack
        current_app.session_interface.regenerate_session(session)
        return response
