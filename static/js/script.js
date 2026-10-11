document.addEventListener("DOMContentLoaded", () => {
    // Mobile navigation
    const menu = document.getElementById("menuBtn");
    const nav = document.getElementById("nav");

    if (menu && nav) {
        menu.addEventListener("click", () => {
            nav.classList.toggle("open");
        });
    }

    // Fleet search and category filter
    const search = document.getElementById("search");
    const filter = document.getElementById("filter");
    const cards = document.querySelectorAll(".fleet-card");

    function filterCars() {
        if (!search || !filter) return;

        const query = search.value.toLowerCase().trim();
        const selectedType = filter.value;

        cards.forEach(card => {
            const name = card.dataset.name || "";
            const type = card.dataset.type || "";

            const matchesSearch = name.includes(query);
            const matchesType = selectedType === "All" || type === selectedType;

            card.style.display = matchesSearch && matchesType ? "" : "none";
        });
    }

    if (search && filter) {
        search.addEventListener("input", filterCars);
        filter.addEventListener("change", filterCars);
    }
});
