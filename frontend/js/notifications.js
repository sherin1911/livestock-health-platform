/* =========================================================
   UYIRTHULIR - NOTIFICATION SYSTEM
   ========================================================= */

(function () {
    "use strict";

    const API_BASE = "http://127.0.0.1:5000/api";

    function getToken() {
        return (
            localStorage.getItem("uyirthulir_token") ||
            localStorage.getItem("access_token") ||
            localStorage.getItem("token") ||
            ""
        );
    }

    function getUser() {
        try {
            return JSON.parse(
                localStorage.getItem("uyirthulir_user") ||
                localStorage.getItem("current_user") ||
                localStorage.getItem("user") ||
                "null"
            );
        } catch (error) {
            return null;
        }
    }

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    async function apiRequest(url, options = {}) {
        const token = getToken();

        const headers = {
            ...(options.headers || {})
        };

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        if (
            options.body &&
            !(options.body instanceof FormData) &&
            !headers["Content-Type"]
        ) {
            headers["Content-Type"] = "application/json";
        }

        const response = await fetch(url, {
            ...options,
            headers
        });

        let data = {};

        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (!response.ok) {
            throw new Error(
                data.message ||
                data.error ||
                `Request failed with status ${response.status}`
            );
        }

        return data;
    }

    function showToast(message, type = "info") {
        let container = document.getElementById(
            "uyirthulir-toast-container"
        );

        if (!container) {
            container = document.createElement("div");
            container.id = "uyirthulir-toast-container";

            container.style.position = "fixed";
            container.style.right = "20px";
            container.style.bottom = "20px";
            container.style.zIndex = "99999";
            container.style.display = "flex";
            container.style.flexDirection = "column";
            container.style.gap = "10px";

            document.body.appendChild(container);
        }

        const toast = document.createElement("div");

        toast.textContent = message;

        toast.style.padding = "14px 18px";
        toast.style.borderRadius = "10px";
        toast.style.background = "#ffffff";
        toast.style.color = "#1f2937";
        toast.style.boxShadow =
            "0 10px 30px rgba(0,0,0,0.15)";
        toast.style.border = "1px solid #e5e7eb";
        toast.style.minWidth = "260px";
        toast.style.fontSize = "14px";

        if (type === "success") {
            toast.style.borderLeft = "4px solid #16a34a";
        } else if (type === "error") {
            toast.style.borderLeft = "4px solid #dc2626";
        } else {
            toast.style.borderLeft = "4px solid #2563eb";
        }

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 4000);
    }

    function getNotificationContainer() {
        return (
            document.getElementById("notificationsList") ||
            document.getElementById("notificationList") ||
            document.querySelector(
                ".notifications-list"
            )
        );
    }

    function createBell() {
        const user = getUser();

        if (!user) {
            return;
        }

        const supportedRoles = [
            "VETERINARIAN",
            "DISTRICT_OFFICER",
            "STATE_ADMIN",
            "SUPER_ADMIN"
        ];

        const role = String(user.role || "").toUpperCase();

        if (!supportedRoles.includes(role)) {
            return;
        }

        if (
            document.getElementById(
                "uyirthulir-notification-bell"
            )
        ) {
            return;
        }

        const nav =
            document.querySelector(".navbar") ||
            document.querySelector("header");

        if (!nav) {
            return;
        }

        const bell = document.createElement("a");

        bell.id = "uyirthulir-notification-bell";
        bell.href = "../pages/alerts.html";
        bell.title = "Notifications";

        bell.style.position = "relative";
        bell.style.textDecoration = "none";
        bell.style.marginLeft = "10px";
        bell.style.fontSize = "20px";
        bell.style.display = "inline-flex";
        bell.style.alignItems = "center";
        bell.style.justifyContent = "center";
        bell.style.cursor = "pointer";

        bell.innerHTML = `
            <span>🔔</span>
            <span
                id="uyirthulir-notification-count"
                style="
                    display:none;
                    position:absolute;
                    top:-7px;
                    right:-8px;
                    min-width:18px;
                    height:18px;
                    padding:0 5px;
                    border-radius:20px;
                    background:#dc2626;
                    color:#ffffff;
                    font-size:11px;
                    font-weight:700;
                    line-height:18px;
                    text-align:center;
                "
            >0</span>
        `;

        nav.appendChild(bell);
    }

    async function loadUnreadCount() {
        const user = getUser();

        if (!user) {
            return;
        }

        const token = getToken();

        if (!token) {
            return;
        }

        try {
            const data = await apiRequest(
                `${API_BASE}/notifications/unread-count`
            );

            const count =
                Number(data.count) ||
                Number(data.unread_count) ||
                Number(data.data?.count) ||
                0;

            const badge = document.getElementById(
                "uyirthulir-notification-count"
            );

            if (!badge) {
                return;
            }

            if (count > 0) {
                badge.textContent =
                    count > 99 ? "99+" : String(count);

                badge.style.display = "block";
            } else {
                badge.textContent = "0";
                badge.style.display = "none";
            }
        } catch (error) {
            console.warn(
                "Notification count could not be loaded:",
                error.message
            );
        }
    }

    function notificationCard(notification) {
        const title = escapeHtml(
            notification.title || "Notification"
        );

        const message = escapeHtml(
            notification.message || ""
        );

        const priority = escapeHtml(
            notification.priority || "NORMAL"
        );

        const type = escapeHtml(
            notification.notification_type || ""
        );

        const createdAt =
            notification.created_at ||
            "";

        let dateText = "";

        if (createdAt) {
            const date = new Date(createdAt);

            if (!Number.isNaN(date.getTime())) {
                dateText = date.toLocaleString();
            }
        }

        const readClass =
            notification.is_read ? "read" : "unread";

        return `
            <div
                class="notification-card ${readClass}"
                data-notification-id="${notification.id}"
                style="
                    padding:18px;
                    margin-bottom:12px;
                    border:1px solid #e5e7eb;
                    border-radius:12px;
                    background:#ffffff;
                    box-shadow:0 4px 15px rgba(0,0,0,0.05);
                "
            >
                <div
                    style="
                        display:flex;
                        justify-content:space-between;
                        gap:12px;
                        align-items:flex-start;
                    "
                >
                    <div>
                        <h3
                            style="
                                margin:0 0 7px 0;
                                font-size:17px;
                            "
                        >
                            ${title}
                        </h3>

                        <p
                            style="
                                margin:0;
                                line-height:1.6;
                                color:#4b5563;
                            "
                        >
                            ${message}
                        </p>
                    </div>

                    <span
                        style="
                            padding:5px 9px;
                            border-radius:20px;
                            background:#eff6ff;
                            color:#1d4ed8;
                            font-size:11px;
                            font-weight:700;
                            white-space:nowrap;
                        "
                    >
                        ${priority}
                    </span>
                </div>

                <div
                    style="
                        display:flex;
                        justify-content:space-between;
                        gap:10px;
                        margin-top:12px;
                        flex-wrap:wrap;
                    "
                >
                    <small style="color:#6b7280;">
                        ${dateText}
                    </small>

                    <div style="display:flex;gap:8px;">
                        ${
                            type
                                ? `
                                    <span
                                        style="
                                            font-size:11px;
                                            color:#6b7280;
                                        "
                                    >
                                        ${type}
                                    </span>
                                  `
                                : ""
                        }

                        ${
                            !notification.is_read
                                ? `
                                    <button
                                        type="button"
                                        class="notification-read-btn"
                                        data-id="${notification.id}"
                                        style="
                                            border:0;
                                            padding:6px 10px;
                                            border-radius:7px;
                                            background:#2563eb;
                                            color:#ffffff;
                                            cursor:pointer;
                                            font-size:12px;
                                        "
                                    >
                                        Mark as read
                                    </button>
                                  `
                                : `
                                    <span
                                        style="
                                            font-size:12px;
                                            color:#16a34a;
                                            font-weight:600;
                                        "
                                    >
                                        Read
                                    </span>
                                  `
                        }
                    </div>
                </div>
            </div>
        `;
    }

    async function loadNotifications() {
        const container = getNotificationContainer();

        if (!container) {
            return;
        }

        const token = getToken();

        if (!token) {
            container.innerHTML = `
                <div
                    style="
                        padding:30px;
                        text-align:center;
                        color:#6b7280;
                    "
                >
                    Please login to view notifications.
                </div>
            `;

            return;
        }

        container.innerHTML = `
            <div
                style="
                    padding:30px;
                    text-align:center;
                    color:#6b7280;
                "
            >
                Loading notifications...
            </div>
        `;

        try {
            const data = await apiRequest(
                `${API_BASE}/notifications`
            );

            const notifications =
                Array.isArray(data)
                    ? data
                    : Array.isArray(data.notifications)
                        ? data.notifications
                        : Array.isArray(data.data)
                            ? data.data
                            : [];

            if (notifications.length === 0) {
                container.innerHTML = `
                    <div
                        style="
                            padding:40px;
                            text-align:center;
                            color:#6b7280;
                        "
                    >
                        <div
                            style="
                                font-size:42px;
                                margin-bottom:12px;
                            "
                        >
                            🔔
                        </div>

                        <h3
                            style="
                                margin:0 0 8px 0;
                                color:#374151;
                            "
                        >
                            No notifications
                        </h3>

                        <p style="margin:0;">
                            You are all caught up.
                        </p>
                    </div>
                `;

                return;
            }

            container.innerHTML =
                notifications
                    .map(notificationCard)
                    .join("");

            attachNotificationButtons();

        } catch (error) {
            console.error(
                "Notification loading error:",
                error
            );

            container.innerHTML = `
                <div
                    style="
                        padding:30px;
                        text-align:center;
                        color:#dc2626;
                    "
                >
                    Unable to load notifications.
                    <br>
                    <small>
                        ${escapeHtml(error.message)}
                    </small>
                </div>
            `;
        }
    }

    function attachNotificationButtons() {
        const buttons = document.querySelectorAll(
            ".notification-read-btn"
        );

        buttons.forEach((button) => {
            button.addEventListener(
                "click",
                async function () {
                    const id = this.dataset.id;

                    if (!id) {
                        return;
                    }

                    try {
                        await apiRequest(
                            `${API_BASE}/notifications/${id}/read`,
                            {
                                method: "PUT"
                            }
                        );

                        showToast(
                            "Notification marked as read.",
                            "success"
                        );

                        await loadNotifications();
                        await loadUnreadCount();

                    } catch (error) {
                        console.error(
                            "Mark read error:",
                            error
                        );

                        showToast(
                            "Could not mark notification as read.",
                            "error"
                        );
                    }
                }
            );
        });
    }

    async function markAllRead() {
        try {
            await apiRequest(
                `${API_BASE}/notifications/read-all`,
                {
                    method: "PUT"
                }
            );

            showToast(
                "All notifications marked as read.",
                "success"
            );

            await loadNotifications();
            await loadUnreadCount();

        } catch (error) {
            console.error(
                "Mark all read error:",
                error
            );

            showToast(
                "Could not mark all notifications as read.",
                "error"
            );
        }
    }

    function attachMarkAllButton() {
        const button =
            document.getElementById("markAllRead") ||
            document.getElementById("mark-all-read") ||
            document.querySelector(
                "[data-action='mark-all-read']"
            );

        if (!button) {
            return;
        }

        button.addEventListener(
            "click",
            function (event) {
                event.preventDefault();
                markAllRead();
            }
        );
    }

    async function initialiseNotifications() {
        createBell();
        attachMarkAllButton();

        await loadUnreadCount();
        await loadNotifications();

        setInterval(
            loadUnreadCount,
            15000
        );
    }

    window.UyirThulirNotifications = {
        load: loadNotifications,
        loadUnreadCount: loadUnreadCount,
        markAllRead: markAllRead
    };

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initialiseNotifications
        );
    } else {
        initialiseNotifications();
    }

})();