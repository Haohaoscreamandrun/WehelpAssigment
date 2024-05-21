# Week 8 - Topic Study

## Topic 1: HTML ```<script>``` Attributes

> There are 2 attributes, defer and async, that we can use in ```<script>``` tag to change the script loading and executing behavior

1. What happens If we add a defer attribute to a ```<script>``` tag?
2. What happens If we add an async attribute to a ```<script>``` tag?
3. When to use these 2 attributes? Could you give us code examples to illustrate the use cases for these 2 attributes?

### Answer

#### History: When is the attribute added and why?

+ 預設情況下，瀏覽器解析HTML時，只要讀到```<script>```就會暫停解析文件物件模型(Document Object Model, DOM)，向```<script scr="...">```中的位址請求資源，並在下載完成後立刻執行。這樣的特性可能衍生幾種問題：
  + ```<script>```被放在前面，欲操作的DOM尚未被解析，```<script>```內的程式無法順利運作。

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
  </head>
  <body>
    <script src="/08IndeStudy/Tryout/tryout.js"></script>
    Hello World!
    <div id="operate"></div>
  <!-- <script src="/08IndeStudy/Tryout/tryout.js"></script> -->
  </body>
  </html>
  ```

  ```js
  // try to manipulate the lines after <script>
  let device = document.getElementById("operate")
  device.innerHTML = "My name is HaoHao"
  ```

  ![01. manipulate DOM before analyzed ](/08IndeStudy/Screenshots/Topic1/01.%20manipulate%20DOM%20before%20analyzed%20.png)
  
  + 上述問題可以透過將```<script>```放在```<body>```閉合處解決，但在更複雜龐大的網站中資源檔案越來越大，下載或執行過久會導致卡畫面，使用者體驗不佳。(以```setTimeout()```模擬載入時間過久)
  
  ```js
  // use setTimeout() as mimic of larger js file
  setTimeout(nameDiv, 5000)
  function nameDiv(){
    let device = document.getElementById("operate")
    device.innerHTML = "My name is HaoHao"
  }
  ```

  ![02. script takes time to load](/08IndeStudy/Screenshots/Topic1/02.%20script%20takes%20time%20to%20load.png)

+ 在HTML4和HTML5中，```<script>```多了```defer async```兩種屬性，皆是用於幫助開發者控制外源```<script>```資源的載入及執行順序，避免上述情形。

#### The function of defer and async attribute

![03. runtime of different script attribute](/08IndeStudy/Screenshots/Topic1/03.%20runtime%20of%20different%20script%20attribute.png)

##### Similarity

+ 解析HTML遇到```<script src="..." defer> or <script src="..." async>```時，在背景執行下載而不阻擋瀏覽器建立DOM，使用者可以先看到網頁內容。
+ 只對外部載入的```<script>```有效，inline script會直接被執行。

##### ```<script src="..." defer>```

+ DOM全部建立完成才開始執行。
+ 同樣有defer attribute的```<script src="..." defer>```會依照排列順序依次執行，無論下載完成與否。
+ 適用於會操作HTML element或是其他```<script>```的，可以放在```<header>```盡早完成下載，但要注意順序。

##### ```<script src="..." async>```

+ 只要下載完成就開始執行，停止執行建立DOM。
+ ```<script src="..." async>```之間無法保證執行順序，和其他```<script>```也沒有排序，只要下載好就會執行。
+ 適用於與DOM無關的```<script>```，如獨立第三方的```<script>```

#### Examples

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Script Defer Attribute Example</title>
  <script defer src="defer.js"></script>
</head>

<body>
  <h1>Script Defer/Async Attribute Example</h1>
  
  <div id="parent">
  <img
    src="https://images.pexels.com/photos/1388069/pexels-photo-1388069.jpeg?cs=srgb&dl=pexels-wildlittlethingsphoto-1388069.jpg&fm=jpg"
    alt="">
  </div>
  <script async src="async.js"></script>
  
  <script>
    let parent = document.getElementById("parent")
    for (let i = 0; i <= 3; i++) {
      let p = document.createElement("p");
      p.innerText = `Inline ${i} times`;
      parent.appendChild(p);
    }
    console.log("Inline function complete")
  </script>

</body>

</html>
```

![04. Examples](/08IndeStudy/Screenshots/Topic1/04.%20Examples.png)

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
