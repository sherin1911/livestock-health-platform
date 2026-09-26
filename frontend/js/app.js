/* =========================================================
   UYIRTHULIR
   GLOBAL FRONTEND APPLICATION
========================================================= */

(function () {
    "use strict";


    /* =====================================================
       API CONFIGURATION
    ====================================================== */

    const API_BASE = "http://127.0.0.1:5000/api";

    window.API_BASE = API_BASE;


    /* =====================================================
       STORAGE KEYS
    ====================================================== */

    const TOKEN_KEY = "uyirthulir_token";
    const USER_KEY = "uyirthulir_user";

    window.TOKEN_KEY = TOKEN_KEY;
    window.USER_KEY = USER_KEY;


    /* =====================================================
       ROLE HOME PAGES
    ====================================================== */

    const ROLE_HOME = {
        FARMER: "farmer-dashboard.html",
        FIELD_WORKER: "farmer-dashboard.html",
        VETERINARIAN: "veterinary-dashboard.html",
        LAB_STAFF: "laboratory.html",
        DISTRICT_OFFICER: "government-dashboard.html",
        STATE_ADMIN: "government-dashboard.html",
        SUPER_ADMIN: "government-dashboard.html"
    };

    window.ROLE_HOME = ROLE_HOME;


    /* =====================================================
       PAGE ACCESS
    ====================================================== */

    const PAGE_ACCESS = {
        "farmer-dashboard.html": [
            "FARMER",
            "FIELD_WORKER"
        ],

        "report-health.html": [
            "FARMER",
            "FIELD_WORKER"
        ],

        "animals.html": [
            "FARMER",
            "FIELD_WORKER"
        ],

        "alerts.html": [
            "FARMER",
            "FIELD_WORKER",
            "VETERINARIAN",
            "DISTRICT_OFFICER",
            "STATE_ADMIN",
            "SUPER_ADMIN"
        ],

        "veterinary-dashboard.html": [
            "VETERINARIAN"
        ],

        "investigation.html": [
            "VETERINARIAN"
        ],

        "laboratory.html": [
            "LAB_STAFF"
        ],

        "government-dashboard.html": [
            "DISTRICT_OFFICER",
            "STATE_ADMIN",
            "SUPER_ADMIN"
        ],

        "gis-surveillance.html": [
            "DISTRICT_OFFICER",
            "STATE_ADMIN",
            "SUPER_ADMIN"
        ]
    };

    window.PAGE_ACCESS = PAGE_ACCESS;


    /* =====================================================
       TOKEN HELPERS
    ====================================================== */

    function getToken() {
        return (
            localStorage.getItem(TOKEN_KEY) ||
            localStorage.getItem("access_token") ||
            localStorage.getItem("token") ||
            ""
        );
    }

    window.getToken = getToken;


    function saveToken(token) {
        if (!token) {
            return;
        }

        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem("access_token", token);
    }


    function removeToken() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem("access_token");
        localStorage.removeItem("token");
    }


    /* =====================================================
       USER HELPERS
    ====================================================== */

    function getStoredUser() {
        const userText = localStorage.getItem(USER_KEY);

        if (!userText) {
            return null;
        }

        try {
            return JSON.parse(userText);
        } catch (error) {
            localStorage.removeItem(USER_KEY);
            return null;
        }
    }

    window.getStoredUser = getStoredUser;


    function saveUser(user) {
        if (!user) {
            return;
        }

        localStorage.setItem(
            USER_KEY,
            JSON.stringify(user)
        );
    }

    window.saveUser = saveUser;


    function clearUser() {
        localStorage.removeItem(USER_KEY);
    }


    function getCurrentRole() {
        const user = getStoredUser();

        if (!user || !user.role) {
            return null;
        }

        return String(user.role).trim().toUpperCase();
    }

    window.getCurrentRole = getCurrentRole;


    function getCurrentUsername() {
        const user = getStoredUser();

        if (!user) {
            return null;
        }

        return user.username || null;
    }

    window.getCurrentUsername = getCurrentUsername;


    /* =====================================================
       LOGIN CHECK
    ====================================================== */

    function isLoggedIn() {
        return Boolean(getToken());
    }

    window.isLoggedIn = isLoggedIn;


    /* =====================================================
       CURRENT PAGE
    ====================================================== */

    function getCurrentPageName() {
        const path = window.location.pathname;

        const pageName = path
            .split("/")
            .filter(Boolean)
            .pop();

        return pageName || "index.html";
    }


    /* =====================================================
       PAGE PATH
    ====================================================== */

    function getPagePath(pageName) {
        const currentPath = window.location.pathname;

        const inPagesFolder =
            currentPath.includes("/frontend/pages/");

        if (inPagesFolder) {
            return pageName;
        }

        return "pages/" + pageName;
    }


    /* =====================================================
       ROLE HOME URL
    ====================================================== */

    function getRoleHome(role) {
        const normalizedRole =
            String(role || "")
                .trim()
                .toUpperCase();

        const page = ROLE_HOME[normalizedRole];

        if (!page) {
            return getPagePath("login.html");
        }

        return getPagePath(page);
    }

    window.getRoleHome = getRoleHome;


    /* =====================================================
       AUTH REDIRECT
    ====================================================== */

    function redirectToLogin() {
        window.location.href =
            getPagePath("login.html");
    }

    window.redirectToLogin = redirectToLogin;


    function redirectToRoleHome() {
        const role = getCurrentRole();

        if (!role) {
            redirectToLogin();
            return;
        }

        window.location.href =
            getRoleHome(role);
    }

    window.redirectToRoleHome = redirectToRoleHome;


    /* =====================================================
       ROLE ACCESS CHECK
    ====================================================== */

    function pageRequiresAuthentication() {
        const pageName =
            getCurrentPageName();

        return Object.prototype.hasOwnProperty.call(
            PAGE_ACCESS,
            pageName
        );
    }


    function enforceRoleAccess() {
        const pageName =
            getCurrentPageName();

        const allowedRoles =
            PAGE_ACCESS[pageName];

        if (!allowedRoles) {
            return;
        }

        if (!isLoggedIn()) {
            redirectToLogin();
            return;
        }

        const role = getCurrentRole();

        if (!role) {
            redirectToLogin();
            return;
        }

        if (!allowedRoles.includes(role)) {
            showToast(
                getTranslation(
                    "unauthorized",
                    "You are not authorized to access this page."
                ),
                "error"
            );

            setTimeout(
                function () {
                    window.location.href =
                        getRoleHome(role);
                },
                700
            );
        }
    }

    window.enforceRoleAccess =
        enforceRoleAccess;


    /* =====================================================
       TRANSLATION HELPER
    ====================================================== */

    function getTranslation(key, fallback) {
        if (typeof window.t === "function") {
            const translated =
                window.t(key);

            if (
                translated &&
                translated !== key
            ) {
                return translated;
            }
        }

        return fallback || key;
    }


    /* =====================================================
       NAVIGATION
    ====================================================== */

    function setupNavigation() {
        const user = getStoredUser();
        const role = getCurrentRole();

        document
            .querySelectorAll("[data-role-home]")
            .forEach(
                function (element) {
                    if (!role) {
                        return;
                    }

                    element.href =
                        getRoleHome(role);
                }
            );


        document
            .querySelectorAll("[data-logout]")
            .forEach(
                function (button) {
                    button.addEventListener(
                        "click",
                        function (event) {
                            event.preventDefault();
                            logout();
                        }
                    );
                }
            );


        const roleElements =
            document.querySelectorAll(
                "[data-user-role]"
            );

        roleElements.forEach(
            function (element) {
                if (role) {
                    element.textContent =
                        role.replaceAll(
                            "_",
                            " "
                        );
                }
            }
        );


        const usernameElements =
            document.querySelectorAll(
                "[data-user-name]"
            );

        usernameElements.forEach(
            function (element) {
                if (user && user.name) {
                    element.textContent =
                        user.name;
                }
            }
        );


        const usernameOnlyElements =
            document.querySelectorAll(
                "[data-username]"
            );

        usernameOnlyElements.forEach(
            function (element) {
                if (user && user.username) {
                    element.textContent =
                        user.username;
                }
            }
        );
    }


    /* =====================================================
       API REQUEST
    ====================================================== */

    async function apiRequest(
        endpoint,
        options = {}
    ) {
        const token = getToken();

        let url = endpoint;

        if (
            !endpoint.startsWith("http://") &&
            !endpoint.startsWith("https://")
        ) {
            if (endpoint.startsWith("/")) {
                url = API_BASE + endpoint;
            } else {
                url = API_BASE + "/" + endpoint;
            }
        }

        const headers = new Headers(
            options.headers || {}
        );


        if (
            !headers.has("Accept")
        ) {
            headers.set(
                "Accept",
                "application/json"
            );
        }


        const bodyIsFormData =
            options.body instanceof FormData;


        if (
            !bodyIsFormData &&
            options.body &&
            !headers.has("Content-Type")
        ) {
            headers.set(
                "Content-Type",
                "application/json"
            );
        }


        if (token) {
            headers.set(
                "Authorization",
                "Bearer " + token
            );
        }


        let response;

        try {
            response = await fetch(
                url,
                {
                    ...options,
                    headers: headers
                }
            );
        } catch (error) {
            showToast(
                getTranslation(
                    "connectionError",
                    "Unable to connect to the server."
                ),
                "error"
            );

            throw error;
        }


        let data = null;

        const contentType =
            response.headers.get(
                "content-type"
            ) || "";


        if (
            contentType.includes(
                "application/json"
            )
        ) {
            try {
                data = await response.json();
            } catch (error) {
                data = null;
            }
        } else {
            try {
                const text =
                    await response.text();

                data = text
                    ? {
                        message: text
                    }
                    : null;
            } catch (error) {
                data = null;
            }
        }


        if (
            response.status === 401
        ) {
            removeToken();
            clearUser();

            if (
                !window.location.pathname.includes(
                    "/login.html"
                )
            ) {
                showToast(
                    getTranslation(
                        "sessionExpired",
                        "Your session has expired. Please login again."
                    ),
                    "error"
                );

                setTimeout(
                    redirectToLogin,
                    500
                );
            }
        }


        if (!response.ok) {
            const errorMessage =
                data &&
                (
                    data.message ||
                    data.error
                )
                    ? (
                        data.message ||
                        data.error
                    )
                    : getTranslation(
                        "somethingWentWrong",
                        "Something went wrong. Please try again."
                    );

            const error =
                new Error(errorMessage);

            error.status =
                response.status;

            error.data = data;

            throw error;
        }


        return data;
    }

    window.apiRequest = apiRequest;


    /* =====================================================
       JSON API HELPER
    ====================================================== */

    async function apiJson(
        endpoint,
        method = "GET",
        body = null
    ) {
        const options = {
            method: method
        };

        if (body !== null) {
            options.body =
                JSON.stringify(body);
        }

        return apiRequest(
            endpoint,
            options
        );
    }

    window.apiJson = apiJson;


    /* =====================================================
       IMAGE / FILE URL
    ====================================================== */

    function getApiFileUrl(path) {
        if (!path) {
            return "";
        }

        if (
            path.startsWith("http://") ||
            path.startsWith("https://")
        ) {
            return path;
        }

        if (path.startsWith("/api/")) {
            return "http://127.0.0.1:5000" + path;
        }

        if (path.startsWith("/")) {
            return "http://127.0.0.1:5000" + path;
        }

        return API_BASE + "/" + path;
    }

    window.getApiFileUrl =
        getApiFileUrl;


    /* =====================================================
       TOAST SYSTEM
    ====================================================== */

    function ensureToastContainer() {
        let container =
            document.querySelector(
                ".toast-container"
            );

        if (container) {
            return container;
        }

        container =
            document.createElement("div");

        container.className =
            "toast-container";

        document.body.appendChild(
            container
        );

        return container;
    }


    function showToast(
        message,
        type = "info",
        duration = 3500
    ) {
        const container =
            ensureToastContainer();

        const toast =
            document.createElement("div");

        toast.className =
            "toast toast-" + type;

        toast.textContent =
            message || "";

        container.appendChild(
            toast
        );


        setTimeout(
            function () {
                toast.style.opacity = "0";
                toast.style.transform =
                    "translateY(-5px)";

                setTimeout(
                    function () {
                        toast.remove();
                    },
                    250
                );
            },
            duration
        );
    }

    window.showToast = showToast;


    /* =====================================================
       CONFIRMATION
    ====================================================== */

    function showConfirm(
        message,
        onConfirm
    ) {
        const confirmed =
            window.confirm(
                message
            );

        if (
            confirmed &&
            typeof onConfirm === "function"
        ) {
            onConfirm();
        }

        return confirmed;
    }

    window.showConfirm =
        showConfirm;


    /* =====================================================
       LOGOUT
    ====================================================== */

    async function logout() {
        try {
            if (getToken()) {
                await apiRequest(
                    "/auth/logout",
                    {
                        method: "POST"
                    }
                );
            }
        } catch (error) {
            // Local logout should still continue
            // even when the backend is unavailable.
        }


        removeToken();
        clearUser();

        localStorage.removeItem(
            "latestReport"
        );

        localStorage.removeItem(
            "reportHistory"
        );

        localStorage.removeItem(
            "selectedAnimal"
        );

        showToast(
            getTranslation(
                "logout",
                "Logout successful."
            ),
            "success"
        );


        setTimeout(
            redirectToLogin,
            300
        );
    }

    window.logout = logout;


    /* =====================================================
       LOGIN DATA HANDLER
    ====================================================== */

    function handleLoginResponse(data) {
        if (!data) {
            return false;
        }


        const token =
            data.access_token ||
            data.accessToken ||
            data.token;


        const user =
            data.user ||
            data.profile;


        if (token) {
            saveToken(token);
        }


        if (user) {
            saveUser(user);
        }


        return Boolean(
            token || user
        );
    }

    window.handleLoginResponse =
        handleLoginResponse;


    /* =====================================================
       REGISTER / LOGIN REDIRECTION
    ====================================================== */

    function redirectAfterLogin(user) {
        const role =
            user && user.role
                ? user.role
                : getCurrentRole();

        if (!role) {
            window.location.href =
                getPagePath(
                    "farmer-dashboard.html"
                );

            return;
        }

        window.location.href =
            getRoleHome(role);
    }

    window.redirectAfterLogin =
        redirectAfterLogin;


    /* =====================================================
       ROLE DISPLAY
    ====================================================== */

    function updateRoleUI() {
        const user = getStoredUser();

        if (!user) {
            return;
        }

        const role =
            String(
                user.role || ""
            )
                .replaceAll(
                    "_",
                    " "
                );


        document
            .querySelectorAll(
                "[data-user-role]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        role;
                }
            );


        document
            .querySelectorAll(
                "[data-user-name]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        user.name ||
                        user.username ||
                        "";
                }
            );


        document
            .querySelectorAll(
                "[data-user-email]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        user.email || "";
                }
            );
    }


    /* =====================================================
       LANGUAGE SELECTOR
    ====================================================== */

    function setupLanguageSelector() {
        const selectors =
            document.querySelectorAll(
                "#languageSelector, .language-selector"
            );

        const currentLanguage =
            typeof window.getCurrentLanguage ===
            "function"
                ? window.getCurrentLanguage()
                : "en";


        selectors.forEach(
            function (selector) {
                selector.value =
                    currentLanguage;


                if (
                    selector.dataset.languageBound ===
                    "true"
                ) {
                    return;
                }


                selector.dataset.languageBound =
                    "true";


                selector.addEventListener(
                    "change",
                    function (event) {
                        const language =
                            event.target.value;


                        if (
                            typeof window.setCurrentLanguage ===
                            "function"
                        ) {
                            window.setCurrentLanguage(
                                language
                            );
                        }


                        if (
                            typeof window.applyTranslations ===
                            "function"
                        ) {
                            window.applyTranslations();
                        }
                    }
                );
            }
        );
    }


    /* =====================================================
       ACTIVE NAVIGATION
    ====================================================== */

    function setupActiveNavigation() {
        const currentPage =
            getCurrentPageName();

        document
            .querySelectorAll(
                "a[href]"
            )
            .forEach(
                function (link) {
                    const href =
                        link.getAttribute(
                            "href"
                        );

                    if (!href) {
                        return;
                    }

                    if (
                        href.startsWith("#") ||
                        href.startsWith("http")
                    ) {
                        return;
                    }

                    const cleanHref =
                        href
                            .split("?")[0]
                            .split("#")[0];

                    const linkedPage =
                        cleanHref
                            .split("/")
                            .pop();

                    if (
                        linkedPage === currentPage
                    ) {
                        link.classList.add(
                            "active"
                        );
                    }
                }
            );
    }


    /* =====================================================
       ONLINE / OFFLINE STATUS
    ====================================================== */

    function setupConnectionStatus() {
        function updateStatus() {
            document.body.classList.toggle(
                "offline-mode",
                !navigator.onLine
            );
        }

        window.addEventListener(
            "online",
            updateStatus
        );

        window.addEventListener(
            "offline",
            updateStatus
        );

        updateStatus();
    }


    /* =====================================================
       GLOBAL AUTH INITIALISATION
    ====================================================== */

    async function initialiseAuthenticatedUser() {
        if (!isLoggedIn()) {
            return;
        }

        try {
            const data =
                await apiRequest(
                    "/auth/me",
                    {
                        method: "GET"
                    }
                );

            if (
                data &&
                data.user
            ) {
                saveUser(
                    data.user
                );
            }
        } catch (error) {
            // The existing stored user can still be used
            // when the backend is temporarily unavailable.
        }
    }


    /* =====================================================
       LOGIN PAGE GUARD
    ====================================================== */

    function redirectLoggedInUserFromAuthPages() {
        const currentPage =
            getCurrentPageName();

        const isAuthPage =
            currentPage === "login.html" ||
            currentPage === "register.html";

        if (
            !isAuthPage ||
            !isLoggedIn()
        ) {
            return;
        }

        const role =
            getCurrentRole();

        if (!role) {
            return;
        }

        window.location.href =
            getRoleHome(role);
    }


    /* =====================================================
       GLOBAL KEYBOARD SUPPORT
    ====================================================== */

    function setupKeyboardSupport() {
        document.addEventListener(
            "keydown",
            function (event) {
                if (
                    event.key === "Escape"
                ) {
                    document
                        .querySelectorAll(
                            ".modal-overlay.active"
                        )
                        .forEach(
                            function (modal) {
                                modal.classList.remove(
                                    "active"
                                );
                            }
                        );
                }
            }
        );
    }


    /* =====================================================
       INITIALISATION
    ====================================================== */

    async function initialiseApp() {
        setupLanguageSelector();

        if (
            typeof window.applyTranslations ===
            "function"
        ) {
            window.applyTranslations();
        }


        enforceRoleAccess();

        redirectLoggedInUserFromAuthPages();

        setupNavigation();

        updateRoleUI();

        setupActiveNavigation();

        setupConnectionStatus();

        setupKeyboardSupport();

        await initialiseAuthenticatedUser();

        setupNavigation();

        updateRoleUI();

        setupLanguageSelector();
    }


    /* =====================================================
       LANGUAGE CHANGE EVENT
    ====================================================== */

    window.addEventListener(
        "uyirthulirLanguageChanged",
        function () {
            setupLanguageSelector();

            if (
                typeof window.applyTranslations ===
                "function"
            ) {
                window.applyTranslations();
            }
        }
    );


    /* =====================================================
       DOM READY
    ====================================================== */

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialiseApp
        );
    } else {
        initialiseApp();
    }

})();