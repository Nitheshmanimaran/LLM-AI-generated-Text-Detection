document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('text-form');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const text = document.getElementById('input-text').value;
        
        // Show loading
        loadingDiv.style.display = 'block';
        resultDiv.innerHTML = '';

        fetch('/api/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({text: text})
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = 'none';
            resultDiv.innerHTML = `
                <p>Probability of AI-generated text: ${(data.probability * 100).toFixed(2)}%</p>
                <p>Verdict: ${data.is_ai_generated ? 'AI-generated' : 'Human-written'}</p>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            loadingDiv.style.display = 'none';
            resultDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});