create table public.departments (
	id bigint not null,
	department varchar(50) not null,
	last_updated timestamp without time zone,
	primary key (id)
);

create table public.jobs (
	id bigint not null,
	job varchar(50) not null,
	last_updated timestamp without time zone,
	primary key (id)
);

create table public.hired_employees (
	id bigint not null,
	name varchar(100) not null,
	datetime timestamp without time zone,
	department_id bigint,
	job_id bigint,
	last_updated timestamp without time zone,
	primary key (id),
	constraint fk_job foreign key (job_id) references jobs(id),
	constraint fk_department foreign key (department_id) references departments(id)
);
