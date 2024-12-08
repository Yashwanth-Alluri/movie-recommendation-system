async function getRecommendations() {
    const movieName = document.getElementById('movieInput').value;
    const backendURL = "https://movie-recommendation-system-whek.onrender.com";

    const response = await fetch(`${backendURL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_name: movieName })
    });

    const data = await response.json();
    const recommendations = data.recommendations;

    let resultHTML = `<h2>Your Recommendations:</h2>`;
    if (recommendations.length > 0) {
        resultHTML += `<div class="movie-grid">` +
            recommendations.map(movie => `
                <div class="movie-card">
                    <img src="${movie.poster}" alt="${movie.title}">
                    <p>${movie.title}</p>
                </div>
            `).join('') +
            `</div>`;
    } else {
        // Display a clean "movie not found" message
        resultHTML += `<p class="not-found-message">Movie not found. Please try another title or correct the spelling.</p>`;
    }

    document.getElementById('results').innerHTML = resultHTML;
}

async function fetchSuggestions() {
    const query = document.getElementById('movieInput').value;

    if (query.length > 0) {
        const response = await fetch(`${backendURL}/suggest?q=${query}`);
        const data = await response.json();
        const suggestions = data.suggestions;

        const suggestionsList = document.getElementById('suggestions');
        suggestionsList.style.display = suggestions.length > 0 ? 'block' : 'none';
        suggestionsList.innerHTML = suggestions
            .map(movie => `<li class="list-group-item suggestion-item">${movie}</li>`)
            .join('');

        document.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function () {
                document.getElementById('movieInput').value = this.textContent;
                suggestionsList.style.display = 'none';
            });
        });
    } else {
        document.getElementById('suggestions').style.display = 'none';
    }
}

// Hide suggestions when clicking outside
document.addEventListener('click', function (e) {
    if (!document.querySelector('.input-group').contains(e.target)) {
        document.getElementById('suggestions').style.display = 'none';
    }
});