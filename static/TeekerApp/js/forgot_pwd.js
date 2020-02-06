// Javascript for Forgot Password Page

// This is use because the page can't load the static files properly
// Push state to URL.
var HIDDEN_URL = document.URL; // Get the old URL
NEW_URL = location.protocol+"//"+location.hostname+":"+location.port+"/forgot_pwd"; // Create a new URL
history.pushState({}, null, NEW_URL); // Replace the URL with the new one
let stateCheck = setInterval(() => {
if (document.readyState === 'complete') {
    clearInterval(stateCheck);
    history.pushState({}, null, HIDDEN_URL); // Place the old URL back
}
}, 100);

document.addEventListener("DOMContentLoaded", () => {

	// Used to check password and confirm password
    document.querySelector("#widgetu1304_input").onchange = () => {
        if (document.querySelector("#widgetu1304_input").value.length > 7 && document.querySelector("#widgetu1304_input").value.length < 65) {
            document.querySelector("#u1306-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1306-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
    document.querySelector("#widgetu1329_input").onchange = () => {
        if (document.querySelector("#widgetu1329_input").value.length > 7 && document.querySelector("#widgetu1329_input").value.length < 65 &&
        document.querySelector("#widgetu1304_input").value.length > 7 && document.querySelector("#widgetu1304_input").value.length < 65 &&
        document.querySelector("#widgetu1304_input").value === document.querySelector("#widgetu1329_input").value) {
            document.querySelector("#u1306-4").style.borderColor = "green"; // Turn the field borders color green
            document.querySelector("#u1330-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1306-4").style.borderColor = "red"; // Turn the field borders color red
            document.querySelector("#u1330-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
});
