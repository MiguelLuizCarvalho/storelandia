const loginCard = document.getElementById('login-card');
const registerCard = document.getElementById('register-card');
const btnToRegister = document.getElementById('sign-up-option');
const btnToLogin = document.getElementById('sign-in-option');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');

registerBtn.addEventListener('click', async (e) => {
    e.preventDefault();

    const username = document.getElementById('register-username')?.value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const role = document.getElementById('role-form').value;

    if (password !== confirmPassword) {
        alert("As senhas não coincidem! Digite novamente.");
        return;
    }

    const data = {
        username: username || email.split('@')[0],
        email: email,
        password: password,
        role: role
    };

    const response = await fetch('/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
        alert("Account created successfully! Please log in.");
        registerCard.style.display = 'none';
        loginCard.style.display = 'block';
    } else {
        alert(result.message);
    }
});

registerCard.style.display = 'none';

btnToRegister.addEventListener('click', (e) => {
    e.preventDefault();
    loginCard.style.display = 'none';
    registerCard.style.display = 'block';
});

btnToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    registerCard.style.display = 'none';
    loginCard.style.display = 'block';
});

loginBtn.addEventListener('click', async () => {
    const loginInput = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = {
        login: loginInput,
        password: password,
    };

    const response = await fetch('/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error('Server error:', errorText);
        alert('An error occured during login. See the console.')
        return;

        // Store the token in local Storage for later use.
        localStorage.setItem('token', result.token);

        // Redirect based on user role selected during registration
        if (result.role === 'seller') {
            window.location.href = '/seller.html';
        } else {
            window.location.href = '/customer.html';
        }

    } else {
        alert(result.message);
    }

    const result = await response.json();
});

function setupPasswordToggle(toggleId, inputId) {
    const toggle = document.getElementById(toggleId);
    const input = document.getElementById(inputId);

    if (toggle && input) {
        toggle.addEventListener('click', function () {
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);

            const icon = this.querySelector('i');
            icon.classList.toggle('bi-eye');
            icon.classList.toggle('bi-eye-slash');
        });
    }
}

setupPasswordToggle('togglePasswordLogin', 'login-password');

setupPasswordToggle('togglePasswordRegister', 'register-password');
