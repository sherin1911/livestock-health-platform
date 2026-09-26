/* =========================================================
   UYIRTHULIR - AUTHENTICATION
   Login + Registration
   ========================================================= */

(function () {
    "use strict";

    const API_BASE = "http://127.0.0.1:5000/api";

    const TOKEN_KEYS = [
        "uyirthulir_token",
        "access_token",
        "token"
    ];

    const USER_KEYS = [
        "uyirthulir_user",
        "current_user",
        "user"
    ];

    /* ---------------------------------------------------------
       Helper: get element safely
       --------------------------------------------------------- */
    function getElement(...ids) {
        for (const id of ids) {
            const element = document.getElementById(id);
            if (element) {
                return element;
            }
        }
        return null;
    }

    /* ---------------------------------------------------------
       Helper: show message
       --------------------------------------------------------- */
    function showAuthMessage(message, type = "error") {
        const box = getElement(
            "authMessage",
            "auth-message",
            "message",
            "formMessage"
        );

        if (!box) {
            alert(message);
            return;
        }

        box.textContent = message;
        box.className = "auth-message " + type;
        box.style.display = "block";
    }

    /* ---------------------------------------------------------
       Helper: save authentication
       --------------------------------------------------------- */
    function saveAuthentication(token, user) {
        TOKEN_KEYS.forEach((key) => {
            localStorage.setItem(key, token);
        });

        USER_KEYS.forEach((key) => {
            localStorage.setItem(key, JSON.stringify(user));
        });
    }

    /* ---------------------------------------------------------
       Helper: remove authentication
       --------------------------------------------------------- */
    function clearAuthentication() {
        TOKEN_KEYS.forEach((key) => {
            localStorage.removeItem(key);
        });

        USER_KEYS.forEach((key) => {
            localStorage.removeItem(key);
        });
    }

    /* ---------------------------------------------------------
       Helper: redirect by role
       --------------------------------------------------------- */
    function redirectByRole(role) {
        const normalizedRole = String(role || "FARMER").toUpperCase();

        const pages = {
            FARMER: "farmer-dashboard.html",
            FIELD_WORKER: "farmer-dashboard.html",
            VETERINARIAN: "veterinary-dashboard.html",
            LAB_STAFF: "laboratory.html",
            DISTRICT_OFFICER: "government-dashboard.html",
            STATE_ADMIN: "government-dashboard.html",
            SUPER_ADMIN: "government-dashboard.html"
        };

        const page = pages[normalizedRole] || "farmer-dashboard.html";

        window.location.href = page;
    }

    /* ---------------------------------------------------------
       Login
       --------------------------------------------------------- */
    async function handleLogin(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        const usernameInput = getElement(
            "username",
            "loginUsername",
            "login-username",
            "email"
        );

        const passwordInput = getElement(
            "password",
            "loginPassword",
            "login-password"
        );

        const button = getElement(
            "loginBtn",
            "loginButton",
            "login-button"
        );

        if (!usernameInput || !passwordInput) {
            showAuthMessage(
                "Login form fields were not found. Please refresh the page.",
                "error"
            );
            return;
        }

        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        if (!username) {
            showAuthMessage("Please enter your username or email.", "error");
            usernameInput.focus();
            return;
        }

        if (!password) {
            showAuthMessage("Please enter your password.", "error");
            passwordInput.focus();
            return;
        }

        if (button) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = "Logging in...";
        }

        showAuthMessage("Checking your account...", "info");

        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            let data = {};

            try {
                data = await response.json();
            } catch (jsonError) {
                throw new Error(
                    "The server returned an invalid response."
                );
            }

            if (!response.ok || !data.success) {
                const errorMessage =
                    data.message ||
                    data.error ||
                    "Invalid username/email or password.";

                showAuthMessage(errorMessage, "error");
                return;
            }

            const token =
                data.access_token ||
                data.token ||
                data.data?.access_token ||
                data.data?.token;

            const user =
                data.user ||
                data.data?.user ||
                {
                    username: username
                };

            if (!token) {
                showAuthMessage(
                    "Login succeeded, but the server did not return an access token.",
                    "error"
                );
                return;
            }

            saveAuthentication(token, user);

            showAuthMessage(
                "Login successful. Opening your dashboard...",
                "success"
            );

            setTimeout(() => {
                redirectByRole(user.role);
            }, 400);

        } catch (error) {
            console.error("Login error:", error);

            showAuthMessage(
                "Cannot connect to the backend. Make sure Flask is running on http://127.0.0.1:5000",
                "error"
            );
        } finally {
            if (button) {
                button.disabled = false;

                if (button.dataset.originalText) {
                    button.innerHTML = button.dataset.originalText;
                }
            }
        }
    }

    /* ---------------------------------------------------------
       Registration
       --------------------------------------------------------- */
    async function handleRegister(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        const nameInput = getElement(
            "name",
            "registerName",
            "register-name"
        );

        const emailInput = getElement(
            "email",
            "registerEmail",
            "register-email"
        );

        const usernameInput = getElement(
            "username",
            "registerUsername",
            "register-username"
        );

        const passwordInput = getElement(
            "password",
            "registerPassword",
            "register-password"
        );

        const confirmPasswordInput = getElement(
            "confirmPassword",
            "confirm_password",
            "registerConfirmPassword",
            "register-confirm-password"
        );

        const languageInput = getElement(
            "language",
            "registerLanguage",
            "register-language"
        );

        const button = getElement(
            "registerBtn",
            "registerButton",
            "register-button"
        );

        if (!nameInput || !emailInput || !usernameInput || !passwordInput) {
            showAuthMessage(
                "Registration form fields were not found. Please refresh the page.",
                "error"
            );
            return;
        }

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput
            ? confirmPasswordInput.value
            : password;
        const language = languageInput
            ? languageInput.value
            : "en";

        if (!name) {
            showAuthMessage("Please enter your name.", "error");
            nameInput.focus();
            return;
        }

        if (!email) {
            showAuthMessage("Please enter your email.", "error");
            emailInput.focus();
            return;
        }

        if (!username) {
            showAuthMessage("Please enter a username.", "error");
            usernameInput.focus();
            return;
        }

        if (password.length < 6) {
            showAuthMessage(
                "Password must contain at least 6 characters.",
                "error"
            );
            passwordInput.focus();
            return;
        }

        if (password !== confirmPassword) {
            showAuthMessage(
                "Passwords do not match.",
                "error"
            );
            if (confirmPasswordInput) {
                confirmPasswordInput.focus();
            }
            return;
        }

        if (button) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = "Creating account...";
        }

        showAuthMessage(
            "Creating your farmer account...",
            "info"
        );

        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    username: username,
                    password: password,
                    language: language,
                    role: "FARMER"
                })
            });

            let data = {};

            try {
                data = await response.json();
            } catch (jsonError) {
                throw new Error(
                    "The server returned an invalid response."
                );
            }

            if (!response.ok || !data.success) {
                const errorMessage =
                    data.message ||
                    data.error ||
                    "Registration failed.";

                showAuthMessage(errorMessage, "error");
                return;
            }

            showAuthMessage(
                "Account created successfully. Redirecting to login...",
                "success"
            );

            setTimeout(() => {
                window.location.href = "login.html";
            }, 700);

        } catch (error) {
            console.error("Registration error:", error);

            showAuthMessage(
                "Cannot connect to the backend. Make sure Flask is running on http://127.0.0.1:5000",
                "error"
            );
        } finally {
            if (button) {
                button.disabled = false;

                if (button.dataset.originalText) {
                    button.innerHTML = button.dataset.originalText;
                }
            }
        }
    }

    /* ---------------------------------------------------------
       Password show/hide
       --------------------------------------------------------- */
    function setupPasswordToggle() {
        const toggle = getElement(
            "togglePassword",
            "passwordToggle",
            "toggle-password"
        );

        const passwordInput = getElement(
            "password",
            "loginPassword",
            "login-password",
            "registerPassword",
            "register-password"
        );

        if (!toggle || !passwordInput) {
            return;
        }

        toggle.addEventListener("click", function (event) {
            event.preventDefault();

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                toggle.textContent = "Hide";
            } else {
                passwordInput.type = "password";
                toggle.textContent = "Show";
            }
        });
    }

    /* ---------------------------------------------------------
       Login/Register form setup
       --------------------------------------------------------- */
    function initialiseAuth() {
        const loginForm = getElement(
            "loginForm",
            "login-form",
            "login-form-element"
        );

        const registerForm = getElement(
            "registerForm",
            "register-form",
            "register-form-element"
        );

        if (loginForm) {
            loginForm.addEventListener("submit", handleLogin);
        }

        if (registerForm) {
            registerForm.addEventListener("submit", handleRegister);
        }

        setupPasswordToggle();

        console.log("UyirThulir authentication loaded.");
    }

    /* ---------------------------------------------------------
       Expose functions globally
       --------------------------------------------------------- */
    window.UyirThulirAuth = {
        login: handleLogin,
        register: handleRegister,
        saveAuthentication: saveAuthentication,
        clearAuthentication: clearAuthentication
    };

    window.handleLogin = handleLogin;
    window.handleRegister = handleRegister;

    /* ---------------------------------------------------------
       Start after DOM is ready
       --------------------------------------------------------- */
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initialiseAuth);
    } else {
        initialiseAuth();
    }

})();