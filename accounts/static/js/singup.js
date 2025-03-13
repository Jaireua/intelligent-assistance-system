// Encapsulation code JS
document.addEventListener('DOMContentLoaded', function () {
    // Get references to HTML elements
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const signupForm = document.getElementById('signup-form');
    const message = document.getElementById('message');
    let capturedImage = null;

    // Access the camera and start the video stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error('Error accessing the camera:', err);
            message.innerText = 'Camera not accessible. Please check your camera permissions.';
        });

    // Capture image from the video stream
    captureButton.addEventListener('click', () => {
        if (!video.srcObject) {
            message.innerText = 'Please enable the camera.';
            return;
        }

        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        capturedImage = canvas.toDataURL('image/png');
        message.innerText = 'Image captured successfully.';
    })

    //Handle form submission
    signupForm.onsubmit = async (e) => {
        e.preventDefault();
        if(!capturedImage) {
            message.innerText = 'Please capture your face first.';
            return;
        }

        const formData = new FormData(signupForm);
        formData.append('face_image', capturedImage);

        const response = await fetch('/signup/',{
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        message.innerText = data.message || 'Signup failed.';
    }
});