function print(text) {
    var history = document.getElementById("history");
    var newElem = document.createElement("p");
    var content = document.createTextNode(text);
    newElem.appendChild(content);
    history.appendChild(newElem);
}


function main() {
    print("The second thing");
}


function readIn(elem) {
    if (event.keyCode == 13) {  // on enter
        print(elem.value);
        elem.value = "";
    }
}


window.onload = main;
