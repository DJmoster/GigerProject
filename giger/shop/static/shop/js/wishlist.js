

function addToWishList(product_id) {
    product_id = parseInt(product_id);

    let list = JSON.parse(localStorage.getItem('wishlist'));

    if (list == null || !Array.isArray(list)) {
        list = [product_id];
        localStorage.setItem('wishlist', JSON.stringify(list));
    } 

    if (!list.includes(product_id)) {
        list.push(product_id);
        localStorage.setItem('wishlist', JSON.stringify(list));
    }
}

function removeFromWishList(product_id) {
    product_id = parseInt(product_id);

    let list = JSON.parse(localStorage.getItem('wishlist'));

    if (list != null || Array.isArray(list)) {
        const index = list.indexOf(product_id);

        if (index !== -1) {
            list.splice(index, 1);
        }
        localStorage.setItem('wishlist', JSON.stringify(list));
    }

    if (document.getElementById('wishlistTable') != null) {
        location.reload();
    }
}

function noItemsInWishList() {
    const text  = document.getElementById('wishlistTitle');
    const table = document.getElementById('wishlistTable');

    text.innerText = 'Ваш список бажаного пустий!';
    table.style.display = 'none';
}

function showItemsFromWishList() {
    const apiUrl     = '/api/getProduct/';
    const productUrl = '/product/';

    let list = JSON.parse(localStorage.getItem('wishlist'));

    if (list == null || !Array.isArray(list) || list == []) {
        noItemsInWishList();
        return;
    }

    let productsData = []

    list.forEach(item => {
        const xmlHttp = new XMLHttpRequest();

        xmlHttp.open('GET', apiUrl + item, false );
        xmlHttp.send();

        if (xmlHttp.status == 200) {
            productsData.push(JSON.parse(xmlHttp.responseText));
        } else {
            removeFromWishList(item);
        }
    })

    const template  = document.querySelector('#wishListElementTemplate');
    const tbody     = document.querySelector("tbody");

    if (productsData.length == 0) {
        noItemsInWishList();
        return;
    }

    productsData.forEach(obj => {
        const clone  = template.content.cloneNode(true);
        const tdList = clone.querySelectorAll('td');

        tdList[0].querySelector('a').addEventListener('click', () => removeFromWishList(obj.product.id));

        tdList[1].querySelector('a').href = productUrl + obj.product.slug;
        tdList[1].querySelector('img').src = obj.product.image;

        tdList[2].querySelector('a').href = productUrl + obj.product.slug;
        tdList[2].querySelector('a').innerText = obj.product.name;

        tdList[3].querySelector('span').innerText = obj.product.price;
        
        if (obj.product.availability == -1) {
            tdList[4].querySelector('span').innerText = 'Під замовлення';

        } else if (obj.product.availability > 0) {
            tdList[4].querySelector('span').innerText = 'В наявності';

        } else {
            tdList[4].querySelector('span').innerText = 'Немає в наявності';
        }

        tbody.appendChild(clone);
    })
}

if (document.getElementById('wishlistTable') != null) {
    showItemsFromWishList();
}