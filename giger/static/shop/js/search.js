const urlParams = new URLSearchParams(window.location.search);

function generate_page_url_input(obj) {
    urlParams.set('page', obj.value);
    window.location.search = urlParams;
}

function generate_page_url(obj) {
    urlParams.set('page', obj.innerText);
    window.location.search = urlParams;
}