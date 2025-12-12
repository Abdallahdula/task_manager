// ================= CONTACTS STORAGE =================

// Load saved contacts array
let contacts = JSON.parse(localStorage.getItem("contacts")) || [];

// Save entire contacts array
function saveContacts() {
    localStorage.setItem("contacts", JSON.stringify(contacts));
}

// Display all saved contacts in the contactList div
function displayContacts() {
    const container = document.getElementById("contactList");
    if (!container) return;

    container.innerHTML = "";

    contacts.forEach((c, index) => {
        container.innerHTML += `
            <div class="contact-entry">
                <p><b>${c.name}</b> (${c.email})</p>
                <p>${c.message}</p>
                <small>${c.time}</small><br><br>
                <button type="button" onclick="deleteContact(${index})">Delete</button>
                <hr>
            </div>
        `;
    });
}

// Make deleteContact available globally (for onclick in HTML)
window.deleteContact = function (index) {
    contacts.splice(index, 1);
    saveContacts();
    displayContacts();
};

// ================= DOM LOADED =================

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form");
    const nameInput = document.getElementById("nameInput");
    const emailInput = document.getElementById("emailInput");
    const messageInput = document.getElementById("messageInput");

    // ---------- Prefill latest form data (contactForm) ----------
    const savedForm = localStorage.getItem("contactForm");
    if (savedForm) {
        try {
            const { name, email, message } = JSON.parse(savedForm);
            if (name) nameInput.value = name;
            if (email) emailInput.value = email;
            if (message) messageInput.value = message;
        } catch (e) {
            console.error("Error parsing contactForm:", e);
        }
    }

    // ---------- Form submit handler ----------
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const message = messageInput.value.trim();

        if (!name || !email || !message) return;

        const contact = {
            name,
            email,
            message,
            time: new Date().toLocaleString()
        };

        // Save in contacts list
        contacts.push(contact);
        saveContacts();
        displayContacts();

        // Save latest form data as requested
        localStorage.setItem(
            "contactForm",
            JSON.stringify({ name, email, message })
        );

        form.reset();
        alert("Message Saved!");
    });

    // ================= THEME TOGGLE (LIGHT / DARK) =================
    const themeToggleBtn = document.getElementById("themeToggle");

    function applyTheme(theme) {
      if (theme === "dark") {
        document.body.classList.add("dark-mode");
        // show sun when currently in dark mode (click to go back to light)
        themeToggleBtn.textContent = "☀️";
    } else {
        document.body.classList.remove("dark-mode");
        // show moon in light mode (click to go dark)
        themeToggleBtn.textContent = "🌙";
    }
}

    // Load saved theme
    let savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    // Toggle theme on click
    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.body.classList.contains("dark-mode")
            ? "dark"
            : "light";
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        localStorage.setItem("theme", newTheme);
        applyTheme(newTheme);
    });

    // ================= COUNTER BUTTON =================



    // Click Counter
    let clicks = 0;

    // ✔ Load saved count from localStorage when page opens
    window.addEventListener("DOMContentLoaded", () => {
        let saved = localStorage.getItem("clicks");

        if (saved !== null) {
            clicks = parseInt(saved);
        }

        document.getElementById("clickCount").innerText = "Clicks: " + clicks;
    });

    // ✔ Increase counter
    document.getElementById("increaseBtn").addEventListener("click", () => {
        clicks++;
        document.getElementById("clickCount").innerText = "Clicks: " + clicks;

        // Save new count
        localStorage.setItem("clicks", clicks);
    });

    // ✔ Reset counter
    document.getElementById("resetBtn").addEventListener("click", () => {
        clicks = 0;
        document.getElementById("clickCount").innerText = "Clicks: 0";
        localStorage.setItem("clicks", 0);
    });


    // Show existing contacts on page load
    displayContacts();
});
