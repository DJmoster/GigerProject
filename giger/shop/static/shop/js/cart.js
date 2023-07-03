let cartProductsData = []

function addToCart(product_id, count) {
    product_id = parseInt(product_id);
    count      = parseInt(count);

    let obj = {'id': product_id, 'count': count};

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list == null || !Array.isArray(list)) {
        list = [obj];
        localStorage.setItem('cart', JSON.stringify(list));
        return;
    } 

    const element = list.find((elem) => elem.id == obj.id);

    if (element != null) {
        element.count += count;
        localStorage.setItem('cart', JSON.stringify(list));
    } else {
        list.push(obj);
        localStorage.setItem('cart', JSON.stringify(list));
    }
}

function setCartCount(product_id, count) {
    product_id = parseInt(product_id);
    count      = parseInt(count);

    if(count < 1) {
        removeFromCart(product_id);
        return;
    }

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list != null || Array.isArray(list)) {
        const element = list.find((elem) => elem.id == product_id);
        const index   = list.indexOf(element);

        if (index !== -1) {
            element.count = count;
        }
        localStorage.setItem('cart', JSON.stringify(list));
    }

    if (document.getElementById('cartTable') != null) {
        cartProductsData.forEach(obj => {
            if(obj.product.id == product_id) {
                obj.product.count = count;
            }
        });

        updateCartItems();
    }
}

function removeFromCart(product_id) {
    product_id = parseInt(product_id);

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list != null || Array.isArray(list)) {
        const element = list.find((elem) => elem.id == product_id);
        const index   = list.indexOf(element);

        if (index !== -1) {
            list.splice(index, 1);
        }
        localStorage.setItem('cart', JSON.stringify(list));
    }

    if (document.getElementById('cartTable') != null) {
        cartProductsData.forEach(obj => {
            if(obj.product.id == product_id) {
                cartProductsData.splice(cartProductsData.indexOf(obj), 1);
            }
        });

        updateCartItems();
    }
}

function cartTableItemSet(item_id, product_id) {
    const element = document.getElementById(item_id);
    const input   = element.querySelector('td:nth-child(5) > div > div > div.col > input');

    if(parseInt(input.value) < 1) {
        input.value = 1;
    }

    setCartCount(product_id, input.value);
}

function cartTableItemMinus(item_id, product_id) {
    const element = document.getElementById(item_id);
    const input   = element.querySelector('td:nth-child(5) > div > div > div.col > input');

    input.value--;

    if(parseInt(input.value) < 1) {
        input.value = 1;
    }
    setCartCount(product_id, input.value);
}

function cartTableItemAdd(item_id, product_id) {
    const element = document.getElementById(item_id);
    const input   = element.querySelector('td:nth-child(5) > div > div > div.col > input');

    input.value++;
    setCartCount(product_id, input.value);
}


function noItemsInCart() {
    const text  = document.getElementById('cartTitle');
    const table = document.getElementById('cartTable');
    const total = document.getElementById('cartTotal');

    text.innerText = 'Ваша корзина пуста!';

    table.style.display = 'none';
    total.style.display = 'none';
}

function calculateCartTotal() {
    const totalElement = document.getElementById('cartTotalSpan');
    let totalPrice = 0;

    cartProductsData.forEach(obj => {
        totalPrice += Math.round((obj.product.price * obj.product.count) * 100) / 100;
    })

    totalElement.innerText = totalPrice + ' грн.';
}

function updateCartItems() {
    const productUrl = '/product/';

    const template  = document.querySelector('#cartElementTemplate');
    const bTemplate = document.querySelector('#cartButtonTable');

    const tbody     = document.querySelector("tbody");

    tbody.innerHTML = '';

    if (cartProductsData.length == 0) {
        noItemsInCart();
        return;
    }

    cartProductsData.forEach(obj => {
        const clone     = template.content.cloneNode(true);
        const tdList    = clone.querySelectorAll('td');
        const table_id  = 'product_table_' + obj.product.id

        clone.querySelector('tr').id = table_id;

        tdList[0].querySelector('a').addEventListener('click', () => removeFromCart(obj.product.id));

        tdList[1].querySelector('a').href = productUrl + obj.product.slug;
        tdList[1].querySelector('img').src = obj.product.image;

        tdList[2].querySelector('a').href = productUrl + obj.product.slug;
        tdList[2].querySelector('a').innerText = obj.product.name;

        tdList[3].querySelector('span').innerText = obj.product.price + ' грн.';
        
        tdList[4].querySelector('div > div > div.col > input').value = obj.product.count;
        tdList[4].querySelector('div > div > div.col > input').addEventListener('change', () => cartTableItemSet(table_id, obj.product.id));
        tdList[4].querySelector('div > div > div:nth-child(2) > a:nth-child(2)').addEventListener('click', () => cartTableItemAdd(table_id, obj.product.id));
        tdList[4].querySelector('div > div > div:nth-child(2) > a:nth-child(1)').addEventListener('click', () => cartTableItemMinus(table_id, obj.product.id));

        tdList[5].querySelector('span').innerText = (Math.round((obj.product.price * obj.product.count) * 100) / 100) + ' грн.';


        tbody.appendChild(clone);
    })
    tbody.appendChild(bTemplate.content.cloneNode(true));

    calculateCartTotal();
}


function showItemsFromCart() {
    const apiUrl     = '/api/getProduct/';

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list == null || !Array.isArray(list) || list == []) {
        noItemsInCart();
        return;
    }

    list.reverse()
    list.forEach(item => {
        const xmlHttp = new XMLHttpRequest();

        xmlHttp.open('GET', apiUrl + item.id, false);
        xmlHttp.send();

        if (xmlHttp.status == 200) {
            let responce = JSON.parse(xmlHttp.responseText);
            responce.product.count = item.count;

            cartProductsData.push(responce);

        } else {
            removeFromCart(item.id);
        }
    })

    updateCartItems()
}

function headerShowCartCount() {
    const cartElement = document.getElementById('headerCartCounter');

    let list = JSON.parse(localStorage.getItem('cart'));

    if (list != null && Array.isArray(list) && list.length != 0) {
        cartElement.innerText = list.length;
    } else {
        cartElement.style.display = 'none';
    }
}

headerShowCartCount()


if (document.getElementById('cartTable') != null) {
    showItemsFromCart()
}