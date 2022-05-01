CREATE TABLE IF NOT EXISTS department (
	department_id	VARCHAR(50) not Null,
	name	VARCHAR(50) UNIQUE not Null,
	PRIMARY KEY(department_id)
);
CREATE TABLE IF NOT EXISTS User (
-- A user must be instructor or student. Each user entry must be inserted to either instructor or student after its creation.
	username	VARCHAR(20) not Null,
	email	VARCHAR(50) not Null,
	password	VARCHAR(256) not Null,
	name	VARCHAR(50) not Null,
	surname	VARCHAR(50) not Null,
    department_id  varchar(50) not Null,
    FOREIGN KEY(department_id) REFERENCES department(department_id) on delete cascade,
	PRIMARY KEY(username)
);
CREATE TABLE IF NOT EXISTS Student ( 
-- An instructor can not be in Student table.
	username	VARCHAR(50) not Null,
	student_id 	INTEGER UNIQUE not Null,
    gpa float default 0,
    completed_credits int default 0,
	FOREIGN KEY(username) REFERENCES User(username) on delete cascade,
	PRIMARY KEY(username)
);
CREATE TABLE IF NOT EXISTS Instructor (
-- A student can not be in Instructor table.
	username	VARCHAR(50) not Null,
	title	ENUM('Assistant Professor', 'Associate Professor', 'Professor') not Null,
	FOREIGN KEY(username) REFERENCES User(username) on delete cascade,
	PRIMARY KEY(username)
);
CREATE TABLE IF NOT EXISTS Course (
	course_id	VARCHAR(50) not Null,
	name	VARCHAR(50) not Null,
	credits	INTEGER not Null,
	quota	INTEGER not Null,
    lecturer	VARCHAR(50) not Null,
    FOREIGN KEY(lecturer) REFERENCES Instructor(username) on delete cascade,
	PRIMARY KEY(course_id)
);
CREATE TABLE IF NOT EXISTS Classroom (
	classroom_id	VARCHAR(50) not Null,
	capacity	INTEGER not Null,
	campus	VARCHAR(50) not Null,
	PRIMARY KEY(classroom_id)
);
CREATE TABLE IF NOT EXISTS Location (
-- Course quota can not exceed classroom capacity.
	course_id	VARCHAR(50) UNIQUE not Null,
	classroom_id	VARCHAR(50) not Null,
	timeslot INTEGER not Null CHECK(timeslot >= 1 AND timeslot <= 10),
	FOREIGN KEY(classroom_id) REFERENCES Classroom(classroom_id) on delete cascade,
	FOREIGN KEY(course_id) REFERENCES Course(course_id) on delete cascade,
	PRIMARY KEY(classroom_id,timeslot)
);
CREATE TABLE IF NOT EXISTS Grades (
	student_id	INTEGER not Null,
	course_id	VARCHAR(50) not Null,
	grade	REAL CHECK(grade >= 0 AND grade <= 4),
	FOREIGN KEY(student_id) REFERENCES Student(student_id ) on delete cascade,
	FOREIGN KEY(course_id) REFERENCES Course(course_id),
	PRIMARY KEY(student_id,course_id)
);
CREATE TABLE IF NOT EXISTS Enrolled_In (
-- The enrolled course must not be full.
-- User cannot enroll to a course that they didn't finished its prerequisites.
	student_id	INTEGER not Null,
	course_id	VARCHAR(50) not Null,
	FOREIGN KEY(student_id) REFERENCES Student(student_id ) on delete cascade,
	FOREIGN KEY(course_id) REFERENCES Course(course_id) on delete cascade,
	PRIMARY KEY(course_id,student_id)
);
CREATE TABLE IF NOT EXISTS DatabaseManager (
-- There can be at most 4 database managers.
	username	VARCHAR(50) not Null,
	password	VARCHAR(256) not Null,
	PRIMARY KEY(username)
);
CREATE TABLE IF NOT EXISTS Prerequisite_Of (
	main	VARCHAR(50) not Null,
	prerequisite	VARCHAR(50) not Null,
	FOREIGN KEY(prerequisite) REFERENCES Course(course_id) on delete cascade,
	FOREIGN KEY(main) REFERENCES Course(course_id) on delete cascade,
	PRIMARY KEY(main,prerequisite),
    CHECK (prerequisite < main)
);