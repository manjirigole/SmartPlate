document.addEventListener('DOMContentLoaded', function(){
    const cartIcon = document.getElementById('cart-icon');
    //initializing cart count
    let cartCount = 0;
   
    //function to update cart count and icon
    function updateCart(){
        cartCount++;
        cartIcon.innerText = cartCount; 
    }
    function decrementCount(){
        if (cartCount > 0){
            cartCount--;
            cartIcon.innerHTML = cartCount;
        }
    }

    //add click event listeners to all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('.product-card .cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click',updateCart)


    });
    const removeFromCartButoons = document.querySelectorAll('.product-card .remove-btn');
    removeFromCartButoons.forEach(button=>{
        button.addEventListener('click',decrementCount)
    });
});
