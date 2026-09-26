/* =========================================================
   UYIRTHULIR
   FARMER / FIELD WORKER FRONTEND
   Handles:
   - Farmer dashboard
   - Health report loading
   - Report submission
   - Animal data
   - Risk preview
   - Report history
   - Dashboard statistics
========================================================= */

(function () {
    "use strict";


    /* =====================================================
       STORAGE KEYS
    ====================================================== */

    const LATEST_REPORT_KEY = "latestReport";
    const REPORT_HISTORY_KEY = "reportHistory";
    const ANIMALS_KEY = "uyirthulir_animals";


    /* =====================================================
       GENERAL HELPERS
    ====================================================== */

    function getElement(...ids) {
        for (const id of ids) {
            const element =
                document.getElementById(id);

            if (element) {
                return element;
            }
        }

        return null;
    }


    function getInputValue(...ids) {
        const element =
            getElement(...ids);

        if (!element) {
            return "";
        }

        return element.value.trim();
    }


    function setText(element, value) {
        if (!element) {
            return;
        }

        element.textContent =
            value === null ||
            value === undefined
                ? ""
                : String(value);
    }


    function safeArray(value) {
        return Array.isArray(value)
            ? value
            : [];
    }


    function getTranslation(key, fallback) {
        if (
            typeof window.t ===
            "function"
        ) {
            const value =
                window.t(key);

            if (
                value &&
                value !== key
            ) {
                return value;
            }
        }

        return fallback || key;
    }


    /* =====================================================
       STORAGE
    ====================================================== */

    function saveLatestReport(report) {
        try {
            localStorage.setItem(
                LATEST_REPORT_KEY,
                JSON.stringify(report)
            );
        } catch (error) {
            console.error(
                "Unable to save latest report:",
                error
            );
        }
    }


    function getLatestReport() {
        const value =
            localStorage.getItem(
                LATEST_REPORT_KEY
            );

        if (!value) {
            return null;
        }

        try {
            return JSON.parse(value);
        } catch (error) {
            return null;
        }
    }


    function saveReportHistory(reports) {
        try {
            localStorage.setItem(
                REPORT_HISTORY_KEY,
                JSON.stringify(reports)
            );
        } catch (error) {
            console.error(
                "Unable to save report history:",
                error
            );
        }
    }


    function getReportHistory() {
        const value =
            localStorage.getItem(
                REPORT_HISTORY_KEY
            );

        if (!value) {
            return [];
        }

        try {
            return safeArray(
                JSON.parse(value)
            );
        } catch (error) {
            return [];
        }
    }


    function addToReportHistory(report) {
        const history =
            getReportHistory();

        history.unshift(report);

        saveReportHistory(
            history.slice(0, 100)
        );
    }


    /* =====================================================
       RISK CALCULATION
    ====================================================== */

    function calculateRisk(
        symptoms,
        severity
    ) {
        const symptomList =
            safeArray(symptoms);

        let score = 15;

        score +=
            symptomList.length * 8;


        const normalizedSeverity =
            String(
                severity || ""
            )
                .trim()
                .toUpperCase();


        if (
            normalizedSeverity ===
            "SEVERE"
        ) {
            score += 25;
        } else if (
            normalizedSeverity ===
            "MODERATE"
        ) {
            score += 12;
        }


        if (score > 100) {
            score = 100;
        }


        let level = "LOW";

        if (score >= 60) {
            level = "HIGH";
        } else if (score >= 30) {
            level = "MEDIUM";
        }


        return {
            score: score,
            level: level
        };
    }


    /* =====================================================
       RISK PREVIEW UI
    ====================================================== */

    function updateRiskPreview() {
        const symptomsInput =
            getElement(
                "symptoms",
                "symptomInput",
                "symptomDescription"
            );

        const severityInput =
            getElement(
                "severity"
            );


        let symptoms = [];


        if (symptomsInput) {
            const text =
                symptomsInput.value
                    .trim();

            if (text) {
                symptoms = text
                    .split(/[,;\n]+/)
                    .map(
                        function (item) {
                            return item.trim();
                        }
                    )
                    .filter(Boolean);
            }
        }


        const severity =
            severityInput
                ? severityInput.value
                : "";


        const risk =
            calculateRisk(
                symptoms,
                severity
            );


        const scoreElements =
            document.querySelectorAll(
                "[data-risk-score]"
            );


        scoreElements.forEach(
            function (element) {
                setText(
                    element,
                    risk.score
                );
            }
        );


        const levelElements =
            document.querySelectorAll(
                "[data-risk-level]"
            );


        levelElements.forEach(
            function (element) {
                setText(
                    element,
                    risk.level
                );

                element.classList.remove(
                    "status-high",
                    "status-medium",
                    "status-low"
                );


                if (
                    risk.level ===
                    "HIGH"
                ) {
                    element.classList.add(
                        "status-high"
                    );
                } else if (
                    risk.level ===
                    "MEDIUM"
                ) {
                    element.classList.add(
                        "status-medium"
                    );
                } else {
                    element.classList.add(
                        "status-low"
                    );
                }
            }
        );


        const previewBox =
            getElement(
                "riskPreview",
                "aiRiskPreview",
                "riskResult"
            );


        if (previewBox) {
            previewBox.style.display =
                "block";
        }


        return risk;
    }


    /* =====================================================
       SYMPTOM EXTRACTION
    ====================================================== */

    function getSymptomsFromForm() {
        const input =
            getElement(
                "symptoms",
                "symptomInput",
                "symptomDescription"
            );

        if (!input) {
            return [];
        }


        const text =
            input.value.trim();


        if (!text) {
            return [];
        }


        return text
            .split(/[,;\n]+/)
            .map(
                function (item) {
                    return item.trim();
                }
            )
            .filter(Boolean);
    }


    /* =====================================================
       UPLOAD FILE
    ====================================================== */

    async function uploadFile(
        file,
        endpoint
    ) {
        if (!file) {
            return null;
        }


        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        const response =
            await apiRequest(
                endpoint,
                {
                    method: "POST",
                    body: formData
                }
            );


        return response;
    }


    /* =====================================================
       UPLOAD PHOTO
    ====================================================== */

    async function uploadPhotoFromForm() {
        const input =
            getElement(
                "photo",
                "image",
                "photoInput",
                "imageInput"
            );


        if (
            !input ||
            !input.files ||
            input.files.length === 0
        ) {
            return null;
        }


        const file =
            input.files[0];


        return uploadFile(
            file,
            "/uploads/photo"
        );
    }


    /* =====================================================
       UPLOAD AUDIO
    ====================================================== */

    async function uploadAudioFromForm() {
        const input =
            getElement(
                "audio",
                "voice",
                "audioInput",
                "voiceInput"
            );


        if (
            !input ||
            !input.files ||
            input.files.length === 0
        ) {
            return null;
        }


        const file =
            input.files[0];


        return uploadFile(
            file,
            "/uploads/audio"
        );
    }


    /* =====================================================
       BUILD HEALTH REPORT
    ====================================================== */

    function buildHealthReportData(
        photoResponse,
        audioResponse
    ) {
        const animalName =
            getInputValue(
                "animalName",
                "animal_name"
            );


        const speciesElement =
            getElement(
                "species"
            );


        const severityElement =
            getElement(
                "severity"
            );


        const description =
            getInputValue(
                "description",
                "symptomDescription",
                "details"
            );


        const location =
            getInputValue(
                "location",
                "locationInput",
                "searchLocation"
            );


        const latitudeElement =
            getElement(
                "latitude",
                "lat"
            );


        const longitudeElement =
            getElement(
                "longitude",
                "lng",
                "lon"
            );


        const latitude =
            latitudeElement
                ? latitudeElement.value
                : "";


        const longitude =
            longitudeElement
                ? longitudeElement.value
                : "";


        const species =
            speciesElement
                ? speciesElement.value
                : "";


        const severity =
            severityElement
                ? severityElement.value
                : "";


        const symptoms =
            getSymptomsFromForm();


        const risk =
            calculateRisk(
                symptoms,
                severity
            );


        const photoName =
            photoResponse
                ? (
                    photoResponse.fileName ||
                    photoResponse.filename ||
                    ""
                )
                : "";


        const audioName =
            audioResponse
                ? (
                    audioResponse.fileName ||
                    audioResponse.filename ||
                    ""
                )
                : "";


        return {
            animalName:
                animalName,

            species:
                species,

            severity:
                severity,

            symptoms:
                JSON.stringify(
                    symptoms
                ),

            description:
                description,

            location:
                location,

            latitude:
                latitude
                    ? Number(latitude)
                    : null,

            longitude:
                longitude
                    ? Number(longitude)
                    : null,

            riskScore:
                risk.score,

            riskLevel:
                risk.level,

            photoName:
                photoName,

            audioName:
                audioName
        };
    }


    /* =====================================================
       SUBMIT HEALTH REPORT
    ====================================================== */

    async function submitHealthReport(
        event
    ) {
        if (event) {
            event.preventDefault();
        }


        const form =
            event
                ? event.currentTarget
                : getElement(
                    "healthReportForm",
                    "reportHealthForm",
                    "healthForm"
                );


        const submitButton =
            form
                ? form.querySelector(
                    'button[type="submit"]'
                )
                : null;


        const originalButtonText =
            submitButton
                ? submitButton.textContent
                : "";


        if (submitButton) {
            submitButton.disabled =
                true;

            submitButton.textContent =
                getTranslation(
                    "submitting",
                    "Submitting..."
                );
        }


        try {
            const photoResponse =
                await uploadPhotoFromForm();


            const audioResponse =
                await uploadAudioFromForm();


            const reportData =
                buildHealthReportData(
                    photoResponse,
                    audioResponse
                );


            if (
                !reportData.animalName
            ) {
                throw new Error(
                    "Animal name is required."
                );
            }


            if (
                !reportData.species
            ) {
                throw new Error(
                    "Species is required."
                );
            }


            if (
                !reportData.description &&
                reportData.symptoms === "[]"
            ) {
                throw new Error(
                    "Please provide symptoms or a description."
                );
            }


            const response =
                await apiRequest(
                    "/health-reports",
                    {
                        method: "POST",
                        body: JSON.stringify(
                            reportData
                        )
                    }
                );


            const report =
                response.report ||
                response.data ||
                {
                    ...reportData,
                    ...response
                };


            saveLatestReport(
                report
            );

            addToReportHistory(
                report
            );


            showToast(
                response.message ||
                getTranslation(
                    "reportSubmitted",
                    "Health report submitted successfully."
                ),
                "success"
            );


            updateLatestReportUI(
                report
            );


            if (form) {
                form.reset();
            }


            updateRiskPreview();


            return response;

        } catch (error) {
            console.error(
                "Health report submission error:",
                error
            );


            showToast(
                error.message ||
                getTranslation(
                    "unableToSubmit",
                    "Unable to submit."
                ),
                "error"
            );


            throw error;

        } finally {
            if (submitButton) {
                submitButton.disabled =
                    false;

                submitButton.textContent =
                    originalButtonText;
            }
        }
    }


    /* =====================================================
       LOAD MY REPORTS
    ====================================================== */

    async function loadMyReports() {
        try {
            const response =
                await apiRequest(
                    "/health-reports",
                    {
                        method: "GET"
                    }
                );


            const reports =
                safeArray(
                    response.reports ||
                    response.data ||
                    response
                );


            saveReportHistory(
                reports
            );


            renderReports(
                reports
            );


            updateDashboardStats(
                reports
            );


            return reports;

        } catch (error) {
            console.error(
                "Unable to load reports:",
                error
            );


            const storedReports =
                getReportHistory();


            if (
                storedReports.length > 0
            ) {
                renderReports(
                    storedReports
                );

                updateDashboardStats(
                    storedReports
                );
            }


            return storedReports;
        }
    }


    /* =====================================================
       RENDER REPORTS
    ====================================================== */

    function renderReports(
        reports
    ) {
        const containers =
            document.querySelectorAll(
                "[data-reports-container], #reportsContainer, #myReportsList"
            );


        containers.forEach(
            function (container) {
                container.innerHTML =
                    "";


                if (
                    !reports.length
                ) {
                    container.innerHTML =
                        `
                        <div class="empty-state">
                            <div class="empty-state-icon">📋</div>
                            <h3>${getTranslation(
                                "noData",
                                "No reports found."
                            )}</h3>
                            <p>
                                Submit your first animal health report
                                to begin surveillance.
                            </p>
                        </div>
                        `;

                    return;
                }


                reports.forEach(
                    function (report) {
                        container.appendChild(
                            createReportCard(
                                report
                            )
                        );
                    }
                );
            }
        );
    }


    /* =====================================================
       REPORT CARD
    ====================================================== */

    function createReportCard(
        report
    ) {
        const card =
            document.createElement(
                "div"
            );


        card.className =
            "dashboard-card report-card";


        const riskLevel =
            String(
                report.riskLevel ||
                report.risk_level ||
                report.severity ||
                "LOW"
            )
                .toUpperCase();


        let riskClass =
            "status-low";


        if (
            riskLevel === "HIGH"
        ) {
            riskClass =
                "status-high";
        } else if (
            riskLevel === "MEDIUM"
        ) {
            riskClass =
                "status-medium";
        }


        const animal =
            report.animalName ||
            report.animal_name ||
            "Unknown Animal";


        const species =
            report.species ||
            "Unknown";


        const location =
            report.location ||
            "Unknown Location";


        const status =
            report.status ||
            "PENDING";


        const createdAt =
            report.createdAt ||
            report.created_at ||
            "";


        card.innerHTML =
            `
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:12px;
            ">
                <div>
                    <h3>${escapeHtml(animal)}</h3>
                    <div class="dashboard-label">
                        ${escapeHtml(species)}
                    </div>
                </div>

                <span class="status-badge ${riskClass}">
                    ${escapeHtml(riskLevel)}
                </span>
            </div>

            <div style="margin-top:15px;">
                <div class="dashboard-label">
                    ${getTranslation(
                        "location",
                        "Location"
                    )}
                </div>

                <div>
                    ${escapeHtml(location)}
                </div>
            </div>

            <div style="margin-top:10px;">
                <div class="dashboard-label">
                    ${getTranslation(
                        "status",
                        "Status"
                    )}
                </div>

                <div>
                    ${escapeHtml(status)}
                </div>
            </div>

            <div style="margin-top:10px;">
                <div class="dashboard-label">
                    ${getTranslation(
                        "date",
                        "Date"
                    )}
                </div>

                <div>
                    ${escapeHtml(
                        formatDate(
                            createdAt
                        )
                    )}
                </div>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-top:18px;
                padding-top:12px;
                border-top:1px solid #e2e8f0;
            ">
                <span class="dashboard-label">
                    ${getTranslation(
                        "riskScore",
                        "Risk Score"
                    )}
                </span>

                <strong>
                    ${escapeHtml(
                        String(
                            report.riskScore ??
                            report.risk_score ??
                            "-"
                        )
                    )}
                </strong>
            </div>
            `;


        return card;
    }


    /* =====================================================
       DASHBOARD STATISTICS
    ====================================================== */

    function updateDashboardStats(
        reports
    ) {
        const list =
            safeArray(reports);


        let high = 0;
        let medium = 0;
        let low = 0;
        let validated = 0;
        let underInvestigation = 0;


        const animals =
            new Set();


        list.forEach(
            function (report) {
                const risk =
                    String(
                        report.riskLevel ||
                        report.risk_level ||
                        report.severity ||
                        "LOW"
                    )
                        .toUpperCase();


                if (
                    risk === "HIGH"
                ) {
                    high += 1;
                } else if (
                    risk === "MEDIUM"
                ) {
                    medium += 1;
                } else {
                    low += 1;
                }


                const animal =
                    report.animalName ||
                    report.animal_name;


                if (animal) {
                    animals.add(
                        String(animal)
                    );
                }


                const status =
                    String(
                        report.status ||
                        ""
                    )
                        .toUpperCase();


                if (
                    status === "VALIDATED"
                ) {
                    validated += 1;
                }


                if (
                    status ===
                    "UNDER INVESTIGATION"
                ) {
                    underInvestigation += 1;
                }
            }
        );


        setStatValue(
            [
                "monitoredAnimals",
                "animalCount"
            ],
            animals.size
        );


        setStatValue(
            [
                "totalReports",
                "reportCount"
            ],
            list.length
        );


        setStatValue(
            [
                "highRiskCases",
                "highRiskCount"
            ],
            high
        );


        setStatValue(
            [
                "mediumRiskCases",
                "mediumRiskCount"
            ],
            medium
        );


        setStatValue(
            [
                "lowRiskCases",
                "lowRiskCount"
            ],
            low
        );


        setStatValue(
            [
                "validatedCases",
                "validatedCount"
            ],
            validated
        );


        setStatValue(
            [
                "underInvestigation",
                "investigationCount"
            ],
            underInvestigation
        );
    }


    function setStatValue(
        ids,
        value
    ) {
        ids.forEach(
            function (id) {
                const element =
                    document.getElementById(
                        id
                    );

                if (element) {
                    setText(
                        element,
                        value
                    );
                }
            }
        );
    }


    /* =====================================================
       LATEST REPORT
    ====================================================== */

    function updateLatestReportUI(
        report
    ) {
        if (!report) {
            return;
        }


        document
            .querySelectorAll(
                "[data-latest-report]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        report.reportId ||
                        report.report_id ||
                        report.id ||
                        "";
                }
            );


        document
            .querySelectorAll(
                "[data-latest-risk]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        report.riskLevel ||
                        report.risk_level ||
                        "";
                }
            );


        document
            .querySelectorAll(
                "[data-latest-risk-score]"
            )
            .forEach(
                function (element) {
                    element.textContent =
                        report.riskScore ??
                        report.risk_score ??
                        "";
                }
            );
    }


    /* =====================================================
       ANIMALS
    ====================================================== */

    function getAnimals() {
        const stored =
            localStorage.getItem(
                ANIMALS_KEY
            );


        if (stored) {
            try {
                return safeArray(
                    JSON.parse(stored)
                );
            } catch (error) {
                return [];
            }
        }


        return [];
    }


    function saveAnimals(
        animals
    ) {
        try {
            localStorage.setItem(
                ANIMALS_KEY,
                JSON.stringify(
                    animals
                )
            );
        } catch (error) {
            console.error(
                "Unable to save animals:",
                error
            );
        }
    }


    function addAnimal(
        animal
    ) {
        const animals =
            getAnimals();


        animals.push(
            animal
        );


        saveAnimals(
            animals
        );


        return animal;
    }


    function renderAnimals() {
        const animals =
            getAnimals();


        const containers =
            document.querySelectorAll(
                "[data-animals-container], #animalsContainer, #animalList"
            );


        containers.forEach(
            function (container) {
                container.innerHTML =
                    "";


                if (
                    !animals.length
                ) {
                    container.innerHTML =
                        `
                        <div class="empty-state">
                            <div class="empty-state-icon">
                                🐄
                            </div>
                            <h3>
                                No animals added yet
                            </h3>
                            <p>
                                Your reported animals will appear here.
                            </p>
                        </div>
                        `;

                    return;
                }


                animals.forEach(
                    function (animal) {
                        const card =
                            document.createElement(
                                "div"
                            );


                        card.className =
                            "dashboard-card";


                        card.innerHTML =
                            `
                            <div style="font-size:32px;">
                                ${animal.icon || "🐄"}
                            </div>

                            <h3 style="margin-top:10px;">
                                ${escapeHtml(
                                    animal.name ||
                                    "Unnamed"
                                )}
                            </h3>

                            <div class="dashboard-label">
                                ${escapeHtml(
                                    animal.species ||
                                    "Unknown"
                                )}
                            </div>

                            ${
                                animal.tag
                                    ? `
                                    <div style="
                                        margin-top:10px;
                                        color:#64748b;
                                        font-size:11px;
                                    ">
                                        ID: ${escapeHtml(
                                            animal.tag
                                        )}
                                    </div>
                                    `
                                    : ""
                            }
                            `;


                        container.appendChild(
                            card
                        );
                    }
                );
            }
        );
    }


    /* =====================================================
       FORM EVENTS
    ====================================================== */

    function setupHealthReportForm() {
        const forms =
            document.querySelectorAll(
                "#healthReportForm, #reportHealthForm, #healthForm, form[data-form='health-report']"
            );


        forms.forEach(
            function (form) {
                if (
                    form.dataset.farmerBound ===
                    "true"
                ) {
                    return;
                }


                form.dataset.farmerBound =
                    "true";


                form.addEventListener(
                    "submit",
                    submitHealthReport
                );


                form.querySelectorAll(
                    "#symptoms, #symptomInput, #symptomDescription, #severity"
                ).forEach(
                    function (input) {
                        input.addEventListener(
                            "input",
                            updateRiskPreview
                        );

                        input.addEventListener(
                            "change",
                            updateRiskPreview
                        );
                    }
                );
            }
        );
    }


    /* =====================================================
       RISK BUTTON
    ====================================================== */

    function setupRiskButton() {
        const buttons =
            document.querySelectorAll(
                "#calculateRisk, [data-calculate-risk]"
            );


        buttons.forEach(
            function (button) {
                if (
                    button.dataset.riskBound ===
                    "true"
                ) {
                    return;
                }


                button.dataset.riskBound =
                    "true";


                button.addEventListener(
                    "click",
                    function (event) {
                        event.preventDefault();

                        updateRiskPreview();
                    }
                );
            }
        );
    }


    /* =====================================================
       DASHBOARD LOAD
    ====================================================== */

    async function initialiseFarmerDashboard() {
        const page =
            getCurrentPageNameSafe();


        if (
            page ===
            "farmer-dashboard.html" ||
            document.querySelector(
                "[data-farmer-dashboard]"
            )
        ) {
            await loadMyReports();
            renderAnimals();

            const latest =
                getLatestReport();

            updateLatestReportUI(
                latest
            );
        }


        if (
            page ===
            "animals.html" ||
            document.querySelector(
                "[data-animals-page]"
            )
        ) {
            renderAnimals();
        }


        if (
            page ===
            "report-health.html"
        ) {
            setupHealthReportForm();
            setupRiskButton();
            updateRiskPreview();
        }
    }


    /* =====================================================
       CURRENT PAGE
    ====================================================== */

    function getCurrentPageNameSafe() {
        const pathname =
            window.location.pathname;


        const parts =
            pathname
                .split("/")
                .filter(Boolean);


        return (
            parts[parts.length - 1] ||
            "index.html"
        );
    }


    /* =====================================================
       HTML ESCAPE
    ====================================================== */

    function escapeHtml(value) {
        return String(
            value === null ||
            value === undefined
                ? ""
                : value
        )
            .replaceAll(
                "&",
                "&amp;"
            )
            .replaceAll(
                "<",
                "&lt;"
            )
            .replaceAll(
                ">",
                "&gt;"
            )
            .replaceAll(
                '"',
                "&quot;"
            )
            .replaceAll(
                "'",
                "&#039;"
            );
    }


    /* =====================================================
       DATE FORMAT
    ====================================================== */

    function formatDate(
        value
    ) {
        if (!value) {
            return "-";
        }


        const date =
            new Date(value);


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {
            return String(value);
        }


        return date.toLocaleString();
    }


    /* =====================================================
       PUBLIC FUNCTIONS
    ====================================================== */

    window.calculateFarmerRisk =
        calculateRisk;

    window.updateRiskPreview =
        updateRiskPreview;

    window.submitHealthReport =
        submitHealthReport;

    window.loadMyReports =
        loadMyReports;

    window.renderReports =
        renderReports;

    window.renderAnimals =
        renderAnimals;

    window.getAnimals =
        getAnimals;

    window.addAnimal =
        addAnimal;

    window.getLatestReport =
        getLatestReport;

    window.getReportHistory =
        getReportHistory;


    /* =====================================================
       INITIALISATION
    ====================================================== */

    function initialise() {
        setupHealthReportForm();
        setupRiskButton();

        const latest =
            getLatestReport();

        updateLatestReportUI(
            latest
        );


        if (
            document.readyState !==
            "loading"
        ) {
            initialiseFarmerDashboard();
        }
    }


    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialiseFarmerDashboard
        );
    } else {
        initialise();
    }

})();