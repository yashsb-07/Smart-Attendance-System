document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const captureButton = document.getElementById("capture");
    const statusDiv = document.getElementById("status");
    const context = canvas.getContext("2d");
  
    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
      })
      .catch((error) => {
        console.error("Error accessing webcam:", error);
      });
  
    // Capture Image and Send to Backend
    captureButton.addEventListener("click", function () {
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imageData = canvas.toDataURL("image/png");
  
      fetch("/register-student", {
        method: "POST",
        body: JSON.stringify({ image: imageData }),
        headers: { "Content-Type": "application/json" }
      })
      .then(response => response.json())
      .then(data => {
        statusDiv.innerHTML = `<strong>${data.message}</strong>`;
      })
      .catch(error => {
        statusDiv.innerHTML = `<span style="color: red;">Error: ${error}</span>`;
      });
    });
  });
  