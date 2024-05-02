SQL Commands and screenshots
===
# Content
1. [Task 2: Create database and table in your MySQL server](#task-2-create-database-and-table-in-your-mysql-server)
2. [Task 3. SQL CRUD](#task-3-sql-crud)
3. [Task 4. SQL Aggregation Functions](#task-4-sql-aggregation-functions)
4. [Task 5. SQL JOIN](#task-5-sql-join)
5. [Use mysqldump command to export the website database to a file named data.sql,putting it in the week5 folder](#task-6-use-mysqldump-command-to-export-the-website-database-to-a-file-named-datasqlputting-it-in-the-week5-folder)
***
## Task 2: Create database and table in your MySQL server
### Q1. Create a new database named website.
```sql
mysql> create database website;
Query OK, 1 row affected (0.00 sec)

mysql> use website;
Database changed
```
### Q2. Create a new table named member, in the website database, designed as below:
| Column Name | Data Type | Additional Settings | Description |
|:--|:--|:--|:--|
|id|bigint|primary key, auto increment|Unique ID|
|name|varchar(255)|not null|Name|
|username|varchar(255)|not null|Username|
|password|varchar(255)|not null|Password|
|follower_count|int unsigned|not null, default to 0|Follower Count|
|time|datetime|not null, default to current time|Signup time|
```sql
mysql> create table member (id bigint auto_increment,
    -> name varchar(255) not null,
    -> username varchar(255) not null,
    -> password varchar(255) not null,
    -> follower_count int unsigned not null default 0,
    -> time datetime not null default current_timestamp on update current_timestamp,
    -> primary key (id));
Query OK, 0 rows affected (0.01 sec)
```
![Task2.Q1](/05MySQL/screenshots/Task2_screenshots.png)
## Task 3. SQL CRUD
### Q1. INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
### Q2. SELECT all rows from the member table.
```sql
mysql> insert into member (name, username, password)
    -> values ('test', 'test', 'test');
mysql> insert into member (name, username, password)
    -> values ('Karl Jablonski', 'Jabber', 'ja222ski222');
Query OK, 1 row affected (0.00 sec)

mysql> insert into member (name, username, password)
    -> values ('Matti Karttunen', 'Kartti', 'mk69696');
Query OK, 1 row affected (0.00 sec)

mysql> insert into member (name, username, password)
    -> values ('Zbyszek', 'Wolski', 'rotinhell666');
Query OK, 1 row affected (0.00 sec)

mysql> insert into member (name, username, password)
    -> values ('Tom B. Erichsen', 'Cardinal', 'happyhellowin123');
Query OK, 1 row affected (0.00 sec)
mysql> select * from member;
```
![Task3.Q1Q2](/05MySQL/screenshots/Task3_1_screenshots.png)
### Q3. SELECT all rows from the member table, in descending order of time.
```sql
mysql> select * from member
    -> order by time desc;
```
![Task3.Q3](/05MySQL/screenshots/Task3_21_screenshots.png)
### Q4. SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
```sql
mysql> select * from member
    -> order by time desc
    -> limit 3 offset 1;
```
![Task3.Q4](/05MySQL/screenshots/Task3_2_screenshots.png)
### Q5. SELECT rows where username equals to test.
```sql
mysql> select * from member
    -> where username = 'test';
```
### Q6. SELECT rows where name includes the es keyword.
```sql
mysql> select * from member
    -> where name like '%es%';
```
![Task3.Q5Q6](/05MySQL/screenshots/Task3_3_screenshots.png)
### Q7. SELECT rows where both username and password equal to test.
```sql
mysql> select * from member
    -> where username = 'test' and password = 'test';
```
![Task3.Q7](/05MySQL/screenshots/Task3_41_screenshots.png)
### Q8. UPDATE data in name column to test2 where username equals to test.
```sql
mysql> update member
    -> set name = 'test2'
    -> where username = 'test';
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> select * from member
    -> where name = 'test2';
```
![Task3.Q8](/05MySQL/screenshots/Task3_4_screenshots.png)
## Task 4. SQL Aggregation Functions
### Q1. SELECT how many rows from the member table.
```sql
mysql> select count(*) from member;
```
### Q2. SELECT the sum of follower_count of all the rows from the member table.
```sql
mysql> update member
    -> set follower_count = 2100
    -> where id = 2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> update member
    -> set follower_count = 101
    -> where id = 3;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> update member
    -> set follower_count = 99999
    -> where id = 4;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> update member
    -> set follower_count = 9
    -> where id = 5;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> select sum(follower_count) from member;
```
### Q3. SELECT the average of follower_count of all the rows from the member table.
```sql
mysql> select avg(follower_count) from member;
```
![Task4.Q1Q2Q3](/05MySQL/screenshots/Task4_1_screenshots.png)
### Q4. SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
```sql
mysql> select avg(follower_count)
    -> from (
    -> select follower_count
    -> from member
    -> order by follower_count desc
    -> limit 2
    -> ) as top_2;
```
![Task4.Q4](/05MySQL/screenshots/Task4_2_screenshots.png)
## Task 5. SQL JOIN
### Q1. Create a new table named message, in the website database. designed as below:
| Column Name | Data Type | Additional Settings | Description |
|:--|:--|:--|:--|
|id|bigint|primary key, auto increment|Unique ID|
|member_id|bigint|not null, foreign key refer to id column in member table|MemberID for message Sender|
|content|varchar(255)|not null|Content|
|like_count|int unsigned|not null, default to 0|Like Count|
|time|datetime|not null, default to current time|Publish time|
```sql
mysql> create table message
    -> (id bigint auto_increment,
    -> member_id bigint not null,
    -> content varchar(255) not null,
    -> like_count int unsigned not null default 0,
    -> time datetime not null default current_timestamp on update current_timestamp,
    -> primary key (id),
    -> foreign key (member_id) references member(id)
    -> );
Query OK, 0 rows affected (0.01 sec)
mysql> describe message;
```
![Task5.Q1](/05MySQL/screenshots/Task5_2_screenshots.png)
### Inert 5 messages
```sql
mysql> insert into message (member_id, content, like_count)
    -> values
    -> (1, 'Living my best life! #YOLO', 1234),
    -> (2, 'Brunch vibes with the squad 🥑🍳 #SundayFunday', 987),
    -> (3, 'Netflix & chill kind of night 🍿📺 #RelaxMode', 1650),
    -> (4, 'Crushing those goals, one latte at a time ☕️💪 #HustleHard', 823),
    -> (5, 'Selfie game strong 💁📸 #OOTD', 2056);
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0
```
### Q2. SELECT all messages, including sender names. We have to JOIN the member table to get that.
```sql
mysql> select member.id, member.name, message.content
    -> from member
    -> inner join message on member.id = message.member_id;
```
![Task5.Q2](/05MySQL/screenshots/Task5_4_screenshots.png)
### Q3. SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
```sql
mysql> select member.id, member.name, message.content
    -> from member
    -> inner join message on member.id = message.member_id
    -> where member.username = 'test';
```
### Q4. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
```sql
mysql> select avg(message.like_count) as average_like_count
    -> from message
    -> join member on member.id = message.member_id
    -> where member.username = 'test';
```
![Task5.Q3Q4](/05MySQL/screenshots/Task5_5_screenshots.png)
### Q5. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username
```sql
mysql> select member.username, avg(message.like_count) as average_like_counts
    -> from message
    -> join member on member.id = message.member_id
    -> group by member.username;
```
![Task5.Q5](/05MySQL/screenshots/Task5_6_screenshots.png)
## Task 6. Use mysqldump command to export the website database to a file named data.sql,putting it in the week5 folder
```shell
mysql> \q
Bye

C:\Program Files\MySQL\MySQL Server 8.4\bin>mysqldump
Usage: mysqldump [OPTIONS] database [tables]
OR     mysqldump [OPTIONS] --databases [OPTIONS] DB1 [DB2 DB3...]
OR     mysqldump [OPTIONS] --all-databases [OPTIONS]
For more options, use mysqldump --help

C:\Program Files\MySQL\MySQL Server 8.4\bin>mysqldump -u root -p website > C:\Users\Jimmy\Github\Wehelp\WeeklyAssignment\05MySQL\data.sql
Enter password: *********
```