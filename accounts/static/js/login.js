/**
 * Script para la funcionalidad de inicio de sesión con reconocimiento facial
 * Este archivo maneja la captura de la cámara y el envío del formulario de inicio de sesión
 */

document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos del DOM
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-button');
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');
    
    // Variable para almacenar la imagen capturada
    let capturedImage = null;

    /**
     * Acceder a la cámara e iniciar la transmisión de video
     */
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
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
    } else {
        // Mostrar mensaje si getUserMedia no es compatible
        messageDiv.innerText = 'getUserMedia is not supported in this browser.';
        messageDiv.style.color = '#f44336';
    }

    /**
     * Capturar imagen de la transmisión de video
     */
    captureButton.addEventListener('click', () => {
        // Verificar si la cámara está disponible
        if (!video.srcObject) {
            messageDiv.innerText = "Camera is not available.";
            messageDiv.style.color = '#f44336';
            return;
        }

        // Dibujar el fotograma de video actual en el canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convertir la imagen capturada a formato base64
        capturedImage = canvas.toDataURL('image/jpeg');

        // Mostrar mensaje de éxito
        messageDiv.innerText = "Face captured successfully! Ready to login.";
        messageDiv.style.color = '#4CAF50';
    });

    /**
     * Manejar el envío del formulario
     */
    loginForm.onsubmit = async (e) => {
        // Prevenir el comportamiento predeterminado del formulario
        e.preventDefault();

        // Verificar si se ha capturado una imagen facial
        if (!capturedImage) {
            messageDiv.innerText = "Please capture your face first.";
            messageDiv.style.color = '#f44336';
            return;
        }

        // Preparar los datos del formulario para el envío
        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('face_image', capturedImage);

        try {
            // Mostrar mensaje de verificación
            messageDiv.innerText = "Verifying...";
            messageDiv.style.color = '#007bff';
            
            // Enviar la solicitud al servidor
            const response = await fetch('/login/', {
                method: 'POST',
                body: formData
            });

            // Procesar la respuesta del servidor
            const data = await response.json();
            
            if (data.status === 'success') {
                // Mostrar mensaje de éxito
                messageDiv.innerText = data.message || 'Login successful!';
                messageDiv.style.color = '#4CAF50';
                
                // Redirigir a la página principal inmediatamente después del inicio de sesión exitoso
                window.location.href = '/';
            } else {
                // Mostrar mensaje de error
                messageDiv.innerText = data.message || 'Login failed.';
                messageDiv.style.color = '#f44336';
            }
        } catch (error) {
            // Manejar errores de la solicitud
            console.error('Error:', error);
            messageDiv.innerText = 'An error occurred while processing your login.';
            messageDiv.style.color = '#f44336';
        }
    };
});