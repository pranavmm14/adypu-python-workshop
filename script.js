document.addEventListener("DOMContentLoaded", function () {
    emailjs.init("YOUR_USER_ID"); // Replace with your EmailJS User ID

    document.getElementById("contact-form").addEventListener("submit", function (event) {
        event.preventDefault();

        let templateParams = {
            from_name: document.getElementById("name").value,
            from_email: document.getElementById("email").value,
            message: document.getElementById("message").value
        };

        emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", templateParams)
            .then(response => {
                document.getElementById("response-message").textContent = "✅ Message sent successfully!";
                document.getElementById("response-message").classList.remove("hidden");
                document.getElementById("contact-form").reset();
            })
            .catch(error => {
                document.getElementById("response-message").textContent = "❌ Failed to send message. Try again!";
                document.getElementById("response-message").classList.remove("hidden");
            });
    });
});
