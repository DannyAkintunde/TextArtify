from flask import Flask
from flask_caching import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    @app.after_request
    async def add_dev_details(response):
      if response.content_type == 'application/json':
          data = await response.get_json()
          data['developer_github'] = {
            "user_name": "DannyAkintunde",
            "profile_link": "https://github.com/DannyAkintunde"
          }
          response.set_data(jsonify(data).data)
    
      return response
      
      cache.init_app(app)
      
      from app import routes
      
      app.register_blueprint(routes.bp)
      app.register_blueprint(routes.v1, url_prefix='/api/v1')
      
      return app