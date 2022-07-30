console.log(localStorage);

/*** GLOBAL FUNCTION | FETCHES LOCALSTORAGE KEYS IN ARRAY ***/
function getStorageKeys() {
    // Initiate an array that will hold all keys fetched from local storage
    var localStorageKeys = [];
    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        localStorageKeys.push(key);
    }
    console.log(localStorageKeys);
    return localStorageKeys;
}

/*** GLOBAL FUNCTION | FETCHES LOCALSTORAGE AND STORES IT IN AN ARRAY */
function getLocalStorage() {
    var localStorageKeys = getStorageKeys();      
    // Initiate an array that will hold all values fetched from local storage
    var localStorageArray = [];
    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        var parsedItem = JSON.parse(localStorage.getItem(key)); 
        parsedItem.localStorageKey = key;
        localStorageArray.push(parsedItem);
    }  
    return localStorageArray;
}

/**** PRODUCT PAGE | ADD TO CART ****/
// Listen for when the user's finished typing content of each line and
//update productTotalPrice shown on the page
if (document.location.pathname == "/product") { 
    var productPrice = parseFloat(document.getElementById("product_price").value);   
    var productTotalPrice = productPrice;
    
    var contentElements = document.querySelectorAll(".content_line");    
    for (var i=0; i < contentElements.length; i++) {     
        var lineVal = contentElements[i].dataset.linevalue;
        contentElements[i].addEventListener("change", myFunction);          
    } 

    function myFunction() {
        var validInputs = Array.from(contentElements).filter( input => input.value !== '');
        productTotalPrice = productPrice + (4 * validInputs.length);
        //console.log(productTotalPrice);
        document.querySelector(".product_total_price").innerHTML = "Cena: " + productTotalPrice.toFixed(2) + " zł";
        document.querySelector(".product_total_price_net").innerHTML = "Cena netto: " + (productTotalPrice / 1.23).toFixed(2) + " zł";
    }
    
    // Listen for when the user clicks the add-to-cart button and save details to localStorage  
    let addToCartBtn = document.getElementById("add-to-cart");
    addToCartBtn.addEventListener("click", () => {

        // Initiate a dict for product details  
        var productDetailsDict = {};
        
        // Add productName to cproductDetailsDict
        var productName = document.getElementById("product_name").value;
        productDetailsDict.productName = productName;
        
        // Add contentColor to productDetailsDict
        var contentColorElement = document.getElementById("content_color_name");
        var contentColor = contentColorElement.options[contentColorElement.selectedIndex].value;
        productDetailsDict.contentColor = contentColor;

        // Add caseColor to productDetailsDict
        var caseColorE = document.getElementById("case_color_name");
        var caseColor = caseColorE.options[caseColorE.selectedIndex].value;
        productDetailsDict.caseColor = caseColor;

        // Add content lines to productDetailsDict and update productTotalPrice
        var productTotalPrice = productPrice;
        var validInputs = Array.from(contentElements).filter( input => input.value !== "");
        for (var i=0; i < validInputs.length; i++) {
            var lineName = "line_" + (i + 1);
            var lineValue = validInputs[i].value;
            productTotalPrice += 4;
            productDetailsDict[lineName] = lineValue;   
        }
        
        // Add productTotalPrice to productDetailsDict    
        productDetailsDict.productTotalPrice = productTotalPrice;
        
        // Add product and its details to localStorage
        localStorage.setItem(localStorage.length + 1, JSON.stringify(productDetailsDict));
                      
        // Add product details to add-to-cart modal  
        var cart = getLocalStorage();
        console.log(cart);
        var localStorageKeys = getStorageKeys();
        var cartTotalValue = 0;
        for (i in localStorageKeys) {
            cartTotalValue += cart[i].productTotalPrice;        
        }
        document.querySelector("#add-to-cart-modal-title").innerHTML = "Pieczątka <b>" + productName + "</b> został dodany do koszyka";
        document.querySelector("#add-to-cart-modal-price").innerHTML = "Cena: " + productTotalPrice.toFixed(2) + " zł";
        document.querySelector("#add-to-cart-modal-price-net").innerHTML = "Cena netto: " + (productTotalPrice / 1.23).toFixed(2) + " zł";
        document.querySelector("#number-in-cart").innerHTML = "Liczba produktów w koszyku: " + cart.length;
        document.querySelector("#cart-total").innerHTML = "Suma koszyka: " + cartTotalValue.toFixed(2) + " zł";
    });
}

/*** CART MODAL ***/
if (document.getElementById("cart")) {
    var cartBtn = document.getElementById("cart");
    cartBtn.addEventListener("click", () => {
        
        // Get data from localStorage
        var cart = getLocalStorage();
        console.log(cart);
        var cartTotalValue = 0;
        var cartProductsDiv = document.querySelector("#cart-products");
        var modalContentDiv = document.querySelector(".modal-content");      
        var localStorageKeys = getStorageKeys();      
        if (cart.length > 0) {
            cartProductsDiv.innerHTML = '';
            for (var i = 0; i < cart.length; i++) {
                if (cart[i]) {    
                    cartTotalValue += cart[i].productTotalPrice;
                    var localStorageKey = cart[i].localStorageKey;
                    var productName = cart[i].productName;
                    var caseColor = cart[i].caseColor;
                    var contentColor = cart[i].contentColor;
                    var productPrice = cart[i].productTotalPrice;
            
                    cartProductsDiv.innerHTML += 
                    `<div class="row" id=${localStorageKey}>
                        <td class="col-md-auto" id="cart-product-title">Pieczątka ${ productName }</td>
                        <td class="col-md-auto" id="cart-product-case-color">${ caseColor }</td>
                        <td class="col-md-auto" id="cart-product-content-color">${ contentColor }</td>
                        <td class="col-md-auto" id="product-total-price">${ productPrice.toFixed(2) } zł</td>
                        <td class="col-md-auto"><button class="remove-product" data-index=${localStorageKey}><ion-icon name="trash-outline"></ion-icon></button></td>
                    </div>
                    <br>`
                }               
            }
            document.querySelector("#cart-total").innerHTML = "<b>" + cartTotalValue.toFixed(2) + " zł</b>";

            var removeBtns = document.querySelectorAll(".remove-product");
            
            removeBtns.forEach(function(current) {
                
                console.log(current.getAttribute("data-index"));
                current.addEventListener("click", function() {
        
                    var localStorageKey = current.getAttribute("data-index");
                    console.log(localStorageKey);
                    localStorage.removeItem(localStorageKey);
                    var itemDiv = document.getElementById(localStorageKey);
                    itemDiv.remove();
                    location.reload();
                });
            });
                      
        } else {
            modalContentDiv.innerHTML = 
                `<div class="modal-header">
                    <h5 class="cart-modal-title" id="modal-title">Twój koszyk jest pusty</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <h3>Dodaj produkty do koszyka <ion-icon name="happy-outline"></ion-icon></h3>
                    <br>
                </div>
            
                <div class="modal-footer">
                    <button type="button" class="box-btn">Przejdź do produktów</button>
                </div>`            
        }    
    });   
}

/*** ORDER PAGE ***/
if (document.location.pathname == "/order") { 
    
    // Get data from localStorage object
    var cart = getLocalStorage();
    var localStorageKeys = getStorageKeys();    
    var cartItemsDiv = document.querySelector("#cart-items");
    var cartTotalValue = 0;
    
    // If cart is not empty loop through cart and assign cart items values to variables
    if (cart.length > 0) {
    
        var index = 1
        for (i in localStorageKeys) {
            if (cart[i]) {
                var productPrice = cart[i].productTotalPrice;
                cartTotalValue += productPrice;
                var productName = cart[i].productName;
                var caseColor = cart[i].caseColor;
                var contentColor = cart[i].contentColor;
                
                // Loop through a cart item and add all values whose keys start with "line"
                let productContentLines = '';
                for (const [key, value] of Object.entries(cart[i])) {
                    if (key.startsWith("line")) {
                        productContentLines += `<li>${ value }</li>`;
                    }
                }

                // Populate order.html with data from localStorage
                cartItemsDiv.innerHTML +=
                    `<tr>
                        <td class="text-start">${ index }</td>
                        <td class="text-start">${ productName }</td>
                        <td class="text-start">
                            <ol>${ productContentLines }</ol>
                        </td>
                        <td class="text-start">${ productPrice.toFixed(2) } zł</td>    
                    </tr>`;    
                
                index ++;
            }        
        }

        // Fill every cart-value element in template with the value of the cartTotalValue variable
        document.querySelector("#cart-value-cart-table").innerHTML = "<b>" + cartTotalValue.toFixed(2) + " zł</b>";
        document.querySelector("#cart-value-summary-table").innerHTML = cartTotalValue.toFixed(2) + " zł";

        // Fill every cartValueNetDiv in template with net value of the cartTotalValue variable
        var cartValueNetDivs = document.querySelectorAll(".cart-value-net");
        for (var i = 0; i < cartValueNetDivs.length; i++) {
            cartValueNetDivs[i].innerHTML = (cartTotalValue / 1.23).toFixed(2) + " zł";
        }
        
        // Listen to user selection of postage type and
        // fill postage-value element in template with the price of postage
        var postage;
        var postageE = document.getElementsByName("postage");
        postageE.forEach(function(current) {
            if (current.checked) {
                postage = parseFloat(current.value);
                document.querySelector("#postage-value").innerHTML = postage.toFixed(2) + " zł";
                document.querySelector("#order-total").innerHTML = "<b>"+ (cartTotalValue + postage).toFixed(2) + " zł<b>";  
                current.addEventListener('click', function () {
                    postage = parseFloat(current.value);
                    document.querySelector("#postage-value").innerHTML = postage.toFixed(2) + " zł";
                    document.querySelector("#order-total").innerHTML = "<b>"+ (cartTotalValue + postage).toFixed(2) + " zł<b>"; 
                });
            } else {
                current.addEventListener('click', function () {
                    postage = parseFloat(current.value);
                    document.querySelector("#postage-value").innerHTML = postage.toFixed(2) +  " zł";
                    document.querySelector("#order-total").innerHTML = "<b>"+ (cartTotalValue + postage).toFixed(2) + " zł<b>"; 
                });
            }
        });
        
        // Listen to user selection of payment type
        var payment;
        var paymentE = document.getElementsByName("payment");
        paymentE.forEach(function(current) {
            if (current.checked) {
                payment = current.value;
                current.addEventListener('click', function() {
                    payment = current.value;
                });
            } else {
                current.addEventListener('click', function() {
                    payment = current.value;
                });
            }
        });

        // Listen for user clicking check input to request an invoice
        var invoice = document.querySelector("#invoice");
        invoice.addEventListener("click", () => {
            if (invoice.checked) {
                var invoiceDetailsDiv = document.querySelector("#invoice-details");
                invoiceDetailsDiv.innerHTML = 
                `<div class="box-order-page">
                    <div class="mb-3">
                        <label for="company-name" class="form-label">Nazwa firmy<span class="compulsory-field">*</span></label>
                        <input type="text" class="form-control" id="company-name" name="company-name">    
                    </div>
                </div>

                <div class="box-order-page">
                    <div class="mb-3">
                        <label for="nip" class="form-label">NIP<span class="compulsory-field">*</span></label>
                        <input type="text" class="form-control" id="nip" name="nip">    
                    </div>
                </div>`
            } else {
                var invoiceDetailsDiv = document.querySelector("#invoice-details");
                invoiceDetailsDiv.innerHTML = ``;
            }
        } );
        
        // Stringify cart items and cart total value and add it as hidden input in the order form
        var frontEndData = JSON.stringify({"cartData": cart, "cartTotalValueData": cartTotalValue});
        document.getElementById('front-end-data').setAttribute('value', frontEndData);
    }
}