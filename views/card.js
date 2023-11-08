//input elements from form
const cardNumberInput = document.getElementById("cardNumberInput");
const cardholderInput = document.getElementById("cardholderInput");
const expiresInput = document.getElementById("expiresInput");
const cvcInput = document.getElementById("cvcInput");

//display elements from the card
const displayCardNumber = document.getElementById("display-card-number");
const displayCardholder = document.getElementById("display-cardholder");
const displayExpires = document.getElementById("display-expires");
const displayCVC = document.getElementById("display-cvc");

//adding event listeners to input fields.
cardNumberInput.addEventListener('input',updateCardNumber);
cardholderInput.addEventListener('input',updateCardholder);
expiresInput.addEventListener('input',updateExpires);
cvcInput.addEventListener('input',updateCVC);

//update the display in real time.
function updateCardNumber(){
    displayCardNumber.textContent = cardNumberInput.value;
}
function updateCardholder(){
    displayCardholder.textContent = cardholderInput.value;
}
function updateExpires(){
    displayExpires.textContent = expiresInput.value;
}
function updateCVC(){
    displayCVC.textContent = cvcInput.value;
}

//prevent form submission
const paymentForm = document.getElementById("paymentForm");
paymentForm.addEventListener("submit",function(event){
    event.preventDefault();
    document.getElementById("paymentForm").addEventListener("submit", function(event) {
        event.preventDefault();
        // Handle form submission using JavaScript (if applicable)
        // Redirect to success.html using window.location.href if needed
        // Example: window.location.href = "success.html";
    });
    
});

//validation
cardNumberInput.addEventListener("input",function(){
    // Remove any existing spaces and non-numeric characters from the input value
    const cleanedInput = cardNumberInput.value.replace(/\D/g, '');
    //add space after each 4 digits
    const formattedInput = cleanedInput.replace(/(\d{4})/g, '$1 ').trim();
    //update the input with the formatted input
    cardNumberInput.value = formattedInput;

})

function hideCVC(){
    cvcInput.style.display = "";
}