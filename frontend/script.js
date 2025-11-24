// Highlight name when hovered
document.addEventListener("DOMContentLoaded", () => {
    const nameTitle = document.querySelector(".name");

    nameTitle.addEventListener("mouseenter", () => {
        nameTitle.style.color = "#4e8a55";
        nameTitle.style.transition = "0.3s";
    });

    nameTitle.addEventListener("mouseleave", () => {
        nameTitle.style.color = "#2d5a31";
    });
});

// Form submission handling
const form = document.getElementById("form");

form.addEventListener("submit", function (event) {
    event.preventDefault(); // stops page reload

    const name = form.querySelector('input[type="text"]').value.trim();
    const email = form.querySelector('input[type="email"]').value.trim();
    const message = form.querySelector("textarea").value.trim();

    // Basic validation
    if (name === "" || email === "" || message === "") {
        alert("Please fill all fields before submitting.");
        return;
    }

    // Success message
    alert(`Thank you, ${name}! Your message has been sent successfully.`);

    // Clear form
    form.reset();
});
