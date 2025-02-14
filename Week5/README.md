# Week 5 Assignment

## Task 1. Install MySQL server
![INSTALL SCREENSHOT](Week5/assets/1_Install.png "INSTALL")

## Task 2. Create database and table in your MySQL server

### Create a new database named website.
```
CREATE DATABASE website;
SHOW DATABASES;
USE website;
```
![CREATE DATABASE](Week5/assets/2.1_Create_Use.png "CREATE DATABASE")
### Create a new table named member, in the website database, designed as below:
```
CREATE TABLE member (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```
![CREATE TABLE](Week5/assets/2.2_Create_Table.png "CREATE TABLE")

## Task 3. SQL CRUD

### INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
![INSERT INTO](Week5/assets/3.1_Insert_Member_Data.png "INSERT MEMBER")
```
INSERT INTO member (name, username, password, follower_count)
    -> VALUES ('test', 'test', 'test', 1);
INSERT INTO member (name, username, password, follower_count)
    -> VALUES ('One', 'member_1', 'pwd_01', 13), ('Two', 'member_2', 'pwd_02', 7), ('Three', 'member_3', 'pwd_03', 8), ('Four', 'member_4', 'pwd_04', 22);
```
### SELECT all rows from the member table.
```
SELECT * FROM member;
```
![SELECT ALL](Week5/assets/3.2_Select_All_Rows.png "SELECT ALL ROW")
### SELECT all rows from the member table, in descending order of time.
```
SELECT * FROM member
    -> ORDER BY time DESC;
```
![SELECT ORDER](Week5/assets/3.3_Select_DESC.png "SELECT ORDRE DESC")
### SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
```
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```
![SELECT LIMIT OFFSET](Week5/assets/3.4_Select_Offset_Limit.png "SELECT LIMIT OFFSET")
### SELECT rows where username equals to test.
```
SELECT * FROM member WHERE username='test';
```
![SELECT 'test'](Week5/assets/3.5_Select_Test.png "SELECT TEST")
### SELECT rows where name includes the es keyword.
```
SELECT * FROM member WHERE name LIKE '%es%';
```
![SELECT '%es%'](Week5/assets/3.6_Select_ES.png "SELECT ES")
### SELECT rows where both username and password equal to test.
```
SELECT * FROM member WHERE username='test' AND password='test';
```
![SELECT USERNAME & PWD](Week5/assets/3.7_Select_USERNAME_PWD.png "SELECT USERNAME PWD")
### UPDATE data in name column to test2 where username equals to test.
```
UPDATE member SET name='test2' WHERE username='test';
```
![UPDATE](Week5/assets/3.8_Update.png "UPDATE")

## Task 4. SQL Aggregation Functions
### SELECT how many rows from the member table.
```
SELECT COUNT(*) FROM member;
```
![COUNT](Week5/assets/4.1_Count.png "COUNT")
### SELECT the sum of follower_count of all the rows from the member table.
```
SELECT SUM(follower_count) FROM member;
```
![SUM](Week5/assets/4.2_Sum.png "SUM")
### SELECT the average of follower_count of all the rows from the member table.
```
SELECT AVG(follower_count) FROM member;
```
![AVG MEMBER](Week5/assets/4.3_Average.png "AVG MEMBER")
### SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
```
SELECT AVG(follower_count)
    -> FROM member
    -> ORDER BY follower_count DESC LIMIT 2;
```
![AVG MEMBER FIRST 2](Week5/assets/4.4_Average_2.png "AVG MEMBER 2")

## Task 5. SQL JOIN
### Create a new table named message, in the website database. designed as below:
```
CREATE TABLE message (
    ->     id BIGINT NOT NULL AUTO_INCREMENT,
    ->     member_id BIGINT NOT NULL,
    ->     content VARCHAR(255) NOT NULL,
    ->     like_count INT UNSIGNED NOT NULL DEFAULT 0,
    ->     time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->     PRIMARY KEY (id),
    ->     FOREIGN KEY (member_id) REFERENCES member(id)
    -> ) ENGINE = InnoDB;
```
![NEW TABLE MSG](Week5/assets/5.1_Create_Table_message.png "ADD message")
### SELECT all messages, including sender names. We have to JOIN the member table to get that.
```
INSERT INTO message (member_id, content, like_count)
    -> VALUES
    -> (3, 'Good morning!', 13),    
    -> (1, 'Test Message 1', 9),
    -> (4, 'Good afternoon!', 5),
    -> (2, 'Good night!', 1),
    -> (5, 'Where are you', 8);
```
![JOIN](Week5/assets/5.2_Join.png "JOIN")
### SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
```
SELECT message.id, member.name AS sender_id, message.content, message.like_count, message.time
    -> FROM message
    -> INNER JOIN member ON message.member_id = member.id;
```
![JOIN TEST](Week5/assets/5.3_Join_2.png "JOIN TEST")
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
```
SELECT message.id, member.username AS sender_name, message.content, message.like_count, message.time
    -> FROM message
    -> INNER JOIN member ON message.member_id = member.id
    -> WHERE member.username = 'test';
```
![JOIN AVG TEST](Week5/assets/5.4_Join_AVG_test.png "JOIN AVG TEST")
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
```
SELECT member.username, AVG(message.like_count) AS avg_like_count
    -> FROM message
    -> INNER JOIN member ON message.member_id = member.id
    -> GROUP BY member.username;
```
![JOIN AVG GROUP](Week5/assets/5.5_Join_AVG_group.png "JOIN AVG GROUP")


