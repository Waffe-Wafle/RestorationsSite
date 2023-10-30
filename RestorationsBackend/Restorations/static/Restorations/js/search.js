search_input = document.getElementById('nav_search')

function do_search() {
    let href = window.location.href;
    let add = '';
    if (href.includes('?')) {
        let last_smbh = href.substring(href.length - 1);
        if (last_smbh != '?' && last_smbh != '&') add = '&';

        let spl = href.split('search=');
        if (spl.length > 1) {
            if (spl[1].indexOf('&') == -1) spl[1] += '&';
            href = spl[0] + spl[1].slice(spl[1].indexOf('&'));
            href = href.slice(0, -2)
        }
    }
    else add = '?'

    let search_query = document.getElementById('nav_search').value;
    enc_search = url_encode(search_query)
    if (search_query.replace(' ', '') != '') {
        document.cookie+='search='+enc_search+';'
        window.location.href = href + add + 'search=' + enc_search;
    }
}

// Doing search:
document.querySelector('img.search-lope').addEventListener('click', do_search);
inputElement.addEventListener('keydown', () => {
    if (event.key === 'Enter'){
        do_search()
    }
});



window.onload = () => {
    set_cookie('search', document.getElementById('nav_search').value)
}





function url_encode(str) {
    return escape(encodeURIComponent(str));
}