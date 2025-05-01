



function toggleDropdown(dropdownId, arrowId) {
    let dropdown = document.getElementById(dropdownId);
    let arrow = document.getElementById(arrowId);
    let isVisible = dropdown.style.display === "block";
    
    // Close all dropdowns first
    document.querySelectorAll(".dropdown-content").forEach(drop => drop.style.display = "none");
    document.querySelectorAll(".arrow").forEach(img => img.classList.remove("rotate"));

    // Toggle current dropdown
    if (!isVisible) {
        dropdown.style.display = "block";
        arrow.classList.add("rotate");
    }
}

    function toggleDropdown(dropdownId, arrowId) {
        let dropdown = document.getElementById(dropdownId);
        let arrow = document.getElementById(arrowId);
        let isVisible = dropdown.style.display === "block";

        // Close all dropdowns first
        document.querySelectorAll(".dropdown-content").forEach(drop => drop.style.display = "none");
        document.querySelectorAll(".arrow").forEach(img => img.classList.remove("rotate"));

        // Toggle current dropdown
        if (!isVisible) {
            dropdown.style.display = "block";
            arrow.classList.add("rotate");
        }
    }

    function filterProducts(filterType, value) {
        console.log(filterType, value); // Debugging
        let url = new URL(window.location.href);
        let params = url.searchParams;
    
        if (filterType === 'brand') {
            if (value === 'all') {
                params.delete('brand');
            } else {
                params.set('brand', value);
            }
        } else if (filterType === 'price') {
            let priceRange = value.match(/\d+/g);  
            if (priceRange.length === 2) {
                params.set('min_price', priceRange[0]);
                params.set('max_price', priceRange[1]);
            }
        }
    
        console.log("Updated URL:", url.toString());
        window.location.href = url.toString();
    }

    // Close dropdown when clicking outside
    document.addEventListener("click", function(event) {
        if (!event.target.closest(".filter-action")) {
            document.querySelectorAll(".dropdown-content").forEach(drop => drop.style.display = "none");
            document.querySelectorAll(".arrow").forEach(img => img.classList.remove("rotate"));
        }
    });