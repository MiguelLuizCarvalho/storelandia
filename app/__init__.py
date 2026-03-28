import os
from flask import Flask

def create_app():
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static')

    from .routes import main
    from .auth import auth_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)

    return app