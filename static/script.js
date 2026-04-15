// -------------------------
// BASE URL
// -------------------------
const BASE_URL = "http://127.0.0.1:5000";

// -------------------------
// SOS BUTTON
// -------------------------
function sendSOS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const data = {
                location: `Lat: ${position.coords.latitude}, Lng: ${position.coords.longitude}`
            };

            fetch(`${BASE_URL}/sos`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
                .then(res => res.json())
                .then(data => {
                    alert("🚨 SOS Sent Successfully!");
                    console.log(data);
                });
        });
    } else {
        alert("Geolocation not supported");
    }
}

// -------------------------
// LIVE LOCATION UPDATE
// -------------------------
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            fetch(`${BASE_URL}/location`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                })
            })
                .then(res => res.json())
                .then(data => console.log("Location updated"));
        });
    }
}

// Auto update every 30 sec
setInterval(sendLocation, 30000);

// -------------------------
// DAILY CHECK-IN
// -------------------------
function checkIn() {
    fetch(`${BASE_URL}/checkin`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "OK" })
    })
        .then(res => res.json())
        .then(data => {
            alert("✅ Check-in Done");
        });
}

// -------------------------
// ADD CONTACT
// -------------------------
function addContact() {
    const name = document.getElementById("cname").value;
    const relation = document.getElementById("crelation").value;
    const phone = document.getElementById("cphone").value;

    fetch(`${BASE_URL}/add_contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, relation, phone })
    })
        .then(res => res.json())
        .then(data => alert("Contact Added"));
}

// -------------------------
// ADD MEDICINE
// -------------------------
function addMedicine() {
    const name = document.getElementById("mname").value;
    const dosage = document.getElementById("mdosage").value;
    const time = document.getElementById("mtime").value;

    fetch(`${BASE_URL}/add_medicine`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, dosage, time })
    })
        .then(res => res.json())
        .then(data => alert("Medicine Added"));
}

// -------------------------
// QUICK CALL
// -------------------------
function quickCall(number) {
    window.location.href = `tel:${number}`;
}

// -------------------------
// EMERGENCY CALL
// -------------------------
function callAmbulance() {
    window.location.href = "tel:108";
}