drop table if exists public.hired_employees;
drop table if exists public.departments;
drop table if exists public.jobs;

create table public.departments (
	id bigint,
	department varchar(50) not null,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id)
);

create table public.jobs (
	id bigint,
	job varchar(50) not null,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id)
);

create table public.hired_employees (
	id bigint,
	name varchar(100) null,
	datetime timestamp without time zone,
	department_id bigint null,
	job_id bigint null,
	last_updated timestamp without time zone default current_timestamp,
	primary key (id),
	constraint fk_job foreign key (job_id) references jobs(id),
	constraint fk_department foreign key (department_id) references departments(id)
);
