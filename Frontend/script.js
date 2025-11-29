// INITIAL SETUP
document.addEventListener("DOMContentLoaded", setupForm);


// SETUP FUNCTION
function setupForm() {
    const form = document.getElementById("myform");

    if (!form) {
        console.error("Form not found!");
        return;
    }

    form.addEventListener("submit", handleSubmit);
}

// FORM SUBMIT HANDLER
function handleSubmit(event) {
    event.preventDefault();

    const formData = getFormData();
    console.log("Sending JSON:", formData);

    sendData(formData)
        .then(response => {
            if (response.ok) {
                showSuccessMessage();
            } else {
                showErrorMessage();
            }
        })
        .catch(err => {
            console.error("Error:", err);
            showErrorMessage();
        });
}



// GATHER FORM VALUES
function getFormData() {
    return {
        name: document.getElementById("name").value,
        surname: document.getElementById("surname").value,
        telefon: document.getElementById("telefon").value,
        email: document.getElementById("email").value,
        people: document.getElementById("people").value
    };
}

// SEND JSON TO SERVER
function sendData(jsonData) {
    return fetch("/api/reservation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData)
    });
}

// WHEN SERVER RETURN RESPONSE 200
function showSuccessMessage() {
    const msg = document.getElementById("successMessage");
    msg.textContent = "✔ Rezervace byla úspěšně odeslána!";
    msg.classList.add("show");

    setTimeout(() => window.location.reload(), 3000);
}

// WHEN SERVER RETURNS ERROR
function showErrorMessage() {
    const msg = document.getElementById("successMessage");
    msg.textContent = "❌ Při odesílání rezervace nastala chyba. Zkuste to prosím znovu.";
    msg.style.background = "#ffd1d1";
    msg.style.border = "1px solid #d11a1a";
    msg.style.color = "#8b0000";
    msg.classList.add("show");
}

