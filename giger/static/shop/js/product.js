
function onStarChosen(value) {
    let stars = document.querySelectorAll("div.stars_block small")
    let input = document.getElementById("stars_count")

    stars.forEach(elem => elem.classList.add("text-muted"))

    for(let i = 0; i < value; i++) {
        stars[i].classList.remove("text-muted")
    }
    input.value = value;
}

function productAddToCart(product_id) {
    product_id = parseInt(product_id);

    const input = document.getElementById('productCount');

    addToCart(product_id, input.value);
}

function productInputAdd() {
    const input = document.getElementById('productCount');
    input.value++;
}

function productInputMinus() {
    const input = document.getElementById('productCount');
    if(input.value > 0) {
        input.value--;
    }
}