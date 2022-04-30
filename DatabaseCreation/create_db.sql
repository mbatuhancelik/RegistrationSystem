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

DELIMITER $$


CREATE TRIGGER student_Insert
BEFORE INSERT
ON Student FOR EACH ROW
BEGIN
    DECLARE rowcount INT;
    
    SELECT COUNT(*) 
    INTO rowcount
    FROM Instructor WHERE new.username = Instructor.username;
    
    IF rowcount > 0 THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'A user can only be instructor or student. There already exists an instructor with this username.', MYSQL_ERRNO = 001;
    END IF; 

END $$

CREATE TRIGGER instructor_Insert
BEFORE INSERT
ON Instructor FOR EACH ROW
BEGIN
    DECLARE rowcount INT;
    
    SELECT COUNT(*) 
    INTO rowcount
    FROM Student WHERE new.username = Student.username;
    
    IF rowcount > 0 THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'A user can only be instructor or student. There already exists an instructor with this username.', MYSQL_ERRNO = 002;
    END IF; 

END $$

CREATE TRIGGER databasemanager_Insert
BEFORE INSERT
ON databasemanager FOR EACH ROW
BEGIN
    DECLARE rowcount INT;
    
    SELECT COUNT(*) 
    INTO rowcount
    FROM databasemanager;
    
    IF rowcount >= 4 THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Number of database managers cant be more than 4.', MYSQL_ERRNO = 003;
    END IF; 

END $$

CREATE TRIGGER location_Insert
BEFORE INSERT
ON location FOR EACH ROW
BEGIN
    DECLARE location_capacity INT;
    DECLARE location_quota INT;
    
    SELECT capacity
    INTO location_capacity
    FROM classroom WHERE classroom.classroom_id =  new.classroom_id;
    
    SELECT quota
    INTO location_quota
    FROM course WHERE course.course_id =  new.course_id;
    
    IF location_capacity < location_quota THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Classroom capacity is not sufficient for this course.', MYSQL_ERRNO = 004;
    END IF; 

END $$

CREATE TRIGGER enrolled_Insert_quota
BEFORE INSERT
ON enrolled_in FOR EACH ROW
BEGIN
    
    DECLARE course_quota INT;
    DECLARE enrolled_students INT;
    
    SELECT count(student_id)
    INTO enrolled_students
    FROM enrolled_in WHERE enrolled_in.course_id =  new.course_id;
    
    SELECT quota
    INTO course_quota
    FROM course WHERE course.course_id =  new.course_id;
    
    IF enrolled_students >= course_quota THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'You can not take this course due to quota restrictions!', MYSQL_ERRNO = 005;
    END IF; 

END $$

CREATE TRIGGER grades_Insert
AFTER INSERT
ON grades FOR EACH ROW
BEGIN
    DECLARE gpa float;
    DECLARE sum_Credits INT;
    
    Select SUM(course.credits * g.grade)/SUM(course.credits),  SUM(course.credits)
    Into gpa ,  sum_Credits
	from 
	course inner join(
	SELECT * 
	FROM grades
	where student_id = new.student_id
	)  as g on course.course_id = g.course_id;
    
    Update student set 
    gpa = gpa,
    completed_credits = sum_Credits
    where
    student.student_id = new.student_id;
    
    delete from enrolled_in where student_id = new.student_id and course_id = new.course_id;

END $$

CREATE TRIGGER enrolled_Insert_prerequisite
AFTER INSERT
ON enrolled_in FOR EACH ROW
BEGIN
declare not_taken_preqs int;

select count(*)
into not_taken_preqs
from
	(select prerequisite
	from prerequisite_of
	where 
	prerequisite_of.main = new.course_id) as preq
where 
	preq.prerequisite not in (
	select course_id
	from grades
	where student_id = new.student_id);
    
     IF not_taken_preqs > 0 THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'You can not take this course due to prerequisite restrictions!', MYSQL_ERRNO = 005;
    END IF; 
END $$

CREATE TRIGGER enrolled_Insert_retake
AFTER INSERT
ON enrolled_in FOR EACH ROW
BEGIN
declare retake int;

select count(*)
into retake
from
	grades
where 
	grades.student_id = new.student_id and
    grades.course_id =  new.course_id;
    
     IF retake > 0 THEN
		SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'You can not take a course twice', MYSQL_ERRNO = 005;
    END IF; 
END $$
DELIMITER ;
