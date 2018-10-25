insert into members values ('davood@abc.com','Davood Rafiei','780-111-3333', 'davoodrocks');
insert into members values ('joe@gmail.com','Joe Anderson','780-111-2222', 'joe123');
insert into members values ('mary@abc.com','Mary Smith','780-222-3333', 'lamb321');
insert into members values ('paul@a.com','John Paul','780-333-4444', 'bythepope44');
insert into members values ('mj@gmail.com','Michael Jordan','780-123-4567', 'kobesucks');
insert into members values ('kobe@nba.com','Kobe Bryant','780-999-9999', 'number45isterrible');
insert into members values ('oneeye@trap.ca','Fetty Wap','780-444-1738', 'fettyisgreat');
insert into members values ('drake@papi.com','Drizzy Drake','780-666-1010', 'therealdrake');

insert into cars values (1,'Aston Martin','DB5',1964,1,'davood@abc.com');
insert into cars values (2,'Honda','Civic',2017,4,'joe@gmail.com');
insert into cars values (3,'Nissan','Rogue',2018,4,'mary@abc.com');
insert into cars values (4,'Bugatti Veyron','Sang Noir',2019,2,'drake@papi.com');
insert into cars values (5,'Bentley Continental','GTC V8',2019,4,'drake@papi.com');
insert into cars values (6,'Lamborghini','Aventador',2019,2,'drake@papi.com');
insert into cars values (7,'Honda','Civic',2014,4,'oneeye@trap.ca');
insert into cars values (8,'Ford','F150',2018,4,'oneeye@trap.ca');
insert into cars values (9,'Nissan','Altima',2004,4,'mj@gmail.com');
insert into cars values (10,'BMW','M5',2011,4,'mj@gmail.com');
insert into cars values (11,'Audi','R8',2019,2,'kobe@nba.com');
insert into cars values (12,'Hyundai','Elantra',2000,4,'kobe@nba.com');
insert into cars values (13,'Ferrari','812',2018,2,'kobe@nba.com');
insert into cars values (14,'Honda','Accord',2009,4,'davood@abc.com');
insert into cars values (15,'Ford','Mustang',2007,4,'davood@abc.com');

insert into locations values ('ab1','Edmonton','Alberta','UofA LRT st');
insert into locations values ('ab2','Edmonton','Alberta','Century LRT st');
insert into locations values ('ab3','Edmonton','Alberta',null);
insert into locations values ('ab4','Calgary','Alberta','111 Edmonton Tr');
insert into locations values ('ab5','Calgary','Alberta','Airport');
insert into locations values ('ab6','Red Deer','Alberta','City Hall');
insert into locations values ('ab7','Red Deer','Alberta','Airport');
insert into locations values ('bc1','Vancouver','British Columbia','Stanley Park');
insert into locations values ('bc2','Vancouver','British Columbia','Airport');
insert into locations values ('ab8','Edmonton','Alberta','Muttary Conservatory');
insert into locations values ('ab9','Edmonton','Alberta','West Edmonton Mall');
insert into locations values ('ab10','Calgary','Alberta',null);
insert into locations values ('ab11','Calgary','Alberta',' Saddledome');
insert into locations values ('ab12','Calgary','Alberta','Bankers Hall');
insert into locations values ('ab13','Red Deer','Alberta','Greyhound Station');
insert into locations values ('ab14','Red Deer','Alberta','Costco');
insert into locations values ('bc3','Vancouver','British Columbia','Starlight Casino');
insert into locations values ('bc4','Vancouver','British Columbia','Tacofino');
insert into locations values ('bc5','Vancouver','British Columbia','Yaletown');
insert into locations values ('bc6','Vancouver','British Columbia','Gastown');

insert into rides values (100, 30, '2018-11-12', 3, 'small bag', 'ab1', 'ab4', 'joe@gmail.com', 2);
insert into rides values (101, 30, '2018-11-13', 3, 'small bag', 'ab1', 'ab4', 'joe@gmail.com', null);
insert into rides values (102, 35, '2018-11-12', 2, 'small bag', 'ab2', 'ab8', 'oneeye@trap.ca', 7);
insert into rides values (103, 40, '2018-11-13', 2, 'small bag', 'ab3', 'ab9', 'oneeye@trap.ca', 8);
insert into rides values (104, 45, '2018-11-14', 2, 'big bag', 'ab10', 'ab4', 'kobe@nba.com', 11);
insert into rides values (105, 50, '2018-11-12', 3, 'small bag', 'ab9', 'ab5', 'kobe@nba.com', 12);
insert into rides values (106, 55, '2018-11-13', 3, 'small bag', 'ab14', 'ab13', 'kobe@nba.com', 13);
insert into rides values (107, 60, '2018-11-14', 4, 'big bag', 'ab13', 'ab11', 'mj@gmail.com', 9);
insert into rides values (108, 65, '2018-11-12', 3, 'small bag', 'ab6', 'ab8', 'davood@abc.com', 12);
insert into rides values (109, 70, '2018-11-13', 3, 'small bag', 'ab9', 'ab5', 'mary@abc.com', 3);
insert into rides values (110, 75, '2018-11-14', 3, 'big bag', 'ab2', 'ab11', 'davood@abc.com', 12);
insert into rides values (111, 80, '2018-11-13', 4, 'big bag', 'bc1', 'bc4', 'joe@gmail.com', 2);
insert into rides values (112, 85, '2018-11-12', 3, 'small bag', 'bc2', 'bc5', 'joe@gmail.com', 2);
insert into rides values (113, 90, '2018-11-14', 3, 'small bag', 'bc3', 'bc6', 'joe@gmail.com', null);
insert into rides values (114, 75, '2018-11-11', 3, 'big bag', 'ab2', 'ab11', 'davood@abc.com', 12);
insert into rides values (115, 80, '2018-11-12', 4, 'big bag', 'bc1', 'bc4', 'joe@gmail.com', 2);
insert into rides values (116, 85, '2018-11-14', 3, 'small bag', 'bc2', 'bc5', 'mj@gmail.com', 2);
insert into rides values (117, 90, '2018-11-14', 3, 'small bag', 'bc3', 'bc6', 'kobe@nba.com', null);


insert into bookings values (10, 'davood@abc.com', 100, null, 1, 'ab1', 'ab2');
insert into bookings values (11, 'davood@abc.com', 101, 28, 1, 'ab3', 'ab4');
insert into bookings values (12, 'joe@gmail.com', 102, null, 1, 'ab6', 'ab7');
insert into bookings values (13, 'mary@abc.com', 103, 34, 1, 'ab8', 'ab9');
insert into bookings values (14, 'mj@gmail.com', 104, 28, 1, 'ab10', 'ab11');
insert into bookings values (15, 'paul@a.com', 105, null, 1, 'bc1', 'bc2');
insert into bookings values (16, 'davood@abc.com', 106, 47, 1, 'ab2', 'ab3');
insert into bookings values (17, 'oneeye@trap.ca', 107, 28, 1, 'ab2', 'ab5');
insert into bookings values (18, 'oneeye@trap.ca', 108, 29, 1, 'bc2', 'bc3');
insert into bookings values (19, 'davood@abc.com', 109, null, 1, 'ab2', 'ab14');
insert into bookings values (20, 'oneeye@trap.ca', 110, 28, 1, 'ab2', 'ab5');
insert into bookings values (21, 'mj@gmail.com', 111, 55, 1, 'ab9', 'ab11');
insert into bookings values (22, 'davood@abc.com', 112, null, 1, 'ab2', 'ab13');
insert into bookings values (23, 'kobe@nba.com', 113, 28, 1, 'ab2', 'ab5');
insert into bookings values (24, 'mj@gmail.com', 114, 27, 1, 'ab7', 'ab3');
insert into bookings values (25, 'drake@papi.com', 115, null, 1, 'ab2', 'bc1');
insert into bookings values (26, 'kobe@nba.com', 116, 28, 1, 'ab2', 'ab5');
insert into bookings values (27, 'mj@gmail.com', 117, 30, 1, 'ab1', 'ab9');

insert into enroute values (100, 'ab6');
insert into enroute values (101, 'ab7');
insert into enroute values (102, 'ab6');
insert into enroute values (103, 'bc2');
insert into enroute values (104, 'ab13');
insert into enroute values (105, 'bc4');
insert into enroute values (106, 'ab7');

insert into requests values (1, 'paul@a.com', '2018-12-22', 'ab3', 'bc1', 80);
insert into requests values (2, 'davood@abc.com', '2018-12-24', 'ab1', 'ab7', 30);
insert into requests values (3, 'paul@a.com', '2018-12-20', 'ab1', 'bc3', 75);
insert into requests values (4, 'mj@gmail.com', '2018-12-25', 'bc1', 'bc3', 130);
insert into requests values (5, 'kobe@nba.com', '2018-12-21', 'ab10', 'ab13', 180);
insert into requests values (6, 'mj@gmail.com', '2018-12-24', 'ab4', 'ab14', 30);

INSERT INTO inbox VALUES ('davood@abc.com', '2018-11-03 12:30:34', 'joe@gmail.com', 'I can no longer drive you.', 100, 'y');
INSERT INTO inbox VALUES ('davood@abc.com', '2018-11-03 16:33:12', 'joe@gmail.com', 'Nevermind. I can drive you again.', 100, 'n');
INSERT INTO inbox VALUES ('mary@abc.com', '2018-11-12 13:19:20', 'oneeye@trap.com', 'Should I bring snacks?', 103, 'y');
INSERT INTO inbox VALUES ('mj@gmail.com', '2018-11-15 11:09:59', 'kobe@nba.com', 'I am better than you.', 116, 'y');
INSERT INTO inbox VALUES ('kobe@nba.com', '2018-11-03 11:13:34', 'mj@gmail.com', 'No, you are not better than me.', 116, 'n');
INSERT INTO inbox VALUES ('drake@papi.com', '2018-11-12 11:13:34', 'joe@gmail.com', 'Where are you?', 115, 'y');
INSERT INTO inbox VALUES ('joe@gmail.com', '2018-11-12 11:16:30', 'drake@papi.com', 'I am standing by the fountain', 115, 'n');
INSERT INTO inbox VALUES ('paul@a.com', '2018-11-12 15:43:11', 'kobe@nba', 'I will be there in 10 minutes', 105, 'y');
INSERT INTO inbox VALUES ('davood@abc.com', '2018-11-12 20:00:30', 'mary@abc.com', 'Are you ready?', 109, 'y');
INSERT INTO inbox VALUES ('mary@abc.com', '2018-11-12 20:02:45', 'davood@abc.com', 'Is there room for my friend?', 109, 'n');
INSERT INTO inbox VALUES ('mj@gmail.com', '2018-11-13 09:22:31', 'paul@a.com', 'Is there room on this ride?', 116, 'y');
INSERT INTO inbox VALUES ('paul@a.com', '2018-11-13 010:41:56', 'mj@gmail.com', 'Sorry, there is no more room on this ride.', 116, 'n');