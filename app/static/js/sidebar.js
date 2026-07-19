//Adding Toggle sidebar

const toggleButton = document.getElementById("sidebar-toggle");
const sidebar = document.querySelector(".sidebar");
const app = document.querySelector(".app-wrapper");
toggleButton.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
    app.classList.toggle("collapsed");

});