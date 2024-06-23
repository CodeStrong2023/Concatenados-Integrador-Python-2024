

document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.querySelector("#registro-form");
    const loginForm = document.querySelector("#login-form");
    const usernameDisplay = document.getElementById('username-display');
    const username = localStorage.getItem('username');
    console.log(username);
    const tournamentButtons = document.querySelectorAll('.inscripcion');
    const btnMisTorneos = document.getElementById('btnMisTorneos');

    if (registerForm) {
        registerForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const username = document.querySelector("input[name='username']").value;
            const email = document.querySelector("input[name='email']").value;
            const password = document.querySelector("input[name='password']").value;
            const confirmPassword = document.querySelector("input[name='confirm-password']").value;

            if (!username || !email || !password || !confirmPassword) {
                const camposObligatorios = "Todos los campos son obligatorios.❗";
                document.getElementById('tournament-list').innerHTML = camposObligatorios;
                document.getElementById('modal').style.display = 'block'; // Mostrar la modal
                return;
            } else if (password !== confirmPassword) {
                const passNoCoinciden = "Las constraseñas no coinciden.❗";
                document.getElementById('tournament-list').innerHTML = passNoCoinciden;
                document.getElementById('modal').style.display = 'block'; // Mostrar la modal
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
            })
        })
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
                    localStorage.setItem('id', data.id);
                    window.location.href = "home.html"; // Redirect to the main page
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
            })
        })
    }

    if (username && usernameDisplay) {
        usernameDisplay.textContent = `Bienvenido, ${username}🏆`;
    }

    tournamentButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const tournamentId = event.target.id;
            const id = localStorage.getItem('id');
            console.log(id);

            if (!id) {
                alert('Por favor, inicia sesión para inscribirte en un torneo.');
                return;
            }

            // Prepare form data to send
            const formData = new FormData();
            formData.append('id', id);
            formData.append('tournament_id', tournamentId);

            fetch('/inscribir', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const inscripcionExitosa = "Tu inscripción fue exitosa, " + username + " !🏆";
                    document.getElementById('tournament-list').innerHTML = inscripcionExitosa;
                    document.getElementById('modal').style.display = 'block'; // Mostrar la modal
                } else {
                    const inscripcionFallida = "Ya estás inscripto en este torneo, " + username;
                    document.getElementById('tournament-list').innerHTML = inscripcionFallida;
                    document.getElementById('modal').style.display = 'block'; // Mostrar la modal
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
            });
        });
    });

})

const closeButton = document.getElementsByClassName('close')[0];
closeButton.onclick = function close() {
    document.getElementById('modal').style.display = 'none';
}


function misTorneos(){
        
    fetch('/mis-torneos', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar un alert con los nombres de los torneos
            if (data.torneos.length > 0) {
                const tournamentList = "ESTÁS INSCRIPTO A:<br><br>" + data.torneos.join(' CUP ✅ <br>') + " CUP ✅" ; // Usar <br> para los saltos de línea
                document.getElementById('tournament-list').innerHTML = tournamentList;
                document.getElementById('modal').style.display = 'block'; // Mostrar la modal
            } else {
                const sinTorneos = "No estas inscripto en ningun torneo aún!" ; //
                document.getElementById('tournament-list').innerHTML = sinTorneos;
                document.getElementById('modal').style.display = 'block'; // Mostrar la modal
            }
        } else {
            alert('Error al obtener los torneos. Por favor, inténtalo de nuevo más tarde.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde.');
    })
}

function logout(){
    
    // Realizar la solicitud de cierre de sesión al servidor
    fetch('/logout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            
            // Cerrar sesión en el almacenamiento local
            localStorage.removeItem('username');
            localStorage.removeItem('id');
            // Redirigir después de unos segundos
            window.location.href = "index.html";
            // Evitar que el usuario vuelva atrás
            window.history.pushState(null, null, "index.html");
            window.addEventListener("popstate", function(event) {
                window.location.href = "index.html";
            })
        } else {
            alert('Error al cerrar sesión. Inténtelo de nuevo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
    })
}