# Week 8 - Topic Study

## Topic 1: HTML ```<script>``` Attributes

> There are 2 attributes, defer and async, that we can use in ```<script>``` tag to change the script loading and executing behavior

1. What happens If we add a defer attribute to a ```<script>``` tag?
2. What happens If we add an async attribute to a ```<script>``` tag?
3. When to use these 2 attributes? Could you give us code examples to illustrate the
use cases for these 2 attributes?

## Topic 2: CSS Selector Naming

> OOCSS, SMACSS, and BEM are 3 common naming guidelines for CSS Selector. These guidelines help us write more readable CSS code

1. Introduce the concepts of OOCSS, SMACSS, and BEM naming guidelines.
2. Tell us which naming guideline is your favorite, and give an example to demonstrate
the main concept of that guideline. For example, you can demo how to apply the
OOCSS naming guideline to the CSS code in our week 1 tasks.

## Topic 3: Data Verification

> Data verification is a very important feature for our web system. We have a lot of small but critical work to do, both in the front-end and the back-end

1. In the front-end, we have to verify input data format before sending data to the
back-end.
2. In the back-end, we have to receive data from the front-end and verify if it matches
the expected format, before we use it to do any critical operations.
3. For password format verification procedure, we want to verify if the length of
password is between 4 ~ 8, and only includes English alphabets, numbers, and one
of following special letters: @#$%, both in the front-end and the back-end.
4. In a web system, why do we want to do data verification in the front-end? And why do
we have to do data verification in the back-end even if we have done it in the
front-end.

## Topic 4: Fetch and CORS

> Using built-in JavaScript fetch function, we can send HTTP requests to the back-end and get HTTP responses without refreshing or redirecting the page. Cross Origin Resource Sharing (CORS) concept plays a critical role if we want to send a request to a different domain with the fetch function

1. What is CORS?
2. Can we use the fetch function in our localhost page, to send a request to
<https://www.google.com/> and get a response?
3. Can we use the fetch function in our localhost page, to send a request to
<https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json>
and get a response? Compared to the previous case, what’s the difference?
4. How to share APIs we developed to other domains, just like what we experienced in
step 3. Could you give us an example?

## Topic 5: Primary Key and Index

> For dramatically speeding up data query operation, we can set up the Primary Key or Index to columns in a table.

1. What is Primary Key and Index? And why do we want to use them?
2. How to properly set up the Index for speeding up the following SQL query:
```SELECT * FROM member WHERE username='test' and password='test'```
3. How to verify that our set up Index really works?
4. Why can Index significantly speed up query?
5. Can Index speed up SQL query using the LIKE feature?

## Topic 6: Connection Pool

> The standard procedure to work with databases is: connect, execute SQL statements, and
finally close the connection. Connection Pool is a programming technique to make the connection between back-end system and database more stable, and increase overall
throughput.

1. What is Connection Pool? Why do we want to use Connection Pool?
2. How to create a Connection Pool by the official mysql-connector-python package?
3. If we want to make database operations, we get a connection from Connection Pool,
execute SQL statements, and finally return connection back to the Connection Pool.
Demo your code which implements the above procedure.

## Topic 7: Cross-Site Scripting (XSS)

> Cross-Site Scripting (XSS) is one of the most common attack methods. Try to study the
basic concept, replicate the attack steps, and tell us how to prevent this kind of attack from the developer’s view.

1. What is XSS?
2. You are a hacker! Design and do a real XSS attack on a web system. Show us your
work.
3. Based on the scenario you did in the previous step, how could it be prevented?
