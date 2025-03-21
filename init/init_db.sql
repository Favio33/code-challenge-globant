drop table if exists public.hired_employees;
drop table if exists public.departments;
drop table if exists public.jobs;

create table public.departments (
	id serial,
	department varchar(50) not null,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id)
);

create table public.jobs (
	id serial,
	job varchar(50) not null,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id)
);

create table public.hired_employees (
	id serial,
	name varchar(100) not null,
	datetime timestamp without time zone,
	department_id serial,
	job_id serial,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id),
	constraint fk_job foreign key (job_id) references jobs(id),
	constraint fk_department foreign key (department_id) references departments(id)
);
