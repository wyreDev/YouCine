document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const message = document.getElementById('message');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        if (response.ok && result.success) {
            window.location.href = 'wyreupdate.html';
        } else {
            message.textContent = result.message || 'Invalid username or password';
        }
    } catch (error) {
        console.error('Login error:', error);
        message.textContent = 'Unable to login. Please try again later.';
    }
});