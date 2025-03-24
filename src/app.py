from flask import Flask

from config import config
from routes import department, hired_employees, jobs, aggregations

app = Flask(__name__)

def page_not_found(error):
    return "<h1>Not Found Page</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(department.department_bp, url_prefix='/api/departments')
    app.register_blueprint(jobs.jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(hired_employees.employees_bp, url_prefix='/api/employees')
    app.register_blueprint(aggregations.aggregations_bp, url_prefix='/api/aggregations')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
