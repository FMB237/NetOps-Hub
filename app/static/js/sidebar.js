function toggleSidebar(toggleButton) {
    const sidebar = document.querySelector(".sidebar");
    const app = document.querySelector(".app-wrapper");
    const toggleIcon = toggleButton.querySelector("i");

    if (!sidebar || !app) {
        return;
    }

    const isCollapsed = sidebar.classList.toggle("collapsed");
    app.classList.toggle("collapsed", isCollapsed);
    app.classList.toggle("sidebar-collapsed", isCollapsed);
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
}

document.addEventListener("click", (event) => {
    const toggleButton = event.target.closest("#sidebar-toggle");

    if (!toggleButton) {
        return;
    }

    toggleSidebar(toggleButton);
});
