// api.js
function callApi(endpoint, method, data, callback) {
    var xhr = new XMLHttpRequest()
    xhr.open(method, "http://localhost:8000/" + endpoint)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            callback(xhr.status === 200 ? JSON.parse(xhr.responseText) : "erreur")
        }
    }
    xhr.send(JSON.stringify(data))
}