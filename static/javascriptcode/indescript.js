document.addEventListener("DOMContentLoaded",function(){
    const filterItems=document.querySelectorAll(".filter-list");
    const products=document.querySelectorAll(".new-product-box-wrapper");
    
   filterItems.forEach(item=>{
    item.addEventListener("click",function(){
        const category=this.getAttribute("data-filter");
        products.forEach(product=>{
            if(category =="all" || product.getAttribute("data-filter")==category){
                product.classList.remove("hidden");
            }
            else{
                product.classList.add("hidden");
            }
        });
        filterItems.forEach(i=>i.classList.remove("active"));
        this.classList.add("active");
    });
   });
 
});


//search 
document.addEventListener('DOMContentLoaded', function() {
    var searchBox = document.getElementById('search-box');
    var searchButton = document.getElementById('search-button');
    var products = document.querySelectorAll('.new-product-box-wrapper'); // Query once, reuse later

    // Function to handle the search logic
    function filterProducts(searchTerm) {
        // Trim the search term to handle spaces only input
        searchTerm = searchTerm.trim().toLowerCase(); // Remove leading/trailing spaces and convert to lowercase

        // If searchTerm is empty after trimming, show all products
        if (searchTerm == "") {
            products.forEach(function(product) {
                product.style.display = 'block'; // Show all products
            });
        } else {
            products.forEach(function(product) {
                var productNameElement = product.querySelector('.new-product-title');
                if (productNameElement) {
                    var productName = productNameElement.textContent.toLowerCase();
                    if (productName.includes(searchTerm)) {
                        product.style.display = 'block'; // Show product
                    } else {
                        product.style.display = 'none'; // Hide product
                    }
                }
            });
        }
    }

    // Trigger the search function when the user types
    searchBox.addEventListener('input', function() {
        var searchTerm = searchBox.value;
        filterProducts(searchTerm); // Call the filter function
    });

    // Trigger the search when the button is clicked
    searchButton.addEventListener('click', function() {
        var searchTerm = searchBox.value;
        filterProducts(searchTerm); // Call the filter function
    });

    // Prevent form submission on pressing Enter
    searchBox.addEventListener('keydown', function(event) {
        if (event.key =='Enter') {
            event.preventDefault(); // Prevent form submission on Enter key
            var searchTerm = searchBox.value;
            filterProducts(searchTerm); // Call the search function
        }
    });
});

function handleSearch(event) {
    event.preventDefault(); // Prevent the form from submitting
    var searchTerm = document.getElementById('search-box').value;
    filterProducts(searchTerm);
}