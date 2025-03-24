from flask import Blueprint, jsonify
from sqlalchemy import text

from database.db import Database

aggregations_bp = Blueprint("aggregation_blueprint", __name__)

@aggregations_bp.route("/hiring-above-average", methods=["GET"])
def get_departments_hiring_above_avg():
    db = Database.get_instance()
    query = text("""
        with employees as (
            select id, department_id,
                extract(quarter from datetime) as quarter,
                extract(year from datetime) as year
            from hired_employees
            where department_id is not null
        ),
        hires_per_department as (
            select department_id, count(*) as count_hire_dept
            from hired_employees
            where extract(year from datetime) = 2021
                and department_id is not null
            group by department_id
        ),
        avg_employees_2021 as (
            select avg(count_hire_dept) as avg_2021
            from hires_per_department
        )
        select department_id, department,
            count(e.id) as hired
        from employees as e
        left join departments as d
            on e.department_id = d.id
        group by department_id, department
        having (
            count(e.id) > (select avg_2021 from avg_employees_2021)
        )
        order by hired desc;
    """)
    with db.get_session() as session:
        result = session.execute(query)
        data = [
            {
                "department_id": row[0],
                "department": row[1],
                "hired": row[2]
            }
            for row in result
            ]
        return jsonify(data), 200

@aggregations_bp.route("/count-2021-quarters", methods=["GET"])
def get_count_2021_quarter():
    db = Database.get_instance()
    query = text("""
        with employees_2021 as (
            select id, department_id, job_id, extract(quarter from datetime) as quarter, datetime 
            from hired_employees
            where extract(year from datetime) = 2021
        ),
        jobs as (
            select id, job
            from jobs
        ),
        departments as (
            select id, department
            from departments
        )
        select department, job,
            count(case
                when e.quarter = 1 then e.id
                else null
            end) as q1,
            count(case
                when e.quarter = 2 then e.id
                else null
            end) as q2,
            count(case
                when e.quarter = 3 then e.id
                else null
            end) as q3,
            count(case
                when e.quarter = 4 then e.id
                else null
            end) as q4
        from employees_2021 as e
        left join jobs as j 
            on e.job_id = j.id
        left join departments as d
            on e.department_id = d.id
        group by department, job
        order by department, job
    """)
    with db.get_session() as session:
        result = session.execute(query)
        data = [
            {
                "department": row[0],
                "job": row[1],
                "q1": row[2],
                "q2": row[3],
                "q3": row[4],
                "q4": row[5],
            }
            for row in result
            ]
        return jsonify(data), 200
