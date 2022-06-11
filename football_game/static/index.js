var image = document.getElementById('image');

image.onclick = function(e) {
    var value = {
        x: e.offsetX,
        y: e.offsetY
    }
    console.log(window.location.pathname);
    const destUrl = window.location.pathname;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', destUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.send(JSON.stringify(value));
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);
            if(data.win){
                window.location.href = data.location;
            }
            else{
                document.getElementById('image').src = "data:image/png;base64," + data.image;
            }
        }
    }
};
