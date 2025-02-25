// Get references to the video, canvas, and buttons
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
const registerForm = document.getElementById('register-form');
const messageDiv = document.getElementById('message');

let capturedImage = null;

// Access the camera and start the video stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.log('Error accessing camera: ' + err);
        messageDiv.innerText = 'Camera not accessible. Please check permissions.';
    });

// Capture image from the video stream
captureButton.addEventListener('click', () => {
    if (!video.srcObject) {
        messageDiv.innerText = "Please enable the camera.";
        return;
    }
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);  // Draw video frame to canvas
    capturedImage = canvas.toDataURL('image/jpeg'); // Convert captured image to base64 format
    messageDiv.innerText = "Face captured successfully!";
});

// Handle form submission
registerForm.onsubmit = async (e) => {
    e.preventDefault();

    if (!capturedImage) {
        messageDiv.innerText = "Please capture your face first.";
        return;
    }

    const formData = new FormData(registerForm);
    formData.append('face_image', capturedImage);

    const response = await fetch('/register/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    messageDiv.innerText = data.message || 'Registration failed.';
};