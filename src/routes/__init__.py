from .company_routes import company_routes

def register_blueprints(app):
    app.register_blueprint(company_routes, url_prefix='/companies')