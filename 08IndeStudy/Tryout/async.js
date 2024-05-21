for (let i = 0; i <= 3; i++) {
  let p = document.createElement("p");
  p.innerText = `Async ${i} times`;
  parent.appendChild(p);
}
console.log("async function complete")