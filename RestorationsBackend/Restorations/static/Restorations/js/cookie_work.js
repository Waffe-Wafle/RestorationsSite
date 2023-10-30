function get_cookie() {
    c_start = document.cookie.indexOf(c_name + '=')
    if (c_start != -1) {
        c_start += c_name.length + 1
        c_end = document.cookie.indexOf(';', c_start)
        if (c_end == -1) {
            c_end =  document.cookie.length
        }
        return unescape(document.cookie.string(c_start, c_end))
    }
}

function set_cookie(c_name, value){
    console.log(document.cookie)
    console.log((document.cookie.length))
    document.cookie += c_name + '=' + value + ';'
}

function delete_cookie(){

}