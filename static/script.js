 // Echtzeit-Vorschau der E-Mail
 document.getElementById("message").addEventListener("input", function() {
    document.getElementById("previewBox").innerHTML = this.value;
});

// Form Validierung & Ajax-Submit
document.getElementById("emailForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);
    let statusMessage = document.getElementById("statusMessage");

    fetch("send_email.php", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        statusMessage.innerHTML = `<div class="alert alert-success">${data}</div>`;
    })
    .catch(error => {
        statusMessage.innerHTML = `<div class="alert alert-danger">Fehler: ${error}</div>`;
    });
});