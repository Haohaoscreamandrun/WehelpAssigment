// Task 3: Parse data from internet and render as HTML by JavaScript

// AJAX: Asynchronous JavaScript and XML
// XHR: XML Http Request
let url =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";

fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    let spotObjList = data.data.results;
    // retrieve the first 13 title and pics
    let titleImgList = [];
    for (let i = 0; i < 13; i++) {
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
    for (let i = 0; i < 3; i++) {
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
    let titlesDiv = document.querySelector(".titles");
    for (let i = 3; i < 13; i++){
      //create element
      //parent
      let titleDiv = document.createElement("div");
      titleDiv.classList.add('title');
      titleDiv.id = `title-${i}`;
      titleDiv.style.backgroundImage = `url(${titleImgList[i][1]})`;
      //star-icon
      let titleStar = document.createElement("div");
      titleStar.classList.add('star-icon');
      //words
      let titleWords = document.createElement("div");
      titleWords.classList.add('title-words');
      titleWords.textContent = titleImgList[i][0];
      //append
      titlesDiv.appendChild(titleDiv);
      let currentTitle = document.getElementById(`title-${i}`);
      currentTitle.appendChild(titleStar);
      currentTitle.appendChild(titleWords);
    }
  });

const burger = document.querySelector(".burger-icon");
const closeB = document.querySelector(".close-icon");
const sideBar = document.querySelector(".side-bar");

burger.addEventListener("click", () => {
  sideBar.classList.toggle("active");
});

closeB.addEventListener("click", () => {
  sideBar.classList.toggle("active");
});