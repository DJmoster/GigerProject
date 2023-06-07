
const showSelector  = document.getElementById('show_selector');
const sortSelector  = document.getElementById('sort_selector');

const urlParams = new URLSearchParams(window.location.search);

const show      = urlParams.get('show');
const sortBy    = urlParams.get('sortBy');

if (show == null) {
    showSelector.value = 20;
} else {
    showSelector.value = show;
}

if (sortBy == null) {
    sortSelector.value = 1;
} else {
    sortSelector.value = sortBy;
}

function generate_show_url(obj) {
    urlParams.set('show', obj.value);
    window.location.search = urlParams;
}

function generate_page_url_input(obj) {
    urlParams.set('page', obj.value);
    window.location.search = urlParams;
}

function generate_page_url(obj) {
    urlParams.set('page', obj.innerText);
    window.location.search = urlParams;
}

function generate_sort_url(obj) {
    urlParams.set('sortBy', obj.value);
    window.location.search = urlParams;
}