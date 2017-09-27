function get_data(url, data, callback) {
    var xhr = new XMLHttpRequest();
    var query_str = ''
    var keys = Object.getOwnPropertyNames(data)
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i]      
        var value = data[key]
        if(value) query_str += key+'='+value+'&'  
    }
    if(query_str.length>0) query_str = '?'+query_str.slice(0, -1)
    xhr.open('get', url+query_str);
    xhr.onreadystatechange = function () {
        if ( xhr.readyState === xhr.DONE ) {
            if ( xhr.status === 200 || xhr.status === 0 ) {
                if ( xhr.responseText ) {
                    var json = JSON.parse(xhr.responseText)
                    callback( json )
                }
            }
        }
    }
    xhr.send();
}

function post_data(url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('post', url);
    xhr.onreadystatechange = function () {
        if ( xhr.readyState === xhr.DONE ) {
            if ( xhr.status === 200 || xhr.status === 0 ) {
                if ( xhr.responseText ) {
                    var json = JSON.parse(xhr.responseText)
                    callback( json )
                }
            }
        }
    }
    xhr.send(data);
}