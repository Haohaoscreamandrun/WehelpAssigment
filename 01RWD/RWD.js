const burger = document.querySelector('.burger-icon')
const closeB = document.querySelector('.close-icon')
const sideBar = document.querySelector('.side-bar')

burger.addEventListener('click', () =>{
  sideBar.classList.toggle('active')
})

closeB.addEventListener('click', () =>{
  sideBar.classList.toggle('active')
})