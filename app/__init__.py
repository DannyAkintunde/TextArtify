from flask import Flask
from flask_caching import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    cache.init_app(app)
    
    from app import routes
    
    app.register_blueprint(routes.bp)
    app.register_blueprint(routes.v1, url_prefix='/api/v1')
    
    return app