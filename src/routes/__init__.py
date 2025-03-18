from .company_routes import company_routes
from .user_routes import user_routes
def register_blueprints(app):
    app.register_blueprint(company_routes, url_prefix='/companies')
    app.register_blueprint(user_routes, url_prefix='/users')
