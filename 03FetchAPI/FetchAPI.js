// Task 3: Parse data from internet and render as HTML by JavaScript

// AJAX: Asynchronous JavaScript and XML
// XHR: XML Http Request
let url =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
let leftList = [];

fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    let spotObjList = data.data.results;
    // retrieve the first 13 title and pics
    let titleImgList = [];
    for (let i = 0; i < spotObjList.length; i++) {
      titleImgList.push([
        spotObjList[i].stitle,
        "https" + spotObjList[i].filelist.split("https")[1],
      ]);
    }
    return titleImgList;
  })
  .then(function (titleImgList) {
    // promotion
    let prmotionsDiv = document.querySelector(".promotions");
    let loadLoop = 3;
    for (let i = 0; i < loadLoop; i++) {
      // create element
      // parent
      let promoDiv = document.createElement("div");
      promoDiv.classList.add("promotion");
      promoDiv.id = `promo-${i}`;
      // pic
      let promoPicDiv = document.createElement("div");
      promoPicDiv.classList.add("promo-pic");
      promoPicDiv.style.backgroundImage = `url(${titleImgList[i][1]})`;
      // title
      let promoTitleDiv = document.createElement("div");
      promoTitleDiv.classList.add("promo-title");
      promoTitleDiv.textContent = titleImgList[i][0];
      // appendchild
      prmotionsDiv.appendChild(promoDiv);
      let currentPromo = document.getElementById(`promo-${i}`);
      currentPromo.appendChild(promoPicDiv);
      currentPromo.appendChild(promoTitleDiv);
    }
    leftList = titleImgList.slice(loadLoop);
    console.log(leftList.length)
    return leftList;
  })
  .then(data => {
    loadTitle(data);
  });

function loadTitle(titleImgList) {
  // title
  let titlesDiv = document.querySelector(".titles");
  let loadLoop
  leftList.length >= 10 ? (loadLoop = 10) : (loadLoop = leftList.length);
  for (let i = 0; i < loadLoop; i++) {
    //create element
    //parent
    let titleDiv = document.createElement("div");
    titleDiv.classList.add("title");
    //titleDiv.id = `title-${i}`;
    titleDiv.style.backgroundImage = `url(${titleImgList[i][1]})`;
    //star-icon
    let titleStar = document.createElement("div");
    titleStar.classList.add("star-icon");
    //words
    let titleWords = document.createElement("div");
    titleWords.classList.add("title-words");
    titleWords.textContent = titleImgList[i][0];
    //append
    titlesDiv.appendChild(titleDiv);
    let currentTitle = document.querySelector('.title:last-of-type');
    currentTitle.appendChild(titleStar);
    currentTitle.appendChild(titleWords);
  }
  //leftList.length >= loadLoop
    //? (leftList = titleImgList.slice(loadLoop))
    //: (leftList = []);
  leftList = titleImgList.slice(loadLoop);
}


// side bar function & load more function
const burger = document.querySelector(".burger-icon");
const closeB = document.querySelector(".close-icon");
const sideBar = document.querySelector(".side-bar");
const loadMore = document.querySelector("#load-more");


burger.addEventListener("click", () => {
  sideBar.classList.toggle("active");
});

closeB.addEventListener("click", () => {
  sideBar.classList.toggle("active");
});

loadMore.addEventListener("click", () => {
  leftList.length > 0 ? loadTitle(leftList): loadMore.textContent = "No More";
});