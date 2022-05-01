INSERT IGNORE INTO  databasemanager VALUES("kadir",sha2("123",256));
INSERT IGNORE INTO  databasemanager VALUES("batu",sha2("123",256));


INSERT IGNORE INTO  department VALUES("CMPE","cmpe");

INSERT IGNORE INTO  user VALUES("kadir.","kadir@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("batu","b@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("ali.","kadir@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("veli.","kadir@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("salim.","kadir@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  user VALUES("ece.","kadir@",sha2("123",256),"kadir","sur","CMPE");
INSERT IGNORE INTO  student(username,student_id)  VALUES("ece.",1);
INSERT IGNORE INTO  student(username,student_id)  VALUES("salim.",2);
INSERT IGNORE INTO  student(username,student_id)  VALUES("batu",3);
INSERT ignore INTO  instructor VALUES("kadir.","asdas");
INSERT IGNORE INTO  instructor VALUES("ali.","Professor");
INSERT IGNORE INTO  instructor VALUES("veli.","Professor");

insert ignore into course Values("CMPE321", "database", 4, 100, "kadir.");
insert ignore into course Values("CMPE350", "oto", 4, 100, "ali.");
insert ignore into course Values("CMPE220", "oto", 4, 100, "ali.");

insert ignore into classroom Values("NH101", 150, "North");

insert ignore into location Values("CMPE220", "NH101", 3);
insert ignore into location Values("CMPE350", "NH101", 4);

insert into prerequisite_of values("CMPE321", "CMPE220");
-- insert into enrolled_in values(3, "CMPE321");

INSERT IGNORE INTO  classroom VALUES("BMA1",120,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA2",140,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA3",140,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA4",140,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA5",140,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA6",140,"North Campus");
INSERT IGNORE INTO  classroom VALUES("BMA7",140,"North Campus");
INSERT IGNORE INTO  location VALUES("CMPE220","BMA1",1);
INSERT IGNORE INTO  location VALUES("CMPE321","BMA2",4);
INSERT IGNORE INTO  location VALUES("CMPE350","BMA3",9);

insert ignore into grades Values(3, "CMPE220", 3);
insert ignore into grades Values(2, "CMPE350", 3);
insert ignore into grades Values(3, "CMPE350", 4);
insert ignore into grades Values(3, "CMPE320", 0);
