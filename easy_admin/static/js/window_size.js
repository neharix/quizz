let window_height = window.innerHeight;
let navbar = document.getElementById("navbar");
let sidebar = document.getElementById("sidebar");
let footer = document.getElementById("footer");

let navbar_height = navbar.clientHeight;
let footer_height = footer.clientHeight;

let sidebar_height = window_height - navbar_height - footer_height;
sidebar.style.height = String(sidebar_height) + "px";

window.addEventListener("resize", function() {

    let window_height = window.innerHeight;
    let navbar_height = navbar.clientHeight;
    let footer_height = footer.clientHeight;
    let sidebar_height = window_height - navbar_height - footer_height;
    sidebar.style.height = String(sidebar_height) + "px";
});