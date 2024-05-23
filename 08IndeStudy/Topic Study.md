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
    <script async src="async.js"></script>
    <img
      src="https://images.pexels.com/photos/1388069/pexels-photo-1388069.jpeg?cs=srgb&dl=pexels-wildlittlethingsphoto-1388069.jpg&fm=jpg"
      alt="">
  </div>
  <script>
    for (let i = 0; i <= 3; i++) {
      let parent = document.getElementById("parent")
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

> Async function 如果失去 async attribute會排在圖片載入之前執行

## Topic 2: CSS Selector Naming

> OOCSS, SMACSS, and BEM are 3 common naming guidelines for CSS Selector. These guidelines help us write more readable CSS code

1. Introduce the concepts of OOCSS, SMACSS, and BEM naming guidelines.
2. Tell us which naming guideline is your favorite, and give an example to demonstrate
the main concept of that guideline. For example, you can demo how to apply the
OOCSS naming guideline to the CSS code in our week 1 tasks.

## Topic 3: Data Verification

> Data verification is a very important feature for our web system. We have a lot of small but critical work to do, both in the front-end and the back-end

1. In the front-end, we have to verify input data format before sending data to the back-end.
2. In the back-end, we have to receive data from the front-end and verify if it matches the expected format, before we use it to do any critical operations.
3. For password format verification procedure, we want to verify if the length of password is between 4 ~ 8, and only includes English alphabets, numbers, and one of following special letters: @#$%, both in the front-end and the back-end.
4. In a web system, why do we want to do data verification in the front-end? And why do we have to do data verification in the back-end even if we have done it in the front-end.

### Front-end AUTO validation

> ```<form> 的 <input>```tag有很多可以幫助自動驗證使用者輸入的type和attributes。

#### Input type

+ Input type - date, 使用者必須輸入包含日期的字串，無法輸入非數字文字。會出現日期選擇器幫助使用者選擇。也可以加入```max, min```控制範圍。```type="datetime-local"```則另外加入無時區的時間選擇；而```type="month"```則是出現只包含年份及月份的選擇器。

   ```html
    <label for="birthday">出生日期</label>
    <input type="date" id="birthday" name="birthday" max="2024-05-01" min="1900-01-01"> <br>
   ```

+ Input type - Email, 根據使用的瀏覽器不同，輸入的電郵地址可能會被自動驗證。目前測試只會驗證是否有包含```@```及前後字串，如以下的正則表達式:```/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/```
+ Input type - File, 顯示能夠選擇及上傳檔案的按鈕。
+ Input type - Number, 只能接受數字輸入並有調整按鈕，依樣可以限制最大值及最小值。

#### Input attribute

+ maxlength attribute, 限定輸入最大字數，但不會顯示任何警示。
+ min/max attribute, 在```type="number/range/date/datetime-local/month/time/week"```的情況下可以套用限制最大值及最小值。
+ multiple attribute, 在```type="email/file"```情況下，使用者可以輸入以逗號分隔的電子郵件或選擇兩個及以上的檔案。
+ pattern attribute, 在```type=" text/date/search/url/tel/email/password"```的情況下，以正則表達式的方式規範輸入樣態。```title=""```可以顯示不符樣態時的警告訊息。
+ required attribute, 在```type=" text/date picker/search/url/tel/email/password/number/checkbox/radio/file"```的情況下阻擋未填入送出。

#### Front-end AUTO validation of the password in point 3

```html
<form action="" onsubmit="checkPassword(event)">
  <label for="password">密碼</label>
  <input type="password" name="password" id="password" pattern="[a-zA-Z0-9@#$%]{4,8}" title="請輸入4-8位包含英文大小寫或@#$%符號之密碼"> <br>
  <input type="submit" value="submit">
</form>
```

### Front-end Javascript validation

> 上述的自動驗證都可以透過Javascript完成。

#### Front-end javascript validation of the password in point 3

```javascript
function checkPassword(event){
  event.preventDefault()
  let password = document.getElementById('password').value
  let pattern = new RegExp('[a-zA-Z0-9@#$%]{4,8}')
  if (pattern.test(password)){
    let form = document.getElementById("form")
    form.action = "/signin"
    form.method = "post"
  } else {
    alert("輸入之密碼須符合以下條件：4-8位包含英文大小寫或@#$%符號")
  }
}
```

### Back-end validation

#### FastAPI validation of the password in point 3

> 以Pydantic的field_validator舉例如何進行後端驗證

```py
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo
import os, re
app = FastAPI()
@app.get("/") #直接把首頁mount成static檔案雖然可以讀取，但打不出POST request，待研究
def root():
   # Get the directory of the current file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the file path to index.html
    index_html_path = os.path.join(current_dir, "index.html")
    # Return the index.html file as a response
    return FileResponse(index_html_path)
class Userdata(BaseModel):
    password: str
    @field_validator('password')
    def password_rules(cls, v, info: FieldValidationInfo):
       if len(v) < 4 or len(v) > 8:
          raise ValueError("Length of password should be >= 4 and <= 8")
       elif len(re.findall('[^a-zA-Z0-9@#$%]', v)) > 0:
          raise ValueError("Password should only contain a-z, A-Z, 0-9 and #,$,%,@")
       else:
          return v

@app.post("/signin", response_class= JSONResponse)
async def validation(request: Request, password: Userdata):
    try:
      print("Password received:", password)
      return {"message": "Password received"}
    except (Exception, ValueError) as e:
      print("Not success:", str(e))
```

### The reason to do both front-end and back-end validation

> 前端驗證僅為照顧使用者體驗，可以協助使用者判斷輸入是否符合後端需求。但只要開啟瀏覽器的console，再透過執行無驗證程序的fetch，即可繞過前端驗證直接將不合規格的輸入送去後端。

![01. Bypass front end validation](/08IndeStudy/Screenshots/Topic3/01.%20Bypass%20front%20end%20validation.png)

> 如上圖，後端已經確實收到不合規格的資料```input:"1"```，但因為有後端驗證而被擋下，顯示```ValueError```錯誤訊息。

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

### 跨站請求偽造 Cross Site Request Forgery, CSRF

+ 原本的伺服器是無條件相信cookie的資料，而沒有再進行驗證。
+ 跨站請求偽造步驟：
  1. 使用者登入合法網站，合法網站發出cookie存至使用者瀏覽器。
  2. 使用者在未登出的情況下，以其他分頁瀏覽惡意網站。
  3. 惡意網站同樣可以使用瀏覽器中的cookie，該惡意網站以該cookie向合法網站發送請求。

### 同源政策 Same Origin Policy

+ 現存所有瀏覽器皆實作同源政策以防止跨站請求偽造。
+ Client-side只能向相同來源的資源發送request，相同來源的定義為：
  1. 相同通訊協定(Same Protocol)
  2. 相同網域(Same Domain)
  3. 相同通訊埠(Same Port)
+ 只要請求發送的網域不符合上述規則，瀏覽器CORS會報錯

以目前的使用者URL```http://127.0.0.1:8000/```來說：

```javascript
1. 'https://127.0.0.1:8000/' //通訊協定不同
2. 'http://example.com:8000/' //網域不同
3. 'http://127.0.0.1:5000/' //通訊埠不同
```

### 跨來源資源共用 Cross-Origin Resource Sharing, CORS

+ 實務上不可能避免請求非同源資源，例如從影片平台API提取影片、使用公共字型庫或顯示全國氣象資料等。
+ 為了請求非同源的資源，瀏覽器必須要在```headers```中放入CORS安全列表請求標頭。
  + 其中```Origin: 當前URL```可告知請求來源。
+ 伺服器收到後，在```response```的```headers```中```Access-Control-Allow-Origin```加上當前url。
  + 開發人員首先在其伺服器上設定CORS標頭，方法是將該url新增到允許的來源清單。

  ```plaintext
  組態清單
  Access-Control-Allow-Origin: https://news.example.com
  ```

  + 對於之後每個請求，伺服器將以```Access-Control-Allow-Credentials : "true"```進行回應。
+ 除```GET, HEAD, POST```三個簡單請求之外，瀏覽器會先發送一次請求、稱預檢請求(Preflighted request)。
  + 因源政策只會擋回應，不會擋請求，所以假如某個惡意攻擊者發送```DELETE```的請求，同源政策不會擋下這個請求。
  + 預檢請求的方法是```OPTIONS```，一旦預檢請求成功完成，真正的請求才會被送出。
  + 伺服器在回應預檢請求時，可以在 ```Access-Control-Max-Age``` 標頭帶上預檢請求回應快取的秒數，也就是說，在這個秒數之內，預檢請求會被快取，在該秒數內不需要再額外發送預檢。

### 實作

#### 是否可以從Local host執行跨域請求?

##### Request from Google

> 會獲得CORS報錯，截圖如下：
  ![01. CORS error screenshot](/08IndeStudy/Screenshots/Topic4/01.%20CORS%20error%20screenshot.png)
  ![04. Failed fetch response header](/08IndeStudy/Screenshots/Topic4/04.%20Failed%20fetch%20response%20header.png)

##### Request from Padax JSON

> 成功取得JSON，截圖如下：
  ![02. Success retrieve of json](/08IndeStudy/Screenshots/Topic4/02.%20Success%20retrieve%20of%20json.png)
  ![03. Success fetch response header](/08IndeStudy/Screenshots/Topic4/03.%20Success%20fetch%20response%20header.png)

##### Difference between 2 respond

1. Padax的回應標頭中，```Access-Control-Allow-Origin: *```萬用字符代表該資源可以被任何來源存取。
2. Padax的回應標頭中，沒有```Access-Control-Allow-Credentials : "true"```可能是因為```Access-Control-Allow-Origin: *```並未單獨列出請求網址。
3. Google回應標頭中並沒有出現任何```Access-Control```相關的內容，且根據CORS錯誤訊息，```Access-Control-Allow-Origin```並沒有在標頭中。

##### Shared APIs to other domains

1. Set up a server by FastAPI host on 127.0.0.2:9000.
2. Set up another server on 127.0.0.1:8000 as a client.
3. Mount a CORS middleware on server:

    ```py
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi import FastAPI, Form, Request
    from fastapi.responses import FileResponse
    import os
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    @app.get("/")
    def root():
      # Get the directory of the current file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Construct the file path to index.html
        index_html_path = os.path.join(current_dir, "server.html")
        # Return the index.html file as a response
        return FileResponse(index_html_path)
    ```

4. ```fetch``` from client to server as a cross origin request.

    ```javascript
    async function CORS(event){
          try {
            let response = await fetch("http://127.0.0.2:9000",{
              method: "GET",
            });
          if (!response.ok) {
              throw new Error('Network response was not ok');
            }
          let text = await response.json();
          console.log("Response Text:", text);
          } catch (error){
            console.error('There was a problem with the fetch operation:', error);
          }
        }
    ```

5. Success sharing API to other domains

    ![05. Success sharing APIs with CORSmiddleware](/08IndeStudy/Screenshots/Topic4/05.%20Success%20sharing%20APIs%20with%20CORSmiddleware.png)

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
