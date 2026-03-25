const video = document.getElementById('video');
const canvas = document.getElementById('faceCanvas');
const faceStatus = document.getElementById('faceStatus');
const instructionText = document.getElementById('instructionText');
const hiddenCanvas = document.getElementById('canvas');
const loader = document.getElementById('loader');
const progressCircle = document.getElementById("progressCircle");
const progressText = document.getElementById("progressText");

let autoCaptured = false;
let blinkDetected = false;
let progress = 0;
let faceDetectedOnce = false;
let lastSpokenTime = 0;

// ================= CAMERA =================
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
});

// Wait for video
video.addEventListener('loadedmetadata', async () => {
    await loadModels();
    startFaceDetection();
});

// ================= LOAD MODELS =================
async function loadModels() {
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
    console.log("Face API Models Loaded");
}

// ================= BLINK DETECTION =================
function isBlinking(landmarks) {
    const leftEye = landmarks.getLeftEye();
    const rightEye = landmarks.getRightEye();

    function eyeHeight(eye) {
        return Math.abs(eye[1].y - eye[5].y);
    }

    return eyeHeight(leftEye) < 4 && eyeHeight(rightEye) < 4;
}

// ================= FACE ALIGNMENT =================
function checkAlignment(landmarks) {
    const nose = landmarks.getNose()[3];
    const jaw = landmarks.getJawOutline();
    const faceCenter = (jaw[0].x + jaw[16].x) / 2;

    if (nose.x < faceCenter - 25) return "Move Right";
    if (nose.x > faceCenter + 25) return "Move Left";
    return "Aligned";
}

// ================= PROGRESS =================
function updateProgress() {
    if (progress >= 100) return;

    progress += 1.5;
    const offset = 377 - (377 * progress) / 100;
    progressCircle.style.strokeDashoffset = offset;
    progressText.innerText = Math.floor(progress) + "%";
}

function resetProgress() {
    progress = 0;
    progressCircle.style.strokeDashoffset = 377;
    progressText.innerText = "0%";
}

// ================= VOICE (Cooldown) =================
function speak(text) {
    const now = Date.now();
    if (now - lastSpokenTime < 3000) return;

    lastSpokenTime = now;

    if ('speechSynthesis' in window) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = "en-US";
        window.speechSynthesis.speak(speech);
    }
}

// ================= FACE DETECTION LOOP =================
function startFaceDetection() {
    const displaySize = {
        width: video.videoWidth,
        height: video.videoHeight
    };

    canvas.width = displaySize.width;
    canvas.height = displaySize.height;
    faceapi.matchDimensions(canvas, displaySize);

    async function detect() {
        const detections = await faceapi.detectAllFaces(video)
            .withFaceLandmarks();

        const resizedDetections = faceapi.resizeResults(detections, displaySize);

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

        if (detections.length > 0) {

            if (!faceDetectedOnce) {
                speak("Face detected");
                faceDetectedOnce = true;
            }

            faceStatus.innerText = "Face Detected";

            const landmarks = detections[0].landmarks;
            const alignment = checkAlignment(landmarks);
            instructionText.innerText = alignment;

            // Progress only when aligned
            if (alignment === "Aligned") {
                updateProgress();
            } else {
                resetProgress();
            }

            // Blink detection
            if (isBlinking(landmarks) && !blinkDetected) {
                blinkDetected = true;
                instructionText.innerText = "Blink Detected";
                speak("Blink detected");
            }

            // Capture
            if (alignment === "Aligned" && blinkDetected && progress >= 100 && !autoCaptured) {
                autoCaptured = true;
                instructionText.innerText = "Capturing...";
                speak("Capturing image");

                setTimeout(() => {
                    captureImage();
                }, 800);
            }

        } else {
            faceStatus.innerText = "No Face Detected";
            instructionText.innerText = "Align your face";
            faceDetectedOnce = false;
            blinkDetected = false;
            autoCaptured = false;
            resetProgress();
        }

        requestAnimationFrame(detect);
    }

    detect();
}

// ================= CAPTURE IMAGE =================
function captureImage() {
    const context = hiddenCanvas.getContext('2d');

    hiddenCanvas.width = video.videoWidth;
    hiddenCanvas.height = video.videoHeight;

    context.drawImage(video, 0, 0);

    const imageData = hiddenCanvas.toDataURL('image/jpeg', 0.7);
    document.getElementById('image_data').value = imageData;

    document.getElementById('captureSound').play();
    progressText.innerText = "Captured";
}

// ================= FORM SUBMIT =================
document.getElementById("registerForm").addEventListener("submit", function() {
    loader.style.display = "block";
});

// ================= SUCCESS OVERLAY =================
const successMessage = document.querySelector(".success-message");
if (successMessage) {
    document.getElementById("successAnimation").style.display = "flex";
    document.getElementById("successSound").play();

    setTimeout(() => {
        window.location.href = "/register_student";
    }, 2000);
}

// ================= PARTICLES =================
const particleCanvas = document.getElementById("particles");
const pctx = particleCanvas.getContext("2d");

particleCanvas.width = window.innerWidth;
particleCanvas.height = window.innerHeight;

let particlesArray = [];

for (let i = 0; i < 60; i++) {
    particlesArray.push({
        x: Math.random() * particleCanvas.width,
        y: Math.random() * particleCanvas.height,
        radius: Math.random() * 2,
        dx: Math.random() - 0.5,
        dy: Math.random() - 0.5
    });
}

function animateParticles() {
    pctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
    pctx.fillStyle = "#38bdf8";

    particlesArray.forEach(p => {
        pctx.beginPath();
        pctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        pctx.fill();

        p.x += p.dx;
        p.y += p.dy;

        if (p.x < 0 || p.x > particleCanvas.width) p.dx *= -1;
        if (p.y < 0 || p.y > particleCanvas.height) p.dy *= -1;
    });

    requestAnimationFrame(animateParticles);
}

animateParticles();