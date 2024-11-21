const uploadImage = async (event) => {
    // Prevent any default behavior
    event.preventDefault();
    
    const imageInput = document.querySelector("#imageInput");
    const outputElement = document.querySelector("#output");

    if (!imageInput.files || imageInput.files.length === 0) {
        alert("Please select an image to upload.");
        return;
    }

    // Show loading state
    outputElement.textContent = "Processing...";

    const formData = new FormData();
    formData.append("file", imageInput.files[0]);

    try {
        console.log("Starting image upload...");
        console.log("Selected file:", imageInput.files[0].name);

        const response = await fetch("http://127.0.0.1:8000/process_image/", {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json",
            },
            mode: "cors",
        });

        console.log("Response received:", {
            status: response.status,
            statusText: response.statusText,
            headers: Object.fromEntries(response.headers.entries())
        });

        const data = await response.json();
        console.log("Processed result:", data);

        // Display the result
        outputElement.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("Error uploading image:", error);
        outputElement.textContent = `Error: ${error.message}`;
    }
};

// Add event listener when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.querySelector('#uploadButton');
    uploadButton.addEventListener('click', (event) => {
        uploadImage(event).catch(error => {
            console.error("Error in upload:", error);
            document.querySelector("#output").textContent = `Error: ${error.message}`;
        });
    });
});