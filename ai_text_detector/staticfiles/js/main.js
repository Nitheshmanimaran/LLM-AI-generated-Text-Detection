document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('textForm');
    const loadingDiv = document.getElementById('loading');
    const progressBar = document.getElementById('progressBar');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const text = document.getElementById('inputText').value;
        
        // Show loading bar
        loadingDiv.style.display = 'block';
        resultDiv.innerHTML = '';
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress > 90) clearInterval(interval);
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }, 100);

        fetch('/api/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: text})
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(interval);
            progressBar.style.width = '100%';
            progressBar.textContent = '100%';
            progressBar.setAttribute('aria-valuenow', 100);
            
            setTimeout(() => {
                loadingDiv.style.display = 'none';
                const resultText = `Probability of being AI-generated: ${(data.probability * 100).toFixed(2)}%<br>
                                    Result: ${data.is_ai_generated ? 'AI-generated' : 'Human written'}`;
                resultDiv.innerHTML = `<div class="alert alert-info">${resultText}</div>`;
            }, 500);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingDiv.style.display = 'none';
            resultDiv.innerHTML = '<div class="alert alert-danger">An error occurred. Please try again.</div>';
        });
    });
});