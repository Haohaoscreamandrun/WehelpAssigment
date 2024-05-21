for (let i = 0; i <= 3; i++) {
  let parent = document.getElementById("parent")
  let p = document.createElement("p");
  p.innerText = `Async ${i} times`;
  parent.appendChild(p);
}
console.log("async function complete")