document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    const app = document.querySelector(".app-wrapper");

    if (!toggleButton || !sidebar || !app) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        const isCollapsed = sidebar.classList.toggle("collapsed");
        app.classList.toggle("collapsed", isCollapsed);
        toggleButton.setAttribute("aria-expanded", String(!isCollapsed));
    });
});
