const uploadImage = async () => {
    const imageInput = document.querySelector("#imageInput");
    const formData = new FormData();
    formData.append("file", imageInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        console.log("Uploaded file:", data);
    } catch (error) {
        console.error("Error uploading image:", error);
    }
};
