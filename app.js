document.getElementById('submitBtn').addEventListener('click', async () => {
    const referenceImage = document.getElementById('referenceImage').files[0];
    const zipFile = document.getElementById('zipFile').files[0];

    if (!referenceImage || !zipFile) {
        alert('Please upload both reference image and ZIP file.');
        return;
    }

    const formData = new FormData();
    formData.append('referenceImage', referenceImage);
    formData.append('zipFile', zipFile);

    try {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/compare', true);
        
        xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                document.getElementById('progress').innerText = `Upload progress: ${percentComplete.toFixed(2)}%`;
            }
        };

        xhr.onload = () => {
            if (xhr.status === 200) {
                const result = JSON.parse(xhr.responseText);
                document.getElementById('results').innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
            } else {
                console.error('Error:', xhr.statusText);
            }
        };

        xhr.onerror = () => console.error('Error:', xhr.statusText);

        xhr.send(formData);
    } catch (error) {
        console.error('Error:', error);
    }
});
