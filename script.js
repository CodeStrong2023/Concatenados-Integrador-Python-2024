document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.querySelector("#registro-form");
    const loginForm = document.querySelector("#login-form");

    if (registerForm) {
        registerForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const username = document.querySelector("input[name='username']").value;
            const email = document.querySelector("input[name='email']").value;
            const password = document.querySelector("input[name='password']").value;
            const confirmPassword = document.querySelector("input[name='confirm-password']").value;

            if (!username || !email || !password || !confirmPassword) {
                alert("Todos los campos son obligatorios.");
                return;
            } else if (password !== confirmPassword) {
                alert("Las contraseñas no coinciden.");
                return;
            }

            // Prepare form data to send
            const formData = new FormData();
            formData.append('username', username);
            formData.append('email', email);
            formData.append('password', password);
            formData.append('confirm-password', confirmPassword);

            // Send data to the server
            fetch('/registro', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = "index.html"; // Redirect to the main page
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
            });
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const username = document.querySelector("input[name='username']").value;
            const password = document.querySelector("input[name='password']").value;

            if (!username || !password) {
                alert("Todos los campos son obligatorios.");
                return;
            }

            // Prepare form data to send
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            // Send data to the server
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    localStorage.setItem('username', data.username);
                    window.location.href = "home.html"; // Redirect to the main page
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
            });
        });
    };
});

document.addEventListener("DOMContentLoaded", function() {
    const usernameDisplay = document.getElementById('username-display');
    const username = localStorage.getItem('username');
    if (username && usernameDisplay) {
        usernameDisplay.textContent = `Bienvenido, ${username}🏆`;
    }
});

