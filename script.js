document.addEventListener("DOMContentLoaded", function() {
    // Seleccionar elementos del DOM
    const registerForm = document.querySelector("#registro-form");
    const loginForm = document.querySelector("#login-form");
    const usernameDisplay = document.getElementById('username-display');
    const username = localStorage.getItem('username');
    const tournamentButtons = document.querySelectorAll('.inscripcion');
    const btnMisTorneos = document.getElementById('btnMisTorneos');

    // Escuchar el evento de submit en el formulario de registro
    if (registerForm) {
        registerForm.addEventListener("submit", function(event) {
            event.preventDefault();

            // Obtener valores del formulario
            const username = document.querySelector("input[name='username']").value;
            const email = document.querySelector("input[name='email']").value;
            const password = document.querySelector("input[name='password']").value;
            const confirmPassword = document.querySelector("input[name='confirm-password']").value;

            // Validar campos obligatorios
            if (!username || !email || !password || !confirmPassword) {
                const camposObligatorios = "Todos los campos son obligatorios.❗";
                mostrarModal(camposObligatorios);
                return;
            } else if (password !== confirmPassword) {
                const passNoCoinciden = "Las contraseñas no coinciden.❗";
                mostrarModal(passNoCoinciden);
                return;
            }

            // Preparar datos del formulario para enviar
            const formData = new FormData();
            formData.append('username', username);
            formData.append('email', email);
            formData.append('password', password);
            formData.append('confirm-password', confirmPassword);

            // Enviar datos al servidor
            fetch('/registro', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = "index.html"; // Redirigir a la página principal
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

    // Escuchar el evento de submit en el formulario de inicio de sesión
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();

            // Obtener valores del formulario
            const username = document.querySelector("input[name='username']").value;
            const password = document.querySelector("input[name='password']").value;

            // Validar campos obligatorios
            if (!username || !password) {
                alert("Todos los campos son obligatorios.");
                return;
            }

            // Preparar datos del formulario para enviar
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            // Enviar datos al servidor
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
                    window.location.href = "home.html"; // Redirigir a la página principal
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

    // Mostrar nombre de usuario si está almacenado en localStorage
    if (username && usernameDisplay) {
        usernameDisplay.textContent = `Bienvenido, ${username}🏆`;
    }

    // Escuchar eventos de clic en botones de torneos
    tournamentButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const tournamentId = event.target.id;
            const id = localStorage.getItem('id');

            // Verificar si el usuario está autenticado
            if (!id) {
                alert('Por favor, inicia sesión para inscribirte en un torneo.');
                return;
            }

            // Preparar datos del formulario para enviar
            const formData = new FormData();
            formData.append('id', id);
            formData.append('tournament_id', tournamentId);

            // Enviar solicitud al servidor para inscribirse en un torneo
            fetch('/inscribir', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const inscripcionExitosa = `Tu inscripción fue exitosa, ${username} !🏆`;
                    mostrarModal(inscripcionExitosa);
                } else {
                    const inscripcionFallida = `Ya estás inscripto en este torneo, ${username}`;
                    mostrarModal(inscripcionFallida);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
            });
        });
    });

    // Función para mostrar la modal con un mensaje específico
    function mostrarModal(mensaje) {
        document.getElementById('tournament-list').innerHTML = mensaje;
        document.getElementById('modal').style.display = 'block'; // Mostrar la modal
    }
});

// Configurar el botón para cerrar la modal
const closeButton = document.getElementsByClassName('close')[0];
closeButton.onclick = function close() {
    document.getElementById('modal').style.display = 'none';
};

// Función para obtener los torneos inscritos del usuario
function misTorneos() {
    fetch('/mis-torneos', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar lista de torneos inscritos en la modal
            if (data.torneos.length > 0) {
                const tournamentList = "ESTÁS INSCRITO A:<br><br>" + data.torneos.join(' CUP ✅ <br>') + " CUP ✅";
                document.getElementById('tournament-list').innerHTML = tournamentList;
                document.getElementById('modal').style.display = 'block'; // Mostrar la modal
            } else {
                const sinTorneos = "No estás inscripto en ningún torneo aún!";
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
    });
}

// Función para cerrar sesión del usuario
function logout() {
    // Realizar solicitud de cerrar sesión al servidor
    fetch('/logout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Eliminar datos de sesión almacenados localmente
            localStorage.removeItem('username');
            localStorage.removeItem('id');
            // Redirigir después de unos segundos
            window.location.href = "index.html";
            // Evitar que el usuario vuelva atrás
            window.history.pushState(null, null, "index.html");
            window.addEventListener("popstate", function(event) {
                window.location.href = "index.html";
            });
        } else {
            alert('Error al cerrar sesión. Inténtelo de nuevo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error. Por favor, inténtelo de nuevo más tarde.');
    });
}



//Ventana emergente del chatbot
var chatOpen = false; // Variable para controlar el estado del chat

function toggleChat() {
    var chatContainer = document.getElementById('chat-container');
    if (!chatOpen) {
        chatContainer.style.display = 'block';
        chatOpen = true;
    } else {
        chatContainer.style.display = 'none';
        chatOpen = false;
    }
}

function mostrarBienvenida() {
    const mensaje_bienvenida = "¡Hola! Bienvenido a TorneosARG. ¿En qué puedo ayudarte?\n MENU:\n 1. Torneos\n 2. Horarios\n 3. Reglas";

    addMessageToChat("Chatbot", mensaje_bienvenida);
}

//Ventana del chatbot
document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("message");
    const chatMessages = document.getElementById("chat-messages");

    mostrarBienvenida();  //Dar mensaje de bienvenida al abrir el chatbot

    // Función para enviar el mensaje al presionar "Enter"
    messageInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});

//Logica del chatbot
async function sendMessage() {
    const message = document.getElementById("message").value;
    if (message.trim() === "") {
        return; // No enviar mensajes vacíos
    }

    // Mostrar el mensaje del usuario en el chat
    addMessageToChat("Usuario", message);

    // Enviar el mensaje al servidor
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });
    const data = await response.json();

    // Mostrar la respuesta del chatbot en el chat
    addMessageToChat("Chatbot", data.response);

    // Limpiar el campo de entrada
    document.getElementById("message").value = "";
}

function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById("chat-messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message");

    // Reemplazar \n por <br>
    const formattedMessage = message.replace(/\n/g, '<br>');

    messageElement.innerHTML = `<strong>${sender}:</strong> ${formattedMessage}`;
    chatMessages.appendChild(messageElement);

    // Hacer scroll hasta el final del chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
