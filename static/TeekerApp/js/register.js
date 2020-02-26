// Javascript ES6 for Register Page

document.addEventListener("DOMContentLoaded", () => {
    
    // Used to check if the username can be used by the person registering
    document.querySelector("#widgetu4337_input").onchange = () => {
        if (document.querySelector("#widgetu4337_input").value.length > 4 && document.querySelector("#widgetu4337_input").value.length < 16) {
            const request = new XMLHttpRequest();
            request.open("POST", "register/username");
            const data = new FormData();
            data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
            data.append("username", document.querySelector("#widgetu4337_input").value);
            request.send(data);
            request.onreadystatechange = () => {
                if (request.readyState === 4 && request.status === 200) {
                    if (JSON.parse(request.response)["STATUS"]) {
                        document.querySelector("#u4340-4").style.borderColor = "green"; // Turn the field borders color green
                    } else {
                        document.querySelector("#u4340-4").style.borderColor = "red"; // Turn the field borders color red
                    }
                }
            }
        } else {
            document.querySelector("#widgetu4337_input").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the fist name are letters only
    document.querySelector("#widgetu4385_input").onchange = () => {
        if (document.querySelector("#widgetu4385_input").value.match(/^[A-Za-z\s]+$/)) {
            document.querySelector("#u4388-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u4388-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the last name are letters only
    document.querySelector("#widgetu4429_input").onchange = () => {
        if (document.querySelector("#widgetu4429_input").value.match(/^[A-Za-z\s]+$/)) {
            document.querySelector("#u4432-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u4432-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }

    // Used to check if the email can be used
    document.querySelector("#widgetu4473_input").onchange = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "register/email");
        const data = new FormData();
        data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
        data.append("email", document.querySelector("#widgetu4473_input").value);
        request.send(data);
        request.onreadystatechange = () => {
            if (request.readyState === 4 && request.status === 200) {
                if (JSON.parse(request.response)["STATUS"]) {
                    document.querySelector("#u4476-4").style.borderColor = "green"; // Turn the field borders color green
                } else {
                    document.querySelector("#u4476-4").style.borderColor = "red"; // Turn the field borders color red
                }
            }
        }
    }

    // Used to check password and confirm password
    document.querySelector("#widgetu4517_input").onchange = () => {
        if (document.querySelector("#widgetu4517_input").value.length > 7 && document.querySelector("#widgetu4517_input").value.length < 65) {
            document.querySelector("#u4519-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u4519-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
    document.querySelector("#widgetu4561_input").onchange = () => {
        if (document.querySelector("#widgetu4561_input").value.length > 7 && document.querySelector("#widgetu4561_input").value.length < 65 &&
        document.querySelector("#widgetu4517_input").value.length > 7 && document.querySelector("#widgetu4517_input").value.length < 65 &&
        document.querySelector("#widgetu4517_input").value === document.querySelector("#widgetu4561_input").value) {
            document.querySelector("#u4519-4").style.borderColor = "green"; // Turn the field borders color green
            document.querySelector("#u4562-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u4519-4").style.borderColor = "red"; // Turn the field borders color red
            document.querySelector("#u4562-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
});
