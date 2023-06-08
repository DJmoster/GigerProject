
function checkoutNoItemsInCart() {
    window.location.href = '/cart'
}

function showCheckoutProducts() {
    const apiUrl     = '/api/getProduct/';
    const productUrl = '/product/';

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list == null || !Array.isArray(list) || list == []) {
        checkoutNoItemsInCart();
        return;
    }

    list.reverse()
    let productsData = []

    list.forEach(item => {
        const xmlHttp = new XMLHttpRequest();

        xmlHttp.open('GET', apiUrl + item.id, false);
        xmlHttp.send();

        if (xmlHttp.status == 200) {
            let responce = JSON.parse(xmlHttp.responseText);
            responce.product.count = item.count;

            productsData.push(responce);

        } else {
            removeFromCart(item.id);
        }
    })

    const template  = document.querySelector('#checkoutElementTemplate');
    const tbody     = document.querySelector("tbody");

    if (productsData.length == 0) {
        checkoutNoItemsInCart();
        return;
    }
    
    objectsTotalPrice = 0

    productsData.forEach(obj => {
        const clone     = template.content.cloneNode(true);
        const tdList    = clone.querySelectorAll('td');

        tdList[0].innerHTML = "<a class=\"text-gray-90\" href=\"" + productUrl + obj.product.slug + "\">" + obj.product.name + "&nbsp;<strong class=\"product-quantity\">× " + obj.product.count + "</strong><a>"
        tdList[1].innerText = obj.product.price + ' грн.'

        objectsTotalPrice += Math.round((obj.product.price * obj.product.count) * 100) / 100;
 
        tbody.appendChild(clone);
    })

    document.getElementById('productsPrice').innerText = objectsTotalPrice + ' грн.';
    document.getElementById('productsTotalPrice').innerText = objectsTotalPrice + ' грн.';

    document.getElementById('formProductsInput').value = localStorage.getItem('cart');
}

if (document.querySelector('#checkoutElementTemplate') != null) {
    showCheckoutProducts();
}