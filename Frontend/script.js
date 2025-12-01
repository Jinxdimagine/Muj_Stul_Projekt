// INITIAL SETUP
document.addEventListener("DOMContentLoaded", setupForm);


// SETUP FUNCTION
function setupForm() {
    const form = document.getElementById("myform");

    if (!form) {
        console.error("Form not found!");
        return;
    }
    generateTimes();
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
        people: document.getElementById("people").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        status:"sending"
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

const dateInput = document.getElementById("date");
const tomorrowDate = new Date();
tomorrowDate.setDate(tomorrowDate.getDate() + 1);
const tomorrow = tomorrowDate.toISOString().split("T")[0];
dateInput.setAttribute("min", tomorrow);

// Vygenerování časů 11:00–23:00 po 15 min
const timeSelect = document.getElementById("time");
function generateTimes() {
    let start = 11 * 60; // 11:00
    let end = 23 * 60;   // 23:00
    let interval = 15;

    for (let t = start; t <= end; t += interval) {
        let hours = String(Math.floor(t / 60)).padStart(2, "0");
        let minutes = String(t % 60).padStart(2, "0");
        let option = document.createElement("option");
        option.value = `${hours}:${minutes}`;
        option.textContent = `${hours}:${minutes}`;
        timeSelect.appendChild(option);
    }
}

