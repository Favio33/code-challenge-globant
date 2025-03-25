import os

from flask import Flask, send_from_directory

from config import configuration
from routes import aggregations, department, hired_employees, jobs


def create_app():
    app = Flask(__name__, static_folder='static')
    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(configuration[env])

    # Blueprints
    app.register_blueprint(department.department_bp, url_prefix='/api/departments')
    app.register_blueprint(jobs.jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(hired_employees.employees_bp, url_prefix='/api/employees')
    app.register_blueprint(aggregations.aggregations_bp, url_prefix='/api/aggregations')

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    
    return app

def page_not_found(error):
    return "<h1>Not Found Raaaaaaaa</h1>", 404

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
