
function onStarChosen(value) {
    let stars = document.querySelectorAll("div.stars_block small")
    let input = document.getElementById("stars_count")

    stars.forEach(elem => elem.classList.add("text-muted"))

    for(let i = 0; i < value; i++) {
        stars[i].classList.remove("text-muted")
    }
    input.value = value;
}