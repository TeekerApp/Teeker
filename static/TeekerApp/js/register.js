// Javascript ES6 for Register Page

document.addEventListener("DOMContentLoaded", () => {
    
    // Used to check if the username can be used by the person registering
    document.querySelector(".username").onchange = () => {
        if (document.querySelector(".username").value.length > 4 && document.querySelector(".username").value.length < 16) {
            const request = new XMLHttpRequest();
            request.open("POST", "register/username");
            const data = new FormData();
            data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
            data.append("username", document.querySelector(".username").value);
            request.send(data);
            request.onreadystatechange = () => {
                if (request.readyState === 4 && request.status === 200) {
                    if (JSON.parse(request.response)["STATUS"]) {
                        document.querySelector(".username").style.borderColor = "green"; // Turn the field borders color green
                    } else {
                        document.querySelector(".username").style.borderColor = "red"; // Turn the field borders color red
                    }
                }
            }
        } else {
            document.querySelector(".username").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the fist name are letters only
    document.querySelector(".first_name").onchange = () => {
        if (document.querySelector(".first_name").value.match(/^[A-Za-z\s]+$/)) {
            document.querySelector(".first_name").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector(".first_name").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the last name are letters only
    document.querySelector(".last_name").onchange = () => {
        if (document.querySelector(".last_name").value.match(/^[A-Za-z\s]+$/)) {
            document.querySelector(".last_name").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector(".last_name").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the email can be used
    document.querySelector(".email").onchange = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "register/email");
        const data = new FormData();
        data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
        data.append("email", document.querySelector(".email").value);
        request.send(data);
        request.onreadystatechange = () => {
            if (request.readyState === 4 && request.status === 200) {
                if (JSON.parse(request.response)["STATUS"]) {
                    document.querySelector(".email").style.borderColor = "green"; // Turn the field borders color green
                } else {
                    document.querySelector(".email").style.borderColor = "red"; // Turn the field borders color red
                }
            }
        }
    }
});
