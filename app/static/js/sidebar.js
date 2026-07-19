document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("sidebar-toggle");
    const toggleIcon = toggleButton?.querySelector("i");
    const sidebar = document.querySelector(".sidebar");
    const app = document.querySelector(".app-wrapper");

    if (!toggleButton || !sidebar || !app) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        const isCollapsed = sidebar.classList.toggle("collapsed");
        app.classList.toggle("collapsed", isCollapsed);
        toggleButton.classList.toggle("active", isCollapsed);
        toggleButton.setAttribute("aria-expanded", String(!isCollapsed));
        toggleButton.setAttribute(
            "aria-label",
            isCollapsed ? "Expand sidebar" : "Collapse sidebar"
        );

        if (toggleIcon) {
            toggleIcon.classList.toggle("bi-list", !isCollapsed);
            toggleIcon.classList.toggle("bi-layout-sidebar-inset", isCollapsed);
        }
    });
});
