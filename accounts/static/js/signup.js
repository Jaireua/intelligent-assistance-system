// Encapsulation JS
document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const signupForm = document.getElementById('signup-form');
    const message = document.getElementById('message');
    let capturedImage = null;

    // Access the camera and start the video stram
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error('Error accessing the camera:', err);
            message.innerText = 'Camera not accessible. Please check permissions.';
        });
});