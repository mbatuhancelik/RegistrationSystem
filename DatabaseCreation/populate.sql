INSERT IGNORE INTO  department VALUES("CMPE","cmpe");
INSERT IGNORE INTO  user VALUES("kadir.","kadir@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("batu.","b@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("ali.","kadir@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("veli.","kadir@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("salim.","kadir@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("ece.","kadir@","123","kadir","sur","CMPE");
INSERT IGNORE INTO  student(username,student_id)  VALUES("ece.",1);
INSERT IGNORE INTO  student(username,student_id)  VALUES("salim.",2);
INSERT IGNORE INTO  student(username,student_id)  VALUES("batu.",3);
INSERT ignore INTO  instructor VALUES("kadir.","asdas");
INSERT IGNORE INTO  instructor VALUES("ali.","Professor");
INSERT IGNORE INTO  instructor VALUES("veli.","Professor");

insert ignore into course Values("CMPE321", "database", 4, 100, "kadir.");
insert ignore into course Values("CMPE350", "oto", 4, 100, "ali.");
insert ignore into course Values("CMPE220", "oto", 4, 100, "ali.");

insert into prerequisite_of values("CMPE321", "CMPE220");
insert into enrolled_in values(3, "CMPE321");

-- insert ignore into grades Values(3, "CMPE321", 3);
-- insert ignore into grades Values(3, "CMPE350", 4);
-- insert ignore into grades Values(3, "CMPE320", 0);
