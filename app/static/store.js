console.log(localStorage.length);

/*** GLOBAL FUNCTION | FETCHES LOCALSTORAGE AND STORES IT IN AN ARRAY */
function getLocalStorage() {  
    
    // Initiate an array that will hold all values fetched from local storage
    var localStorageArray = [];

    for (var i=0; i < localStorage.length; i++) {
        var parsedItem = JSON.parse(localStorage.getItem(i + 1)); 
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
        var cartTotalValue = 0;
        for (var i=0; i < cart.length; i++) {
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
        var cartTotalValue = 0;
        var cartProductsDiv = document.querySelector("#cart-products");
        var modalContentDiv = document.querySelector(".modal-content");
        
        if (cart.length > 0) {
            cartProductsDiv.innerHTML = '';
            for (var i=0; i < cart.length; i++) {
                cartTotalValue += cart[i].productTotalPrice;
                var productName = cart[i].productName;
                var caseColor = cart[i].caseColor;
                var contentColor = cart[i].contentColor;
                var productPrice = cart[i].productTotalPrice;
        
                cartProductsDiv.innerHTML += 
                `<div class="row">
                    <div class="col-md-4 ms-auto" id="cart-product-title">Pieczątka ${ productName }</div>
                    <div class="col-md-2 ms-auto" id="cart-product-case-color">${ caseColor }</div>
                    <div class="col-md-2 ms-auto" id="cart-product-content-color">${ contentColor }</div>
                    <div class="col-md-2 ms-auto" id="product-total-price">${ productPrice.toFixed(2) } zł</div>
                </div>
                <br>`
            }
            document.querySelector("#cart-total").innerHTML = "<b>" + cartTotalValue.toFixed(2) + " zł</b>";
            console.log(cartTotalValue);                        
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
    
    var cartItemsDiv = document.querySelector("#cart-items");
    var cartTotalValue = 0;
    
    // If cart if not empty loop through cart and assign cart items values to variables
    if (cart.length > 0) {
        
        for (var i = 0; i < cart.length; i++) {
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
                    <td class="text-start">${ i + 1 }</td>
                    <td class="text-start">${ productName }</td>
                    <td class="text-start">
                        <ol>${ productContentLines }</ol>
                    </td>
                    <td class="text-start">${ productPrice.toFixed(2) } zł</td>    
                </tr>`;    
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
        
        // Listen to user selection of ppayment type
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
        } )
            
        // Send localStorage data to views.py
        $('#orderBtnInSession' || '#orderBtnNotInSession').click(function(){
            console.log(payment);
            var data = {"cartData": cart, "postageData": postage, "paymentData": payment, "cartTotalValueData": cartTotalValue};
            console.log(data);
            $.ajax({
                data: JSON.stringify(data),
                dataType: 'json',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                url: "/order",
                success: function(m){
                    console.log(m);
                },
                error: function(m){
                    console.log(m);
                }
            });
        });
    }  
}    
        

        

        
        
 
                       
    
/*function cartNumbers(product) {
    let productNumbers = localStorage.getItem('cartNumbers');
    productNumbers = parseInt(productNumbers);

    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    if (action) {
        localStorage.setItem('cartNumbers', productNumbers - 1);
        document.querySelector('.cart span').innerHTML = productNumbers - 1;
        console.log("action running");

    if (productNumbers) {
        localStorage.setItem('cartNumbers', + 1);
        document.querySelector('.cart span').innerHTML = productNumbers + 1;
    } else {
        localStorage.setItem('cartNumbers', 1);
        document.querySelector('.cart span').innerHTML = 1;
    }
    setItems(product);
}

function setItems(product) {
    let productNumbers = localStorage.getItem('cartNumbers');
    productNumbers = parseInt(productNumbers);

    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    if(cartItems != null){
        let currentProduct = product.tag;

        if (cartItems[currentProduct] == undefined) {
            cartItems = {
                ...cartItems,
                [currentProduct]: product
            }
        }
        cartItems[currentProduct].inCart += 1;
    } else {
        product.inCart = 1;
        cartItems = {
            [product.tag]: product
        };
    }

    localStorage.setItem('productsInCart', JSON.stringify(cartItems));
}

function totalCost(product) {
    let cart =  localStorage.getItem("totalCost");

    if (action) {
        cart = parseInt(cart);
        localStorage.setItem("totalCost", cart - product.price);
    if (cart != null) {
        cart = parseInt(cart);
        localStorage.setItem("totalCost", cart + product.price);
    } else {
        localStorage.setItem("totalCost", product.price);
    }
}

function displayCart() {
    let cartItems = localStorage.getItem("productsInCart");
    cartItems = JSON.parse(cartItems);

    let cart =  localStorage.getItem("totalCost");
    cart = parseInt(cart);

    let productsSection = document.querySelector(".products");
    let totalSection = document.querySelector(".cart-total-conteiner");


    if (cartItems && productsSection) {
        productsSection.innerHTML = '';
        Object.values(cartItems).map((item, index) => {
            productsSection.innerHTML +=
            `<div class="grid-cart-item">
                <img alt="colop20" class="img-thumbnail img-cart p-3 img-fluid" src="./photos/${item.tag}.jpg">
            </div>
            <div class="grid-cart-item product">
                <ion-icon name="trash-outline"></ion-icon>
                <span>${item.name}</span>
            </div>
            <div class="grid-cart-item product.price">${item.price},00 zł</div>
            <div class="grid-cart-item product-quantity">
                <ion-icon class="decrease" name="arrow-dropleft-circle"></ion-icon>
                <span>${item.inCart}</span>
                <ion-icon class="increase" name="arrow-dropright-circle"></ion-icon>
            </div>
            <div class="grid-cart-item total">
                ${item.inCart * item.price},00 zł
            </div>`;
        });

        totalSection.innerHTML +=
        `<div class=cartTotalContainer">
                <h4 class="cartTotalTitle">
                    RAZEM<span class="cartTotal">
                    ${cart},00 zł</span>
                </h4>
        </div>`
    }
}

onLoadCartNumbers();
displayCart();*/