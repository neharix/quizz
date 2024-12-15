const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
let isUploaded = false;
let contentContainer = document.querySelector("#content");
let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0];

function toggleBtn(e) {
  if (isMobile) {
    if (isUploaded) {
      document.getElementById("submitBtn").click();
    } else {
      document.getElementById("cameraInput").click();
    }
  }
}

if (isMobile) {
  contentContainer.innerHTML = `
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken.value}">
            <input type="file"
                   name="image"
                   accept="image/*"
                   capture="user"
                   id="cameraInput"
                   class="d-none">
            <input type="submit" class="d-none" id="submitBtn" value="Submit">
        </form>
        <div class="d-flex justify-content-center align-items-center"
             style="height: 50vh">
            <button class="btn btn-ui-design p-3" style="border-radius: 10%" id="mainBtn">
                <svg xmlns="http://www.w3.org/2000/svg"
                     fill="#ffffff"
                     width="50vw"
                     viewBox="0 0 512 512">
                    <!--! Font Awesome Free 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
                    <path d="M149.1 64.8L138.7 96H64C28.7 96 0 124.7 0 160V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V160c0-35.3-28.7-64-64-64H373.3L362.9 64.8C356.4 45.2 338.1 32 317.4 32H194.6c-20.7 0-39 13.2-45.5 32.8zM256 384c-53 0-96-43-96-96s43-96 96-96s96 43 96 96s-43 96-96 96z" />
                </svg>
            </button>
        </div>
    `;
  let mainBtn = document.getElementById("mainBtn");
  mainBtn.onclick = toggleBtn;
  document.getElementById("cameraInput").addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      isUploaded = true;
      mainBtn.innerHTML = `
        <svg fill="#ffffff" width="50vw" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
            <!--! Font Awesome Free 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
            <path d="M224 256c-35.2 0-64 28.8-64 64c0 35.2 28.8 64 64 64c35.2 0 64-28.8 64-64C288 284.8 259.2 256 224 256zM433.1 129.1l-83.9-83.9C341.1 37.06 328.8 32 316.1 32H64C28.65 32 0 60.65 0 96v320c0 35.35 28.65 64 64 64h320c35.35 0 64-28.65 64-64V163.9C448 151.2 442.9 138.9 433.1 129.1zM128 80h144V160H128V80zM400 416c0 8.836-7.164 16-16 16H64c-8.836 0-16-7.164-16-16V96c0-8.838 7.164-16 16-16h16v104c0 13.25 10.75 24 24 24h192C309.3 208 320 197.3 320 184V83.88l78.25 78.25C399.4 163.2 400 164.8 400 166.3V416z" />
        </svg>
        `;
    }
  });
} else {
  contentContainer.innerHTML = `
        <div id="camera-container" class="d-flex justify-content-center">
            <video id="video" height="10%" autoplay style="border-radius: 1.5rem;">
            </video>
            <canvas id="canvas" width="640" height="480" class="d-none"></canvas>
        </div>
        <div id="upload-container" style="display: none;"></div>
        <div class="d-flex justify-content-center mt-4">
            <button id="finalUpload" class="btn btn-ui-design">Ýüklemek</button>
        </div>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken.value}">
            <input type="file"
                   class="d-none"
                   name="image"
                   id="file-input"
                   accept="image/*">
            <input type="submit" class="d-none" id="submitBtn" value="Submit">
        </form>`;

  const cameraContainer = document.getElementById("camera-container");
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const fileInput = document.getElementById("file-input");
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
      video.play();
    })
    .catch((err) => {
      // If access to webcam is denied or not available, show file upload
      alert("No webcam found, showing file upload input.");
      cameraContainer.style.display = "none";
    });
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const context = canvas.getContext("2d");
          context.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
  $("#finalUpload").on("click", function () {
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      let date = Date.now();
      const file = new File([blob], `captured_image_${date}.png`, {
        type: "image/png",
      });
      console.log("file:::::::::::file", file); // This file object can now be uploaded to the server
      // Create a DataTransfer object and use it to set the file into the input element
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;
      // Optionally, trigger an event to handle the file upload logic if needed
      const event = new Event("change");
      fileInput.dispatchEvent(event);
    }, "image/png");
    setTimeout(() => {
      document.getElementById("submitBtn").click();
    }, 500);
  });
}

document.querySelector("#policy").click();
