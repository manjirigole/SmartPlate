document.addEventListener("DOMContentLoaded", function () {
  const check = document.getElementById("check");
  const nav2Ul = document.querySelector(".navbar");

  document.querySelector(".fa-bars").addEventListener("click", function () {
    // Toggle the class to switch between column and row
    nav2Ul.classList.toggle("column");
    nav2Ul.classList.display("column");
    nav2Ul.classList.display("none");
    if (window.getComputedStyle(nav2Ul).display === "none") {
      nav2Ul.style.display = "block";
    } else {
      nav2Ul.style.display = "none";
    }
  });

  const nav2Items = document.querySelectorAll("nav-element");
  nav2Items.forEach(function (item) {
    item.addEventListener("click", function () {
      nav2Ul.style.display = "none";
      check.checked = false;
    });
  });
});

