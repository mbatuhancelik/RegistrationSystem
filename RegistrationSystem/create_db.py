from MySQLdb import OperationalError
import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user=env("MYSQL_USER"),
  password=env("MYSQL_PASSWORD"),
  database=env("MYSQL_DATABASE"),
  auth_plugin='mysql_native_password'
)
cursor= connection.cursor()

creation_script_file =  open("DatabaseCreation\\create_tables.sql", "r")
creation_script = creation_script_file.read().split(';')
creation_script_file.close()
for sta in creation_script:
  cursor.execute(sta)

student_insert_trig = """
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
  END ;
"""
cursor.execute(student_insert_trig)
instructor_insert_trig = """
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

  END ;
"""
cursor.execute(instructor_insert_trig)
databasemanager_insert_trig = """
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
  END ;
"""
cursor.execute(databasemanager_insert_trig)

location_insert_trig = """
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
      Delete from course where course_id = new.course_id;
      END IF; 
    IF location_capacity < location_quota THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Classroom capacity is not sufficient for this course.', MYSQL_ERRNO = 004;
    END IF; 
END ;
"""
cursor.execute(location_insert_trig)
enrolled_insert_quota_trig = """
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
  END ;
"""
grades_insert_trig = """
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
  END ;
"""
cursor.execute(grades_insert_trig)
enrolled_insert_preq_trig = """
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
  END ;
"""

enrolled_insert_retake_trig = """
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
  END ;
"""
filter_procedure = """
  CREATE PROCEDURE `filterCourses` (IN departmentIn varchar(20),IN campusIn varchar(20), IN min_credits int, IN max_credits int)
  BEGIN
    select c.course_id, name, surname, department_id, credits, l.campus from 
    ( select location.course_id, classroom.campus from location inner join classroom
    on location.classroom_id = classroom.classroom_id
    where
        classroom.campus LIKE CONCAT('%', campusIn ,'%')
    ) as l
    inner join
    (
    Select course.course_id, course.name, user.surname, department_id, credits from course inner join user on course.lecturer = user.username
    where
        department_id LIKE CONCAT('%', departmentIn ,'%') and
        credits <= max_credits and
        credits >= min_credits
    ) as c
    on c.course_id = l.course_id;
  END ;
"""
cursor.execute(enrolled_insert_preq_trig)
cursor.execute(enrolled_insert_quota_trig)
cursor.execute(enrolled_insert_retake_trig)
cursor.execute(filter_procedure)



connection.commit()
    

