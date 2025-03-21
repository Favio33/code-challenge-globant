from flask import Flask

from config import config
from routes import department, hired_employees, jobs

app = Flask(__name__)

def page_not_found(error):
    return "<h1>Not Found Page</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(department.main, url_prefix='/api/department')
    app.register_blueprint(jobs.main, url_prefix='/api/job')
    app.register_blueprint(hired_employees.main, url_prefix='/api/employee')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
