document.addEventListener('DOMContentLoaded', function() {
    // Get references to the video, canvas, and buttons
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-button');
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');

    let capturedImage = null;

    // Access the camera and start the video stream
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
                video.play(); // Añadimos play explícitamente
            })
            .catch((err) => {
                console.log('Error accessing camera: ' + err);
                messageDiv.innerText = 'Camera not accessible. Please check permissions.';
            });
    } else {
        messageDiv.innerText = 'getUserMedia is not supported in this browser.';
    }

    // Capture image from the video stream
    captureButton.addEventListener('click', () => {
        if (!video.srcObject) {
            messageDiv.innerText = "Camera is not available.";
            return;
        }

        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);  // Draw video frame to canvas
        capturedImage = canvas.toDataURL('image/jpeg'); // Convert captured image to base64 format

        messageDiv.innerText = "Face captured successfully! Ready to login.";
    });

    // Handle form submission
    loginForm.onsubmit = async (e) => {
        e.preventDefault();

        if (!capturedImage) {
            messageDiv.innerText = "Please capture your face first.";
            return;
        }

        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('face_image', capturedImage);

        try {
            const response = await fetch('/login/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                messageDiv.innerText = data.message || 'Login successful!';
            } else {
                messageDiv.innerText = data.message || 'Login failed.';
            }
        } catch (error) {
            console.error('Error:', error);
            messageDiv.innerText = 'An error occurred while processing your login.';
        }
    };
});