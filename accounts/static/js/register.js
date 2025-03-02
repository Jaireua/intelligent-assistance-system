/**
 * Script para la funcionalidad de registro con reconocimiento facial
 * Este archivo maneja la captura de la cámara y el envío del formulario de registro
 */

// Obtener referencias a los elementos del DOM
// Get references to the video, canvas, and buttons
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
const registerForm = document.getElementById('register-form');
const messageDiv = document.getElementById('message');

// Variable para almacenar la imagen capturada
let capturedImage = null;

/**
 * Acceder a la cámara e iniciar la transmisión de video
 * Access the camera and start the video stream
 */
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        // Asignar el stream de la cámara al elemento de video
        video.srcObject = stream;
    })
    .catch((err) => {
        // Manejar errores de acceso a la cámara
        console.log('Error accessing camera: ' + err);
        messageDiv.innerText = 'Camera not accessible. Please check permissions.';
        messageDiv.style.color = '#f44336';
    });

/**
 * Capturar imagen de la transmisión de video
 * Capture image from the video stream
 */
captureButton.addEventListener('click', () => {
    // Verificar si la cámara está disponible
    if (!video.srcObject) {
        messageDiv.innerText = "Please enable the camera.";
        messageDiv.style.color = '#f44336';
        return;
    }
    
    // Dibujar el fotograma de video actual en el canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);  // Dibujar fotograma de video en el canvas
    
    // Convertir la imagen capturada a formato base64
    capturedImage = canvas.toDataURL('image/jpeg'); // Convertir imagen capturada a formato base64
    
    // Mostrar mensaje de éxito
    messageDiv.innerText = "Face captured successfully!";
    messageDiv.style.color = '#4CAF50';
});

/**
 * Manejar el envío del formulario
 * Handle form submission
 */
registerForm.onsubmit = async (e) => {
    // Prevenir el comportamiento predeterminado del formulario
    e.preventDefault();

    // Verificar si se ha capturado una imagen facial
    if (!capturedImage) {
        messageDiv.innerText = "Please capture your face first.";
        messageDiv.style.color = '#f44336';
        return;
    }

    // Preparar los datos del formulario para el envío
    const formData = new FormData(registerForm);
    formData.append('face_image', capturedImage);

    try {
        // Enviar la solicitud al servidor
        const response = await fetch('/register/', {
            method: 'POST',
            body: formData
        });

        // Procesar la respuesta del servidor
        const data = await response.json();
        
        if (data.status === 'success') {
            // Mostrar mensaje de éxito
            messageDiv.innerText = data.message || 'Registration successful!';
            messageDiv.style.color = '#4CAF50';
            
            // Limpiar el formulario después del registro exitoso
            document.getElementById('username').value = '';
            capturedImage = null;
            
            // Redirigir a la página de inicio de sesión después de 2 segundos
            setTimeout(() => {
                window.location.href = '/login/';
            }, 2000);
        } else {
            // Mostrar mensaje de error
            messageDiv.innerText = data.message || 'Registration failed.';
            messageDiv.style.color = '#f44336';
        }
    } catch (error) {
        // Manejar errores de la solicitud
        console.error('Error:', error);
        messageDiv.innerText = 'An error occurred during registration.';
        messageDiv.style.color = '#f44336';
    }
};