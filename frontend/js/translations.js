/* =========================================================
   UYIRTHULIR
   GLOBAL TRANSLATION SYSTEM
   Languages:
   English (en)
   Tamil (ta)
   Marathi (mr)
   Hindi (hi)
========================================================= */

(function () {
    "use strict";

    const translations = {
        en: {
            /* -------------------------------------------------
               COMMON
            ------------------------------------------------- */
            home: "Home",
            about: "About",
            features: "Features",
            workflow: "Workflow",
            login: "Login",
            register: "Register",
            logout: "Logout",
            save: "Save",
            submit: "Submit",
            cancel: "Cancel",
            close: "Close",
            back: "Back",
            next: "Next",
            search: "Search",
            filter: "Filter",
            refresh: "Refresh",
            loading: "Loading...",
            noData: "No data available.",
            success: "Success",
            error: "Error",
            warning: "Warning",
            information: "Information",
            view: "View",
            edit: "Edit",
            delete: "Delete",
            status: "Status",
            date: "Date",
            location: "Location",
            description: "Description",
            actions: "Actions",

            /* -------------------------------------------------
               BRAND
            ------------------------------------------------- */
            brandName: "UyirThulir",
            brandSubtitle: "Livestock Health Surveillance",

            /* -------------------------------------------------
               LANDING PAGE
            ------------------------------------------------- */
            heroBadge: "AI-Enabled Livestock Health Surveillance",
            heroTitle: "Early Warning for Livestock Health",
            heroDescription:
                "A digital surveillance platform that helps farmers, field workers, veterinarians, laboratories and government authorities identify health-risk signals early and coordinate timely response.",
            getStarted: "Get Started",
            signIn: "Sign In",
            heroNote:
                "AI-assisted risk assessment • Veterinary review • Laboratory validation • Government surveillance",

            surveillanceStatus: "Surveillance Status",
            earlyWarningActive: "Early Warning Active",
            monitoring: "Monitoring",
            riskSignal: "Risk Signal",
            veterinaryReview: "Veterinary Review",
            clusterIntelligence: "Cluster Intelligence",
            locationMonitoring: "Location Monitoring",

            aboutPlatform: "ABOUT THE PLATFORM",
            fromFieldToSurveillance:
                "From Field Reports to Coordinated Surveillance",
            aboutDescription:
                "UyirThulir connects the complete livestock health surveillance workflow in one platform.",

            digitalHealthReporting: "Digital Health Reporting",
            digitalHealthReportingText:
                "Farmers and field workers can submit animal health observations with symptoms, descriptions, location, photographs and audio evidence.",

            aiRiskAssessment: "AI-Assisted Risk Assessment",
            aiRiskAssessmentText:
                "Reported observations are transformed into an early-warning risk signal to support veterinary triage and prioritisation.",

            veterinaryInvestigation: "Veterinary Investigation",
            veterinaryInvestigationText:
                "Veterinarians can review cases, record field findings, collect samples and forward cases for laboratory validation.",

            governmentSurveillance: "Government Surveillance",
            governmentSurveillanceText:
                "Government authorities can monitor risk trends, emerging location signals, validated cases and surveillance activity.",

            coreCapabilities: "CORE CAPABILITIES",
            onePlatform:
                "One Platform, Complete Surveillance Workflow",

            healthReporting: "Health Reporting",
            healthReportingText:
                "Capture animal health observations directly from the field.",

            aiRiskSignal: "AI Risk Signal",
            aiRiskSignalText:
                "Convert reported symptoms and observations into an early-warning risk score.",

            smartNotifications: "Smart Notifications",
            smartNotificationsText:
                "Route relevant high and medium-risk signals to responsible users for action.",

            caseInvestigation: "Case Investigation",
            caseInvestigationText:
                "Veterinarians document examination findings, samples and preliminary assessments.",

            laboratoryValidation: "Laboratory Validation",
            laboratoryValidationText:
                "Record laboratory tests and validated results before surveillance classification.",

            gisSurveillance: "GIS Surveillance",
            gisSurveillanceText:
                "Visualise report locations and potential emerging clusters geographically.",

            surveillanceWorkflow: "SURVEILLANCE WORKFLOW",
            observeAssessInvestigateValidateRespond:
                "Observe → Assess → Investigate → Validate → Respond",

            fieldReport: "Field Report",
            fieldReportText:
                "Farmer or field worker records animal health observations.",

            riskAssessment: "Risk Assessment",
            riskAssessmentText:
                "AI-assisted analysis generates a risk signal for prioritisation.",

            veterinaryReview: "Veterinary Review",
            veterinaryReviewText:
                "A veterinarian investigates the reported case.",

            laboratoryValidationStep: "Laboratory Validation",
            laboratoryValidationTextStep:
                "Samples are tested and results are recorded for validation.",

            governmentSurveillanceStep: "Government Surveillance",
            governmentSurveillanceTextStep:
                "Validated information supports surveillance and prevention.",

            roleBasedAccess: "ROLE-BASED ACCESS",
            responseChain:
                "Designed for Every Level of the Response Chain",

            farmer: "Farmer",
            farmerText:
                "Report animal health observations and track submitted cases.",

            fieldWorker: "Field Worker",
            fieldWorkerText:
                "Submit field-level reports and support livestock surveillance.",

            veterinarian: "Veterinarian",
            veterinarianText:
                "Review risk signals and investigate suspected cases.",

            labStaff: "Laboratory Staff",
            labStaffText:
                "Manage testing, findings and validation results.",

            districtOfficer: "District Officer",
            districtOfficerText:
                "Monitor district-level alerts, clusters and surveillance activity.",

            stateAdministration: "State Administration",
            stateAdministrationText:
                "View statewide surveillance intelligence and emerging health signals.",

            responsibleAI: "Responsible AI & Surveillance",
            responsibleAIText:
                "The platform provides AI-assisted risk assessment and early-warning signals. It does not replace veterinary diagnosis, laboratory testing or epidemiological confirmation. Potential clusters require professional investigation and validation.",

            getStartedTitle:
                "Strengthening Livestock Health Surveillance Through Technology",
            getStartedText:
                "Connect field observations, veterinary expertise, laboratory validation and government surveillance in one platform.",

            createAccount: "Create Account",

            footerPlatform: "Platform",
            footerAccount: "Account",

            /* -------------------------------------------------
               AUTH
            ------------------------------------------------- */
            welcomeBack: "Welcome Back",
            loginSubtitle:
                "Sign in to continue to the Livestock Health Surveillance Platform.",
            createYourAccount: "Create Your Account",
            registerSubtitle:
                "Create your account to participate in livestock health surveillance.",

            name: "Name",
            email: "Email",
            username: "Username",
            password: "Password",
            confirmPassword: "Confirm Password",
            currentPassword: "Current Password",
            newPassword: "New Password",
            language: "Language",
            role: "Role",

            loginSuccessful: "Login successful.",
            registrationSuccessful: "Registration successful.",
            invalidCredentials:
                "Invalid username/email or password.",
            accountCreated:
                "Your account has been created successfully.",

            alreadyHaveAccount: "Already have an account?",
            dontHaveAccount: "Don't have an account?",
            passwordRequirements:
                "Password must contain at least 6 characters.",

            /* -------------------------------------------------
               FARMER DASHBOARD
            ------------------------------------------------- */
            farmerDashboard: "Farmer Dashboard",
            welcome: "Welcome",
            dashboardOverview: "Dashboard Overview",
            monitoredAnimals: "Monitored Animals",
            totalReports: "Total Reports",
            activeAlerts: "Active Alerts",
            highRiskCases: "High Risk Cases",
            mediumRiskCases: "Medium Risk Cases",
            lowRiskCases: "Low Risk Cases",
            validatedCases: "Validated Cases",
            underInvestigation: "Under Investigation",
            sentToLaboratory: "Sent to Laboratory",
            sentToSurveillance: "Sent to Surveillance",

            reportAnimalHealth: "Report Animal Health",
            myReports: "My Reports",
            myAnimals: "My Animals",
            alerts: "Alerts",
            profile: "Profile",

            /* -------------------------------------------------
               HEALTH REPORT
            ------------------------------------------------- */
            reportHealth: "Report Animal Health",
            animalName: "Animal Name",
            species: "Species",
            symptoms: "Symptoms",
            symptomDescription: "Symptom Description",
            severity: "Severity",
            mild: "Mild",
            moderate: "Moderate",
            severe: "Severe",

            describeSymptoms:
                "Describe the symptoms observed in the animal.",
            selectSpecies: "Select Species",
            cattle: "Cattle",
            buffalo: "Buffalo",
            goat: "Goat",
            sheep: "Sheep",
            poultry: "Poultry",
            pig: "Pig",
            other: "Other",

            searchLocation: "Search Location",
            currentLocation: "Use Current Location",
            latitude: "Latitude",
            longitude: "Longitude",

            uploadPhoto: "Upload Photo",
            uploadAudio: "Upload Audio",
            optional: "Optional",

            aiPreview: "AI Risk Preview",
            calculateRisk: "Calculate Risk",
            submitting: "Submitting...",
            reportSubmitted: "Health report submitted successfully.",
            riskScore: "Risk Score",
            riskLevel: "Risk Level",

            lowRisk: "Low Risk",
            mediumRisk: "Medium Risk",
            highRisk: "High Risk",

            /* -------------------------------------------------
               VETERINARY
            ------------------------------------------------- */
            veterinaryDashboard: "Veterinary Dashboard",
            caseQueue: "Case Queue",
            reviewCase: "Review Case",
            investigateCase: "Investigate Case",
            investigation: "Investigation",

            temperature: "Temperature",
            respiration: "Respiration",
            hydration: "Hydration",
            appetite: "Appetite",
            behaviour: "Behaviour",
            visibleSigns: "Visible Signs",

            sampleType: "Sample Type",
            collectionDate: "Collection Date",
            collectionNotes: "Collection Notes",
            preliminaryAssessment: "Preliminary Assessment",
            surveillanceFlag: "Surveillance Flag",

            newCase: "New",
            underInvestigationStatus: "Under Investigation",
            sentToLab: "Sent to Laboratory",
            validated: "Validated",
            rejected: "Rejected",

            saveInvestigation: "Save Investigation",
            sendToLab: "Send to Laboratory",
            investigationSaved:
                "Investigation details saved successfully.",

            /* -------------------------------------------------
               LABORATORY
            ------------------------------------------------- */
            laboratory: "Laboratory",
            laboratoryDashboard: "Laboratory Dashboard",
            sampleId: "Sample ID",
            testType: "Test Type",
            result: "Result",
            assayReference: "Assay Reference",
            findings: "Findings",
            surveillanceClassification:
                "Surveillance Classification",
            validationDate: "Validation Date",
            sentToSurveillanceText:
                "Sent to Surveillance",

            microscopicExamination: "Microscopic Examination",
            cultureIsolation: "Culture / Isolation",
            pcrMolecularTest: "PCR / Molecular Test",
            serologicalTest: "Serological Test",
            rapidDiagnosticTest: "Rapid Diagnostic Test",
            milkQualityAnalysis: "Milk Quality Analysis",

            negative: "Negative",
            positive: "Positive",
            inconclusive: "Inconclusive",

            saveValidation: "Save Validation",
            sendForSurveillance: "Send to Surveillance",
            laboratorySaved:
                "Laboratory result saved successfully.",

            /* -------------------------------------------------
               GOVERNMENT
            ------------------------------------------------- */
            governmentDashboard: "Government Dashboard",
            surveillanceDashboard: "Surveillance Dashboard",
            governmentOverview: "Government Overview",
            recentReports: "Recent Reports",
            districtSummary: "District Summary",
            riskDistribution: "Risk Distribution",
            clusterIntelligenceTitle: "Cluster Intelligence",
            gisMap: "GIS Surveillance Map",
            potentialEmergingClusters:
                "Potential Emerging Clusters",

            locationClusters: "Location Clusters",
            symptomClusters: "Symptom Clusters",
            clusterScore: "Cluster Score",
            priority: "Priority",
            signalReasons: "Signal Reasons",
            repeatedSymptoms: "Repeated Symptoms",
            speciesDistribution: "Species Distribution",
            reportCount: "Report Count",

            highPriority: "High Priority",
            moderatePriority: "Moderate Priority",
            watch: "Watch",

            potentialClusterNotice:
                "Potential cluster signals require veterinary, laboratory and epidemiological review before confirmation.",

            /* -------------------------------------------------
               NOTIFICATIONS
            ------------------------------------------------- */
            notifications: "Notifications",
            unreadNotifications: "Unread Notifications",
            markAsRead: "Mark as Read",
            markAllAsRead: "Mark All as Read",
            noNotifications: "No notifications.",
            notificationMarkedRead:
                "Notification marked as read.",
            allNotificationsRead:
                "All notifications marked as read.",

            /* -------------------------------------------------
               GIS
            ------------------------------------------------- */
            gisSurveillanceTitle: "GIS Surveillance",
            mapLegend: "Map Legend",
            allRisk: "All Risk Levels",
            clusterSignal: "Cluster Signal",
            reportLocation: "Report Location",
            mapLoading: "Loading surveillance map...",

            /* -------------------------------------------------
               MESSAGES
            ------------------------------------------------- */
            unableToLoad: "Unable to load data.",
            unableToSubmit: "Unable to submit.",
            sessionExpired:
                "Your session has expired. Please login again.",
            unauthorized:
                "You are not authorized to access this page.",
            somethingWentWrong:
                "Something went wrong. Please try again.",
            connectionError:
                "Unable to connect to the server.",

            /* -------------------------------------------------
               RESPONSIBLE AI
            ------------------------------------------------- */
            aiDisclaimer:
                "AI-generated risk signals are intended for early warning and triage. They do not constitute autonomous disease diagnosis.",
            veterinaryValidation:
                "Veterinary and laboratory validation is required before confirming a disease or outbreak.",
        },

        ta: {
            home: "முகப்பு",
            about: "பற்றி",
            features: "அம்சங்கள்",
            workflow: "செயல்முறை",
            login: "உள்நுழை",
            register: "பதிவு",
            logout: "வெளியேறு",
            save: "சேமி",
            submit: "சமர்ப்பி",
            cancel: "ரத்து செய்",
            close: "மூடு",
            back: "பின்",
            next: "அடுத்து",
            search: "தேடு",
            filter: "வடிகட்டு",
            refresh: "புதுப்பி",
            loading: "ஏற்றுகிறது...",
            noData: "தரவு இல்லை.",
            success: "வெற்றி",
            error: "பிழை",
            warning: "எச்சரிக்கை",
            information: "தகவல்",
            view: "பார்",
            edit: "திருத்து",
            delete: "நீக்கு",
            status: "நிலை",
            date: "தேதி",
            location: "இடம்",
            description: "விளக்கம்",
            actions: "செயல்கள்",

            brandName: "உயிர்துளிர்",
            brandSubtitle: "கால்நடை சுகாதார கண்காணிப்பு",

            heroBadge: "AI அடிப்படையிலான கால்நடை சுகாதார கண்காணிப்பு",
            heroTitle: "கால்நடை சுகாதாரத்திற்கான முன் எச்சரிக்கை",
            heroDescription:
                "விவசாயிகள், களப்பணியாளர்கள், கால்நடை மருத்துவர்கள், ஆய்வகங்கள் மற்றும் அரசு அதிகாரிகள் சுகாதார அபாய அறிகுறிகளை முன்கூட்டியே கண்டறிந்து ஒருங்கிணைந்த நடவடிக்கை எடுக்க உதவும் டிஜிட்டல் கண்காணிப்பு தளம்.",
            getStarted: "தொடங்குங்கள்",
            signIn: "உள்நுழைக",
            heroNote:
                "AI உதவியுடன் அபாய மதிப்பீடு • கால்நடை மருத்துவர் ஆய்வு • ஆய்வக சரிபார்ப்பு • அரசு கண்காணிப்பு",

            surveillanceStatus: "கண்காணிப்பு நிலை",
            earlyWarningActive: "முன் எச்சரிக்கை செயல்பாட்டில்",
            monitoring: "கண்காணிப்பு",
            riskSignal: "அபாய அறிகுறி",
            veterinaryReview: "கால்நடை மருத்துவர் ஆய்வு",
            clusterIntelligence: "குழு நுண்ணறிவு",
            locationMonitoring: "இட கண்காணிப்பு",

            aboutPlatform: "தளத்தைப் பற்றி",
            fromFieldToSurveillance:
                "கள அறிக்கைகளிலிருந்து ஒருங்கிணைந்த கண்காணிப்பிற்கு",
            aboutDescription:
                "உயிர்துளிர் கால்நடை சுகாதார கண்காணிப்பு பணிச்சுற்றை ஒரே தளத்தில் இணைக்கிறது.",

            digitalHealthReporting: "டிஜிட்டல் சுகாதார அறிக்கை",
            digitalHealthReportingText:
                "விவசாயிகள் மற்றும் களப்பணியாளர்கள் அறிகுறிகள், விளக்கம், இடம், புகைப்படம் மற்றும் ஆடியோ ஆதாரங்களுடன் கால்நடை சுகாதார தகவல்களை சமர்ப்பிக்கலாம்.",

            aiRiskAssessment: "AI உதவியுடன் அபாய மதிப்பீடு",
            aiRiskAssessmentText:
                "சமர்ப்பிக்கப்பட்ட தகவல்கள் கால்நடை மருத்துவ முன்னுரிமைக்காக முன் எச்சரிக்கை அபாய அறிகுறியாக மாற்றப்படுகின்றன.",

            veterinaryInvestigation: "கால்நடை மருத்துவ ஆய்வு",
            veterinaryInvestigationText:
                "கால்நடை மருத்துவர்கள் வழக்குகளை ஆய்வு செய்து கள தகவல்களை பதிவு செய்து மாதிரிகளை சேகரித்து ஆய்வகத்திற்கு அனுப்பலாம்.",

            governmentSurveillance: "அரசு கண்காணிப்பு",
            governmentSurveillanceText:
                "அரசு அதிகாரிகள் அபாய போக்குகள், இட அடிப்படையிலான அறிகுறிகள், சரிபார்க்கப்பட்ட வழக்குகள் மற்றும் கண்காணிப்பு செயல்பாடுகளை கண்காணிக்கலாம்.",

            coreCapabilities: "முக்கிய திறன்கள்",
            onePlatform:
                "ஒரே தளத்தில் முழுமையான கண்காணிப்பு செயல்முறை",

            healthReporting: "சுகாதார அறிக்கை",
            healthReportingText:
                "களத்திலிருந்து கால்நடை சுகாதார தகவல்களை பதிவு செய்யுங்கள்.",

            aiRiskSignal: "AI அபாய அறிகுறி",
            aiRiskSignalText:
                "அறிகுறிகள் மற்றும் தகவல்களை முன் எச்சரிக்கை அபாய மதிப்பெண்ணாக மாற்றுகிறது.",

            smartNotifications: "ஸ்மார்ட் அறிவிப்புகள்",
            smartNotificationsText:
                "முக்கியமான அபாய அறிகுறிகளை பொறுப்பான அதிகாரிகளுக்கு அனுப்புகிறது.",

            caseInvestigation: "வழக்கு ஆய்வு",
            caseInvestigationText:
                "கால்நடை மருத்துவர்கள் பரிசோதனை தகவல்கள், மாதிரிகள் மற்றும் ஆரம்ப மதிப்பீடுகளை பதிவு செய்கிறார்கள்.",

            laboratoryValidation: "ஆய்வக சரிபார்ப்பு",
            laboratoryValidationText:
                "கண்காணிப்பு வகைப்படுத்தலுக்கு முன் ஆய்வக சோதனை முடிவுகளை பதிவு செய்கிறது.",

            gisSurveillance: "GIS கண்காணிப்பு",
            gisSurveillanceText:
                "அறிக்கைகளின் இடங்கள் மற்றும் சாத்தியமான குழுக்களை வரைபடத்தில் காண்பிக்கிறது.",

            surveillanceWorkflow: "கண்காணிப்பு செயல்முறை",
            observeAssessInvestigateValidateRespond:
                "கவனி → மதிப்பிடு → ஆய்வு செய் → சரிபார் → நடவடிக்கை எடு",

            fieldReport: "கள அறிக்கை",
            fieldReportText:
                "விவசாயி அல்லது களப்பணியாளர் கால்நடை சுகாதார தகவலை பதிவு செய்கிறார்.",

            riskAssessment: "அபாய மதிப்பீடு",
            riskAssessmentText:
                "AI உதவியுடன் பகுப்பாய்வு செய்து முன்னுரிமைக்கான அபாய அறிகுறியை உருவாக்குகிறது.",

            veterinaryReview: "கால்நடை மருத்துவர் ஆய்வு",
            veterinaryReviewText:
                "கால்நடை மருத்துவர் சமர்ப்பிக்கப்பட்ட வழக்கை ஆய்வு செய்கிறார்.",

            laboratoryValidationStep: "ஆய்வக சரிபார்ப்பு",
            laboratoryValidationTextStep:
                "மாதிரிகள் பரிசோதிக்கப்பட்டு முடிவுகள் பதிவு செய்யப்படுகின்றன.",

            governmentSurveillanceStep: "அரசு கண்காணிப்பு",
            governmentSurveillanceTextStep:
                "சரிபார்க்கப்பட்ட தகவல் கண்காணிப்பு மற்றும் தடுப்பு நடவடிக்கைகளுக்கு உதவுகிறது.",

            roleBasedAccess: "பாத்திர அடிப்படையிலான அணுகல்",
            responseChain:
                "முழுமையான நடவடிக்கை சங்கிலிக்காக வடிவமைக்கப்பட்டது",

            farmer: "விவசாயி",
            farmerText:
                "கால்நடை சுகாதார தகவல்களை பதிவு செய்து சமர்ப்பிக்கப்பட்ட வழக்குகளை கண்காணிக்கவும்.",

            fieldWorker: "களப்பணியாளர்",
            fieldWorkerText:
                "கள அறிக்கைகளை சமர்ப்பித்து கால்நடை கண்காணிப்புக்கு உதவுங்கள்.",

            veterinarian: "கால்நடை மருத்துவர்",
            veterinarianText:
                "அபாய அறிகுறிகளை ஆய்வு செய்து சந்தேகத்திற்குரிய வழக்குகளை விசாரிக்கவும்.",

            labStaff: "ஆய்வக பணியாளர்",
            labStaffText:
                "சோதனைகள், கண்டறிதல்கள் மற்றும் சரிபார்ப்பு முடிவுகளை நிர்வகிக்கவும்.",

            districtOfficer: "மாவட்ட அலுவலர்",
            districtOfficerText:
                "மாவட்ட அளவிலான எச்சரிக்கைகள், குழுக்கள் மற்றும் கண்காணிப்பை கண்காணிக்கவும்.",

            stateAdministration: "மாநில நிர்வாகம்",
            stateAdministrationText:
                "மாநில அளவிலான கண்காணிப்பு நுண்ணறிவு மற்றும் உருவாகும் சுகாதார அறிகுறிகளை பார்க்கவும்.",

            responsibleAI: "பொறுப்பான AI மற்றும் கண்காணிப்பு",
            responsibleAIText:
                "இந்த தளம் AI உதவியுடன் அபாய மதிப்பீடு மற்றும் முன் எச்சரிக்கை அறிகுறிகளை வழங்குகிறது. இது கால்நடை மருத்துவர் நோயறிதல், ஆய்வக சோதனை அல்லது தொற்றுநோயியல் உறுதிப்படுத்தலை மாற்றாது. சாத்தியமான குழுக்களுக்கு தொழில்முறை ஆய்வு மற்றும் சரிபார்ப்பு அவசியம்.",

            getStartedTitle:
                "தொழில்நுட்பத்தின் மூலம் கால்நடை சுகாதார கண்காணிப்பை வலுப்படுத்துதல்",
            getStartedText:
                "கள தகவல்கள், கால்நடை நிபுணத்துவம், ஆய்வக சரிபார்ப்பு மற்றும் அரசு கண்காணிப்பை ஒரே தளத்தில் இணைக்கவும்.",

            createAccount: "கணக்கை உருவாக்கு",

            footerPlatform: "தளம்",
            footerAccount: "கணக்கு",

            welcomeBack: "மீண்டும் வரவேற்கிறோம்",
            loginSubtitle:
                "கால்நடை சுகாதார கண்காணிப்பு தளத்தை தொடர உள்நுழையுங்கள்.",
            createYourAccount: "உங்கள் கணக்கை உருவாக்குங்கள்",
            registerSubtitle:
                "கால்நடை சுகாதார கண்காணிப்பில் பங்கேற்க உங்கள் கணக்கை உருவாக்குங்கள்.",

            name: "பெயர்",
            email: "மின்னஞ்சல்",
            username: "பயனர் பெயர்",
            password: "கடவுச்சொல்",
            confirmPassword: "கடவுச்சொல்லை உறுதிப்படுத்து",
            currentPassword: "தற்போதைய கடவுச்சொல்",
            newPassword: "புதிய கடவுச்சொல்",
            language: "மொழி",
            role: "பாத்திரம்",

            loginSuccessful: "உள்நுழைவு வெற்றிகரமாக முடிந்தது.",
            registrationSuccessful: "பதிவு வெற்றிகரமாக முடிந்தது.",
            invalidCredentials:
                "பயனர் பெயர்/மின்னஞ்சல் அல்லது கடவுச்சொல் தவறாக உள்ளது.",
            accountCreated:
                "உங்கள் கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது.",
            alreadyHaveAccount: "ஏற்கனவே கணக்கு உள்ளதா?",
            dontHaveAccount: "கணக்கு இல்லையா?",
            passwordRequirements:
                "கடவுச்சொல்லில் குறைந்தது 6 எழுத்துகள் இருக்க வேண்டும்.",

            farmerDashboard: "விவசாயி டாஷ்போர்டு",
            welcome: "வரவேற்பு",
            dashboardOverview: "டாஷ்போர்டு சுருக்கம்",
            monitoredAnimals: "கண்காணிக்கப்படும் கால்நடைகள்",
            totalReports: "மொத்த அறிக்கைகள்",
            activeAlerts: "செயலில் உள்ள எச்சரிக்கைகள்",
            highRiskCases: "அதிக அபாய வழக்குகள்",
            mediumRiskCases: "நடுத்தர அபாய வழக்குகள்",
            lowRiskCases: "குறைந்த அபாய வழக்குகள்",
            validatedCases: "சரிபார்க்கப்பட்ட வழக்குகள்",
            underInvestigation: "ஆய்வில் உள்ளவை",
            sentToLaboratory: "ஆய்வகத்திற்கு அனுப்பப்பட்டவை",
            sentToSurveillance: "கண்காணிப்பிற்கு அனுப்பப்பட்டவை",

            reportAnimalHealth: "கால்நடை சுகாதார அறிக்கை",
            myReports: "என் அறிக்கைகள்",
            myAnimals: "என் கால்நடைகள்",
            alerts: "எச்சரிக்கைகள்",
            profile: "சுயவிவரம்",

            reportHealth: "கால்நடை சுகாதார அறிக்கை",
            animalName: "கால்நடை பெயர்",
            species: "வகை",
            symptoms: "அறிகுறிகள்",
            symptomDescription: "அறிகுறி விளக்கம்",
            severity: "தீவிரம்",
            mild: "லேசான",
            moderate: "மிதமான",
            severe: "கடுமையான",

            describeSymptoms:
                "கால்நடையில் காணப்படும் அறிகுறிகளை விவரிக்கவும்.",
            selectSpecies: "கால்நடை வகையைத் தேர்ந்தெடுக்கவும்",
            cattle: "மாடு",
            buffalo: "எருமை",
            goat: "ஆடு",
            sheep: "செம்மறியாடு",
            poultry: "கோழி",
            pig: "பன்றி",
            other: "மற்றவை",

            searchLocation: "இடத்தைத் தேடு",
            currentLocation: "தற்போதைய இடத்தைப் பயன்படுத்து",
            latitude: "அட்சரேகை",
            longitude: "தீர்க்கரேகை",

            uploadPhoto: "புகைப்படத்தை பதிவேற்று",
            uploadAudio: "ஆடியோவை பதிவேற்று",
            optional: "விருப்பம்",

            aiPreview: "AI அபாய முன்னோட்டம்",
            calculateRisk: "அபாயத்தை கணக்கிடு",
            submitting: "சமர்ப்பிக்கிறது...",
            reportSubmitted:
                "சுகாதார அறிக்கை வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது.",
            riskScore: "அபாய மதிப்பெண்",
            riskLevel: "அபாய நிலை",

            lowRisk: "குறைந்த அபாயம்",
            mediumRisk: "நடுத்தர அபாயம்",
            highRisk: "அதிக அபாயம்",

            veterinaryDashboard: "கால்நடை மருத்துவ டாஷ்போர்டு",
            caseQueue: "வழக்கு வரிசை",
            reviewCase: "வழக்கை ஆய்வு செய்",
            investigateCase: "வழக்கை விசாரி",
            investigation: "ஆய்வு",

            temperature: "உடல் வெப்பநிலை",
            respiration: "சுவாசம்",
            hydration: "நீர்ச்சத்து",
            appetite: "பசியுணர்வு",
            behaviour: "நடத்தை",
            visibleSigns: "காணக்கூடிய அறிகுறிகள்",

            sampleType: "மாதிரி வகை",
            collectionDate: "சேகரிப்பு தேதி",
            collectionNotes: "சேகரிப்பு குறிப்புகள்",
            preliminaryAssessment: "ஆரம்ப மதிப்பீடு",
            surveillanceFlag: "கண்காணிப்பு குறியீடு",

            newCase: "புதியது",
            underInvestigationStatus: "ஆய்வில்",
            sentToLab: "ஆய்வகத்திற்கு அனுப்பப்பட்டது",
            validated: "சரிபார்க்கப்பட்டது",
            rejected: "நிராகரிக்கப்பட்டது",

            saveInvestigation: "ஆய்வை சேமி",
            sendToLab: "ஆய்வகத்திற்கு அனுப்பு",
            investigationSaved:
                "ஆய்வு தகவல்கள் வெற்றிகரமாக சேமிக்கப்பட்டன.",

            laboratory: "ஆய்வகம்",
            laboratoryDashboard: "ஆய்வக டாஷ்போர்டு",
            sampleId: "மாதிரி ID",
            testType: "சோதனை வகை",
            result: "முடிவு",
            assayReference: "Assay குறிப்பு",
            findings: "கண்டறிதல்கள்",
            surveillanceClassification:
                "கண்காணிப்பு வகைப்பாடு",
            validationDate: "சரிபார்ப்பு தேதி",
            sentToSurveillanceText:
                "கண்காணிப்பிற்கு அனுப்பப்பட்டது",

            microscopicExamination: "நுண்ணோக்கி பரிசோதனை",
            cultureIsolation: "கல்ச்சர் / தனிமைப்படுத்தல்",
            pcrMolecularTest: "PCR / மூலக்கூறு சோதனை",
            serologicalTest: "சீராலஜிக்கல் சோதனை",
            rapidDiagnosticTest: "விரைவு கண்டறிதல் சோதனை",
            milkQualityAnalysis: "பால் தர பகுப்பாய்வு",

            negative: "எதிர்மறை",
            positive: "நேர்மறை",
            inconclusive: "தெளிவற்றது",

            saveValidation: "சரிபார்ப்பை சேமி",
            sendForSurveillance: "கண்காணிப்பிற்கு அனுப்பு",
            laboratorySaved:
                "ஆய்வக முடிவு வெற்றிகரமாக சேமிக்கப்பட்டது.",

            governmentDashboard: "அரசு டாஷ்போர்டு",
            surveillanceDashboard: "கண்காணிப்பு டாஷ்போர்டு",
            governmentOverview: "அரசு சுருக்கம்",
            recentReports: "சமீபத்திய அறிக்கைகள்",
            districtSummary: "மாவட்ட சுருக்கம்",
            riskDistribution: "அபாய விநியோகம்",
            clusterIntelligenceTitle: "குழு நுண்ணறிவு",
            gisMap: "GIS கண்காணிப்பு வரைபடம்",
            potentialEmergingClusters:
                "சாத்தியமான உருவாகும் குழுக்கள்",

            locationClusters: "இட குழுக்கள்",
            symptomClusters: "அறிகுறி குழுக்கள்",
            clusterScore: "குழு மதிப்பெண்",
            priority: "முன்னுரிமை",
            signalReasons: "அறிகுறி காரணங்கள்",
            repeatedSymptoms: "மீண்டும் காணப்படும் அறிகுறிகள்",
            speciesDistribution: "கால்நடை வகை விநியோகம்",
            reportCount: "அறிக்கை எண்ணிக்கை",

            highPriority: "அதிக முன்னுரிமை",
            moderatePriority: "மிதமான முன்னுரிமை",
            watch: "கண்காணிப்பு",

            potentialClusterNotice:
                "சாத்தியமான குழு அறிகுறிகள் உறுதிப்படுத்துவதற்கு முன் கால்நடை, ஆய்வக மற்றும் தொற்றுநோயியல் ஆய்வுக்கு உட்படுத்தப்பட வேண்டும்.",

            notifications: "அறிவிப்புகள்",
            unreadNotifications: "படிக்காத அறிவிப்புகள்",
            markAsRead: "படித்ததாக குறி",
            markAllAsRead: "அனைத்தையும் படித்ததாக குறி",
            noNotifications: "அறிவிப்புகள் இல்லை.",
            notificationMarkedRead:
                "அறிவிப்பு படித்ததாக குறிக்கப்பட்டது.",
            allNotificationsRead:
                "அனைத்து அறிவிப்புகளும் படித்ததாக குறிக்கப்பட்டன.",

            gisSurveillanceTitle: "GIS கண்காணிப்பு",
            mapLegend: "வரைபட குறியீடு",
            allRisk: "அனைத்து அபாய நிலைகள்",
            clusterSignal: "குழு அறிகுறி",
            reportLocation: "அறிக்கை இடம்",
            mapLoading: "கண்காணிப்பு வரைபடம் ஏற்றப்படுகிறது...",

            unableToLoad: "தரவை ஏற்ற முடியவில்லை.",
            unableToSubmit: "சமர்ப்பிக்க முடியவில்லை.",
            sessionExpired:
                "உங்கள் அமர்வு முடிந்துவிட்டது. மீண்டும் உள்நுழையவும்.",
            unauthorized:
                "இந்தப் பக்கத்தை அணுக உங்களுக்கு அனுமதி இல்லை.",
            somethingWentWrong:
                "ஏதோ தவறு ஏற்பட்டுள்ளது. மீண்டும் முயற்சிக்கவும்.",
            connectionError:
                "சேவையகத்துடன் இணைக்க முடியவில்லை.",

            aiDisclaimer:
                "AI உருவாக்கும் அபாய அறிகுறிகள் முன் எச்சரிக்கை மற்றும் முன்னுரிமைக்காக மட்டுமே. அவை தன்னாட்சி நோய் கண்டறிதலை குறிக்காது.",
            veterinaryValidation:
                "நோய் அல்லது தொற்றை உறுதிப்படுத்த கால்நடை மருத்துவர் மற்றும் ஆய்வக சரிபார்ப்பு அவசியம்.",
        },

        mr: {
            home: "मुख्यपृष्ठ",
            about: "माहिती",
            features: "वैशिष्ट्ये",
            workflow: "कार्यप्रवाह",
            login: "लॉगिन",
            register: "नोंदणी",
            logout: "लॉगआउट",
            save: "जतन करा",
            submit: "सबमिट करा",
            cancel: "रद्द करा",
            close: "बंद करा",
            back: "मागे",
            next: "पुढे",
            search: "शोधा",
            filter: "फिल्टर",
            refresh: "रिफ्रेश",
            loading: "लोड होत आहे...",
            noData: "डेटा उपलब्ध नाही.",
            success: "यशस्वी",
            error: "त्रुटी",
            warning: "इशारा",
            information: "माहिती",
            view: "पहा",
            edit: "संपादित करा",
            delete: "हटवा",
            status: "स्थिती",
            date: "तारीख",
            location: "स्थान",
            description: "वर्णन",
            actions: "कृती",

            brandName: "UyirThulir",
            brandSubtitle: "पशुधन आरोग्य देखरेख",

            heroBadge: "AI-सक्षम पशुधन आरोग्य देखरेख",
            heroTitle: "पशुधन आरोग्यासाठी पूर्व इशारा",
            heroDescription:
                "शेतकरी, क्षेत्रीय कर्मचारी, पशुवैद्यकीय डॉक्टर, प्रयोगशाळा आणि सरकारी अधिकाऱ्यांना आरोग्य जोखमीचे संकेत लवकर ओळखण्यासाठी आणि योग्य प्रतिसादासाठी मदत करणारे डिजिटल देखरेख व्यासपीठ.",
            getStarted: "सुरू करा",
            signIn: "साइन इन",
            heroNote:
                "AI-सहाय्यित जोखीम मूल्यांकन • पशुवैद्यकीय तपासणी • प्रयोगशाळा पडताळणी • सरकारी देखरेख",

            surveillanceStatus: "देखरेख स्थिती",
            earlyWarningActive: "पूर्व इशारा सक्रिय",
            monitoring: "देखरेख",
            riskSignal: "जोखीम संकेत",
            veterinaryReview: "पशुवैद्यकीय तपासणी",
            clusterIntelligence: "क्लस्टर बुद्धिमत्ता",
            locationMonitoring: "स्थान देखरेख",

            aboutPlatform: "व्यासपीठाबद्दल",
            fromFieldToSurveillance:
                "क्षेत्रीय अहवालांपासून समन्वित देखरेखीपर्यंत",
            aboutDescription:
                "UyirThulir संपूर्ण पशुधन आरोग्य देखरेख कार्यप्रवाह एका व्यासपीठावर जोडते.",

            digitalHealthReporting: "डिजिटल आरोग्य अहवाल",
            digitalHealthReportingText:
                "शेतकरी आणि क्षेत्रीय कर्मचारी लक्षणे, वर्णन, स्थान, छायाचित्रे आणि ऑडिओ पुराव्यासह पशुधन आरोग्य निरीक्षणे नोंदवू शकतात.",

            aiRiskAssessment: "AI-सहाय्यित जोखीम मूल्यांकन",
            aiRiskAssessmentText:
                "नोंदवलेली निरीक्षणे पशुवैद्यकीय प्राधान्यक्रमासाठी पूर्व-इशारा जोखीम संकेतामध्ये रूपांतरित केली जातात.",

            veterinaryInvestigation: "पशुवैद्यकीय तपासणी",
            veterinaryInvestigationText:
                "पशुवैद्यकीय डॉक्टर प्रकरणांचे पुनरावलोकन करून तपासणी निष्कर्ष, नमुने आणि प्राथमिक मूल्यांकन नोंदवू शकतात.",

            governmentSurveillance: "सरकारी देखरेख",
            governmentSurveillanceText:
                "सरकारी अधिकारी जोखीम ट्रेंड, स्थानिक संकेत, पडताळलेली प्रकरणे आणि देखरेख क्रियाकलाप पाहू शकतात.",

            coreCapabilities: "मुख्य क्षमता",
            onePlatform:
                "एका व्यासपीठावर संपूर्ण देखरेख कार्यप्रवाह",

            healthReporting: "आरोग्य अहवाल",
            healthReportingText:
                "क्षेत्रातून पशुधन आरोग्य निरीक्षणे नोंदवा.",

            aiRiskSignal: "AI जोखीम संकेत",
            aiRiskSignalText:
                "लक्षणे आणि निरीक्षणे पूर्व-इशारा जोखीम गुणामध्ये रूपांतरित करा.",

            smartNotifications: "स्मार्ट सूचना",
            smartNotificationsText:
                "महत्त्वाचे जोखीम संकेत संबंधित वापरकर्त्यांपर्यंत पोहोचवा.",

            caseInvestigation: "प्रकरण तपासणी",
            caseInvestigationText:
                "पशुवैद्यकीय डॉक्टर तपासणी निष्कर्ष आणि नमुने नोंदवतात.",

            laboratoryValidation: "प्रयोगशाळा पडताळणी",
            laboratoryValidationText:
                "देखरेख वर्गीकरणापूर्वी प्रयोगशाळा चाचणी आणि पडताळणी परिणाम नोंदवा.",

            gisSurveillance: "GIS देखरेख",
            gisSurveillanceText:
                "अहवाल स्थाने आणि संभाव्य उदयोन्मुख क्लस्टर्स नकाशावर पहा.",

            surveillanceWorkflow: "देखरेख कार्यप्रवाह",
            observeAssessInvestigateValidateRespond:
                "निरीक्षण → मूल्यांकन → तपासणी → पडताळणी → प्रतिसाद",

            fieldReport: "क्षेत्रीय अहवाल",
            fieldReportText:
                "शेतकरी किंवा क्षेत्रीय कर्मचारी पशुधन आरोग्य निरीक्षण नोंदवतो.",

            riskAssessment: "जोखीम मूल्यांकन",
            riskAssessmentText:
                "AI-सहाय्यित विश्लेषण प्राधान्यक्रमासाठी जोखीम संकेत तयार करते.",

            veterinaryReview: "पशुवैद्यकीय पुनरावलोकन",
            veterinaryReviewText:
                "पशुवैद्यकीय डॉक्टर नोंदवलेल्या प्रकरणाची तपासणी करतात.",

            laboratoryValidationStep: "प्रयोगशाळा पडताळणी",
            laboratoryValidationTextStep:
                "नमुने तपासले जातात आणि परिणाम नोंदवले जातात.",

            governmentSurveillanceStep: "सरकारी देखरेख",
            governmentSurveillanceTextStep:
                "पडताळलेली माहिती देखरेख आणि प्रतिबंधात्मक उपायांना मदत करते.",

            roleBasedAccess: "भूमिकेनुसार प्रवेश",
            responseChain:
                "प्रतिसाद साखळीतील प्रत्येक स्तरासाठी डिझाइन केलेले",

            farmer: "शेतकरी",
            farmerText:
                "पशुधन आरोग्य निरीक्षण नोंदवा आणि सादर केलेली प्रकरणे ट्रॅक करा.",

            fieldWorker: "क्षेत्रीय कर्मचारी",
            fieldWorkerText:
                "क्षेत्रीय अहवाल सादर करून पशुधन देखरेखीला मदत करा.",

            veterinarian: "पशुवैद्यकीय डॉक्टर",
            veterinarianText:
                "जोखीम संकेतांचे पुनरावलोकन करून संशयित प्रकरणांची तपासणी करा.",

            labStaff: "प्रयोगशाळा कर्मचारी",
            labStaffText:
                "चाचण्या, निष्कर्ष आणि पडताळणी निकाल व्यवस्थापित करा.",

            districtOfficer: "जिल्हा अधिकारी",
            districtOfficerText:
                "जिल्हास्तरीय इशारे, क्लस्टर्स आणि देखरेख क्रियाकलापांचे निरीक्षण करा.",

            stateAdministration: "राज्य प्रशासन",
            stateAdministrationText:
                "राज्यस्तरीय देखरेख बुद्धिमत्ता आणि उदयोन्मुख आरोग्य संकेत पहा.",

            responsibleAI: "जबाबदार AI आणि देखरेख",
            responsibleAIText:
                "हे व्यासपीठ AI-सहाय्यित जोखीम मूल्यांकन आणि पूर्व-इशारा संकेत देते. हे पशुवैद्यकीय निदान, प्रयोगशाळा चाचणी किंवा महामारीशास्त्रीय पुष्टीची जागा घेत नाही.",

            getStartedTitle:
                "तंत्रज्ञानाद्वारे पशुधन आरोग्य देखरेख मजबूत करणे",
            getStartedText:
                "क्षेत्रीय निरीक्षणे, पशुवैद्यकीय कौशल्य, प्रयोगशाळा पडताळणी आणि सरकारी देखरेख एका व्यासपीठावर जोडा.",

            createAccount: "खाते तयार करा",

            footerPlatform: "व्यासपीठ",
            footerAccount: "खाते",

            welcomeBack: "पुन्हा स्वागत आहे",
            loginSubtitle:
                "पशुधन आरोग्य देखरेख व्यासपीठ सुरू ठेवण्यासाठी लॉगिन करा.",
            createYourAccount: "आपले खाते तयार करा",
            registerSubtitle:
                "पशुधन आरोग्य देखरेखीत सहभागी होण्यासाठी खाते तयार करा.",

            name: "नाव",
            email: "ईमेल",
            username: "वापरकर्तानाव",
            password: "पासवर्ड",
            confirmPassword: "पासवर्डची पुष्टी करा",
            currentPassword: "सध्याचा पासवर्ड",
            newPassword: "नवीन पासवर्ड",
            language: "भाषा",
            role: "भूमिका",

            loginSuccessful: "लॉगिन यशस्वी.",
            registrationSuccessful: "नोंदणी यशस्वी.",
            invalidCredentials:
                "वापरकर्तानाव/ईमेल किंवा पासवर्ड चुकीचा आहे.",
            accountCreated:
                "आपले खाते यशस्वीरित्या तयार झाले आहे.",
            alreadyHaveAccount: "आधीच खाते आहे?",
            dontHaveAccount: "खाते नाही?",
            passwordRequirements:
                "पासवर्डमध्ये किमान 6 अक्षरे असणे आवश्यक आहे.",

            farmerDashboard: "शेतकरी डॅशबोर्ड",
            welcome: "स्वागत",
            dashboardOverview: "डॅशबोर्ड आढावा",
            monitoredAnimals: "देखरेखीतील पशुधन",
            totalReports: "एकूण अहवाल",
            activeAlerts: "सक्रिय इशारे",
            highRiskCases: "उच्च जोखीम प्रकरणे",
            mediumRiskCases: "मध्यम जोखीम प्रकरणे",
            lowRiskCases: "कमी जोखीम प्रकरणे",
            validatedCases: "पडताळलेली प्रकरणे",
            underInvestigation: "तपासणीखाली",
            sentToLaboratory: "प्रयोगशाळेत पाठवलेले",
            sentToSurveillance: "देखरेखीसाठी पाठवलेले",

            reportAnimalHealth: "पशुधन आरोग्य अहवाल",
            myReports: "माझे अहवाल",
            myAnimals: "माझे पशुधन",
            alerts: "इशारे",
            profile: "प्रोफाइल",

            reportHealth: "पशुधन आरोग्य अहवाल",
            animalName: "पशुधनाचे नाव",
            species: "प्रजाती",
            symptoms: "लक्षणे",
            symptomDescription: "लक्षणांचे वर्णन",
            severity: "तीव्रता",
            mild: "सौम्य",
            moderate: "मध्यम",
            severe: "गंभीर",

            describeSymptoms:
                "पशुधनामध्ये दिसणाऱ्या लक्षणांचे वर्णन करा.",
            selectSpecies: "प्रजाती निवडा",
            cattle: "गाय",
            buffalo: "म्हैस",
            goat: "शेळी",
            sheep: "मेंढी",
            poultry: "कुक्कुट",
            pig: "डुक्कर",
            other: "इतर",

            searchLocation: "स्थान शोधा",
            currentLocation: "सध्याचे स्थान वापरा",
            latitude: "अक्षांश",
            longitude: "रेखांश",

            uploadPhoto: "फोटो अपलोड करा",
            uploadAudio: "ऑडिओ अपलोड करा",
            optional: "पर्यायी",

            aiPreview: "AI जोखीम पूर्वदृश्य",
            calculateRisk: "जोखीम मोजा",
            submitting: "सबमिट होत आहे...",
            reportSubmitted:
                "आरोग्य अहवाल यशस्वीरित्या सबमिट झाला.",
            riskScore: "जोखीम गुण",
            riskLevel: "जोखीम पातळी",

            lowRisk: "कमी जोखीम",
            mediumRisk: "मध्यम जोखीम",
            highRisk: "उच्च जोखीम",

            veterinaryDashboard: "पशुवैद्यकीय डॅशबोर्ड",
            caseQueue: "प्रकरण रांग",
            reviewCase: "प्रकरण पुनरावलोकन",
            investigateCase: "प्रकरण तपासा",
            investigation: "तपासणी",

            temperature: "तापमान",
            respiration: "श्वसन",
            hydration: "जलयोजन",
            appetite: "भूक",
            behaviour: "वर्तन",
            visibleSigns: "दृश्यमान चिन्हे",

            sampleType: "नमुना प्रकार",
            collectionDate: "संकलन तारीख",
            collectionNotes: "संकलन नोंदी",
            preliminaryAssessment: "प्राथमिक मूल्यांकन",
            surveillanceFlag: "देखरेख चिन्ह",

            newCase: "नवीन",
            underInvestigationStatus: "तपासणीखाली",
            sentToLab: "प्रयोगशाळेत पाठवले",
            validated: "पडताळलेले",
            rejected: "नाकारलेले",

            saveInvestigation: "तपासणी जतन करा",
            sendToLab: "प्रयोगशाळेत पाठवा",
            investigationSaved:
                "तपासणी तपशील यशस्वीरित्या जतन झाला.",

            laboratory: "प्रयोगशाळा",
            laboratoryDashboard: "प्रयोगशाळा डॅशबोर्ड",
            sampleId: "नमुना ID",
            testType: "चाचणी प्रकार",
            result: "निकाल",
            assayReference: "Assay संदर्भ",
            findings: "निष्कर्ष",
            surveillanceClassification:
                "देखरेख वर्गीकरण",
            validationDate: "पडताळणी तारीख",
            sentToSurveillanceText:
                "देखरेखीसाठी पाठवले",

            microscopicExamination: "सूक्ष्मदर्शकीय तपासणी",
            cultureIsolation: "कल्चर / आयसोलेशन",
            pcrMolecularTest: "PCR / आण्विक चाचणी",
            serologicalTest: "सीरोलॉजिकल चाचणी",
            rapidDiagnosticTest: "जलद निदान चाचणी",
            milkQualityAnalysis: "दुधाची गुणवत्ता विश्लेषण",

            negative: "नकारात्मक",
            positive: "सकारात्मक",
            inconclusive: "अनिर्णित",

            saveValidation: "पडताळणी जतन करा",
            sendForSurveillance: "देखरेखीसाठी पाठवा",
            laboratorySaved:
                "प्रयोगशाळा निकाल यशस्वीरित्या जतन झाला.",

            governmentDashboard: "सरकारी डॅशबोर्ड",
            surveillanceDashboard: "देखरेख डॅशबोर्ड",
            governmentOverview: "सरकारी आढावा",
            recentReports: "अलीकडील अहवाल",
            districtSummary: "जिल्हा आढावा",
            riskDistribution: "जोखीम वितरण",
            clusterIntelligenceTitle: "क्लस्टर बुद्धिमत्ता",
            gisMap: "GIS देखरेख नकाशा",
            potentialEmergingClusters:
                "संभाव्य उदयोन्मुख क्लस्टर्स",

            locationClusters: "स्थान क्लस्टर्स",
            symptomClusters: "लक्षण क्लस्टर्स",
            clusterScore: "क्लस्टर गुण",
            priority: "प्राधान्य",
            signalReasons: "संकेत कारणे",
            repeatedSymptoms: "पुनरावृत्ती होणारी लक्षणे",
            speciesDistribution: "प्रजाती वितरण",
            reportCount: "अहवाल संख्या",

            highPriority: "उच्च प्राधान्य",
            moderatePriority: "मध्यम प्राधान्य",
            watch: "निरीक्षण",

            potentialClusterNotice:
                "संभाव्य क्लस्टर संकेतांची पुष्टी करण्यापूर्वी पशुवैद्यकीय, प्रयोगशाळा आणि महामारीशास्त्रीय तपासणी आवश्यक आहे.",

            notifications: "सूचना",
            unreadNotifications: "न वाचलेल्या सूचना",
            markAsRead: "वाचलेले म्हणून चिन्हांकित करा",
            markAllAsRead: "सर्व वाचलेले म्हणून चिन्हांकित करा",
            noNotifications: "सूचना नाहीत.",
            notificationMarkedRead:
                "सूचना वाचलेली म्हणून चिन्हांकित केली.",
            allNotificationsRead:
                "सर्व सूचना वाचलेल्या म्हणून चिन्हांकित केल्या.",

            gisSurveillanceTitle: "GIS देखरेख",
            mapLegend: "नकाशा संकेत",
            allRisk: "सर्व जोखीम पातळी",
            clusterSignal: "क्लस्टर संकेत",
            reportLocation: "अहवाल स्थान",
            mapLoading: "देखरेख नकाशा लोड होत आहे...",

            unableToLoad: "डेटा लोड करता आला नाही.",
            unableToSubmit: "सबमिट करता आले नाही.",
            sessionExpired:
                "आपले सत्र कालबाह्य झाले आहे. पुन्हा लॉगिन करा.",
            unauthorized:
                "या पृष्ठावर प्रवेश करण्याची आपल्याला परवानगी नाही.",
            somethingWentWrong:
                "काहीतरी चूक झाली. पुन्हा प्रयत्न करा.",
            connectionError:
                "सर्व्हरशी कनेक्ट करता आले नाही.",

            aiDisclaimer:
                "AI-निर्मित जोखीम संकेत पूर्व इशारा आणि प्राधान्यक्रमासाठी आहेत. ते स्वयंचलित रोग निदान दर्शवत नाहीत.",
            veterinaryValidation:
                "रोग किंवा उद्रेकाची पुष्टी करण्यासाठी पशुवैद्यकीय आणि प्रयोगशाळा पडताळणी आवश्यक आहे.",
        },

        hi: {
            home: "होम",
            about: "जानकारी",
            features: "विशेषताएँ",
            workflow: "कार्यप्रवाह",
            login: "लॉगिन",
            register: "पंजीकरण",
            logout: "लॉगआउट",
            save: "सहेजें",
            submit: "जमा करें",
            cancel: "रद्द करें",
            close: "बंद करें",
            back: "वापस",
            next: "आगे",
            search: "खोजें",
            filter: "फ़िल्टर",
            refresh: "रिफ्रेश",
            loading: "लोड हो रहा है...",
            noData: "कोई डेटा उपलब्ध नहीं है।",
            success: "सफल",
            error: "त्रुटि",
            warning: "चेतावनी",
            information: "जानकारी",
            view: "देखें",
            edit: "संपादित करें",
            delete: "हटाएँ",
            status: "स्थिति",
            date: "तारीख",
            location: "स्थान",
            description: "विवरण",
            actions: "कार्रवाई",

            brandName: "UyirThulir",
            brandSubtitle: "पशुधन स्वास्थ्य निगरानी",

            heroBadge: "AI-सक्षम पशुधन स्वास्थ्य निगरानी",
            heroTitle: "पशुधन स्वास्थ्य के लिए प्रारंभिक चेतावनी",
            heroDescription:
                "किसानों, फील्ड कर्मचारियों, पशु चिकित्सकों, प्रयोगशालाओं और सरकारी अधिकारियों को स्वास्थ्य जोखिम संकेतों की जल्दी पहचान करने और समय पर कार्रवाई में सहायता करने वाला डिजिटल निगरानी प्लेटफॉर्म।",
            getStarted: "शुरू करें",
            signIn: "साइन इन",
            heroNote:
                "AI-सहायित जोखिम मूल्यांकन • पशु चिकित्सकीय समीक्षा • प्रयोगशाला सत्यापन • सरकारी निगरानी",

            surveillanceStatus: "निगरानी स्थिति",
            earlyWarningActive: "प्रारंभिक चेतावनी सक्रिय",
            monitoring: "निगरानी",
            riskSignal: "जोखिम संकेत",
            veterinaryReview: "पशु चिकित्सकीय समीक्षा",
            clusterIntelligence: "क्लस्टर इंटेलिजेंस",
            locationMonitoring: "स्थान निगरानी",

            aboutPlatform: "प्लेटफॉर्म के बारे में",
            fromFieldToSurveillance:
                "फील्ड रिपोर्ट से समन्वित निगरानी तक",
            aboutDescription:
                "UyirThulir पूरे पशुधन स्वास्थ्य निगरानी कार्यप्रवाह को एक प्लेटफॉर्म पर जोड़ता है।",

            digitalHealthReporting: "डिजिटल स्वास्थ्य रिपोर्टिंग",
            digitalHealthReportingText:
                "किसान और फील्ड कर्मचारी लक्षण, विवरण, स्थान, फोटो और ऑडियो प्रमाण के साथ पशु स्वास्थ्य जानकारी जमा कर सकते हैं।",

            aiRiskAssessment: "AI-सहायित जोखिम मूल्यांकन",
            aiRiskAssessmentText:
                "रिपोर्ट की गई जानकारी को पशु चिकित्सकीय प्राथमिकता के लिए प्रारंभिक चेतावनी जोखिम संकेत में बदला जाता है।",

            veterinaryInvestigation: "पशु चिकित्सकीय जाँच",
            veterinaryInvestigationText:
                "पशु चिकित्सक मामलों की समीक्षा कर जाँच निष्कर्ष, नमूने और प्रारंभिक मूल्यांकन दर्ज कर सकते हैं।",

            governmentSurveillance: "सरकारी निगरानी",
            governmentSurveillanceText:
                "सरकारी अधिकारी जोखिम रुझान, स्थान संकेत, सत्यापित मामलों और निगरानी गतिविधियों को देख सकते हैं।",

            coreCapabilities: "मुख्य क्षमताएँ",
            onePlatform:
                "एक प्लेटफॉर्म पर पूरी निगरानी प्रक्रिया",

            healthReporting: "स्वास्थ्य रिपोर्टिंग",
            healthReportingText:
                "फील्ड से पशु स्वास्थ्य जानकारी दर्ज करें।",

            aiRiskSignal: "AI जोखिम संकेत",
            aiRiskSignalText:
                "लक्षणों और निरीक्षणों को प्रारंभिक चेतावनी जोखिम स्कोर में बदलें।",

            smartNotifications: "स्मार्ट सूचनाएँ",
            smartNotificationsText:
                "महत्वपूर्ण जोखिम संकेतों को संबंधित उपयोगकर्ताओं तक पहुँचाएँ।",

            caseInvestigation: "केस जाँच",
            caseInvestigationText:
                "पशु चिकित्सक जाँच निष्कर्ष, नमूने और प्रारंभिक आकलन दर्ज करते हैं।",

            laboratoryValidation: "प्रयोगशाला सत्यापन",
            laboratoryValidationText:
                "निगरानी वर्गीकरण से पहले प्रयोगशाला परीक्षण और सत्यापित परिणाम दर्ज करें।",

            gisSurveillance: "GIS निगरानी",
            gisSurveillanceText:
                "रिपोर्ट स्थानों और संभावित उभरते क्लस्टरों को नक्शे पर देखें।",

            surveillanceWorkflow: "निगरानी कार्यप्रवाह",
            observeAssessInvestigateValidateRespond:
                "निरीक्षण → मूल्यांकन → जाँच → सत्यापन → प्रतिक्रिया",

            fieldReport: "फील्ड रिपोर्ट",
            fieldReportText:
                "किसान या फील्ड कर्मचारी पशु स्वास्थ्य निरीक्षण दर्ज करता है।",

            riskAssessment: "जोखिम मूल्यांकन",
            riskAssessmentText:
                "AI-सहायित विश्लेषण प्राथमिकता के लिए जोखिम संकेत उत्पन्न करता है।",

            veterinaryReview: "पशु चिकित्सकीय समीक्षा",
            veterinaryReviewText:
                "पशु चिकित्सक रिपोर्ट किए गए मामले की जाँच करता है।",

            laboratoryValidationStep: "प्रयोगशाला सत्यापन",
            laboratoryValidationTextStep:
                "नमूनों की जाँच की जाती है और परिणाम दर्ज किए जाते हैं।",

            governmentSurveillanceStep: "सरकारी निगरानी",
            governmentSurveillanceTextStep:
                "सत्यापित जानकारी निगरानी और रोकथाम में सहायता करती है।",

            roleBasedAccess: "भूमिका आधारित प्रवेश",
            responseChain:
                "प्रतिक्रिया श्रृंखला के प्रत्येक स्तर के लिए डिज़ाइन किया गया",

            farmer: "किसान",
            farmerText:
                "पशु स्वास्थ्य निरीक्षण दर्ज करें और जमा किए गए मामलों को ट्रैक करें।",

            fieldWorker: "फील्ड कर्मचारी",
            fieldWorkerText:
                "फील्ड रिपोर्ट जमा करें और पशुधन निगरानी में सहायता करें।",

            veterinarian: "पशु चिकित्सक",
            veterinarianText:
                "जोखिम संकेतों की समीक्षा करें और संदिग्ध मामलों की जाँच करें।",

            labStaff: "प्रयोगशाला कर्मचारी",
            labStaffText:
                "परीक्षण, निष्कर्ष और सत्यापन परिणामों का प्रबंधन करें।",

            districtOfficer: "जिला अधिकारी",
            districtOfficerText:
                "जिला स्तर के अलर्ट, क्लस्टर और निगरानी गतिविधियों की निगरानी करें।",

            stateAdministration: "राज्य प्रशासन",
            stateAdministrationText:
                "राज्य स्तर की निगरानी जानकारी और उभरते स्वास्थ्य संकेत देखें।",

            responsibleAI: "जिम्मेदार AI और निगरानी",
            responsibleAIText:
                "यह प्लेटफॉर्म AI-सहायित जोखिम मूल्यांकन और प्रारंभिक चेतावनी संकेत प्रदान करता है। यह पशु चिकित्सकीय निदान, प्रयोगशाला परीक्षण या महामारी विज्ञान की पुष्टि का विकल्प नहीं है।",

            getStartedTitle:
                "तकनीक के माध्यम से पशुधन स्वास्थ्य निगरानी को मजबूत करना",
            getStartedText:
                "फील्ड निरीक्षण, पशु चिकित्सकीय विशेषज्ञता, प्रयोगशाला सत्यापन और सरकारी निगरानी को एक प्लेटफॉर्म पर जोड़ें।",

            createAccount: "खाता बनाएँ",

            footerPlatform: "प्लेटफॉर्म",
            footerAccount: "खाता",

            welcomeBack: "वापसी पर स्वागत है",
            loginSubtitle:
                "पशुधन स्वास्थ्य निगरानी प्लेटफॉर्म जारी रखने के लिए लॉगिन करें।",
            createYourAccount: "अपना खाता बनाएँ",
            registerSubtitle:
                "पशुधन स्वास्थ्य निगरानी में भाग लेने के लिए खाता बनाएँ।",

            name: "नाम",
            email: "ईमेल",
            username: "उपयोगकर्ता नाम",
            password: "पासवर्ड",
            confirmPassword: "पासवर्ड की पुष्टि करें",
            currentPassword: "वर्तमान पासवर्ड",
            newPassword: "नया पासवर्ड",
            language: "भाषा",
            role: "भूमिका",

            loginSuccessful: "लॉगिन सफल हुआ।",
            registrationSuccessful: "पंजीकरण सफल हुआ।",
            invalidCredentials:
                "उपयोगकर्ता नाम/ईमेल या पासवर्ड गलत है।",
            accountCreated:
                "आपका खाता सफलतापूर्वक बनाया गया है।",
            alreadyHaveAccount: "क्या पहले से खाता है?",
            dontHaveAccount: "क्या आपके पास खाता नहीं है?",
            passwordRequirements:
                "पासवर्ड में कम से कम 6 अक्षर होने चाहिए।",

            farmerDashboard: "किसान डैशबोर्ड",
            welcome: "स्वागत",
            dashboardOverview: "डैशबोर्ड अवलोकन",
            monitoredAnimals: "निगरानी में पशु",
            totalReports: "कुल रिपोर्ट",
            activeAlerts: "सक्रिय अलर्ट",
            highRiskCases: "उच्च जोखिम वाले मामले",
            mediumRiskCases: "मध्यम जोखिम वाले मामले",
            lowRiskCases: "कम जोखिम वाले मामले",
            validatedCases: "सत्यापित मामले",
            underInvestigation: "जाँच के अंतर्गत",
            sentToLaboratory: "प्रयोगशाला भेजे गए",
            sentToSurveillance: "निगरानी के लिए भेजे गए",

            reportAnimalHealth: "पशु स्वास्थ्य रिपोर्ट",
            myReports: "मेरी रिपोर्ट",
            myAnimals: "मेरे पशु",
            alerts: "अलर्ट",
            profile: "प्रोफ़ाइल",

            reportHealth: "पशु स्वास्थ्य रिपोर्ट",
            animalName: "पशु का नाम",
            species: "प्रजाति",
            symptoms: "लक्षण",
            symptomDescription: "लक्षण विवरण",
            severity: "गंभीरता",
            mild: "हल्का",
            moderate: "मध्यम",
            severe: "गंभीर",

            describeSymptoms:
                "पशु में देखे गए लक्षणों का वर्णन करें।",
            selectSpecies: "प्रजाति चुनें",
            cattle: "गाय",
            buffalo: "भैंस",
            goat: "बकरी",
            sheep: "भेड़",
            poultry: "मुर्गी",
            pig: "सूअर",
            other: "अन्य",

            searchLocation: "स्थान खोजें",
            currentLocation: "वर्तमान स्थान का उपयोग करें",
            latitude: "अक्षांश",
            longitude: "देशांतर",

            uploadPhoto: "फोटो अपलोड करें",
            uploadAudio: "ऑडियो अपलोड करें",
            optional: "वैकल्पिक",

            aiPreview: "AI जोखिम पूर्वावलोकन",
            calculateRisk: "जोखिम की गणना करें",
            submitting: "जमा किया जा रहा है...",
            reportSubmitted:
                "स्वास्थ्य रिपोर्ट सफलतापूर्वक जमा की गई।",
            riskScore: "जोखिम स्कोर",
            riskLevel: "जोखिम स्तर",

            lowRisk: "कम जोखिम",
            mediumRisk: "मध्यम जोखिम",
            highRisk: "उच्च जोखिम",

            veterinaryDashboard: "पशु चिकित्सकीय डैशबोर्ड",
            caseQueue: "केस कतार",
            reviewCase: "केस की समीक्षा करें",
            investigateCase: "केस की जाँच करें",
            investigation: "जाँच",

            temperature: "तापमान",
            respiration: "श्वसन",
            hydration: "जलयोजन",
            appetite: "भूख",
            behaviour: "व्यवहार",
            visibleSigns: "दिखाई देने वाले संकेत",

            sampleType: "नमूना प्रकार",
            collectionDate: "संग्रह तिथि",
            collectionNotes: "संग्रह नोट्स",
            preliminaryAssessment: "प्रारंभिक मूल्यांकन",
            surveillanceFlag: "निगरानी संकेत",

            newCase: "नया",
            underInvestigationStatus: "जाँच के अंतर्गत",
            sentToLab: "प्रयोगशाला भेजा गया",
            validated: "सत्यापित",
            rejected: "अस्वीकृत",

            saveInvestigation: "जाँच सहेजें",
            sendToLab: "प्रयोगशाला भेजें",
            investigationSaved:
                "जाँच विवरण सफलतापूर्वक सहेजा गया।",

            laboratory: "प्रयोगशाला",
            laboratoryDashboard: "प्रयोगशाला डैशबोर्ड",
            sampleId: "नमूना ID",
            testType: "परीक्षण प्रकार",
            result: "परिणाम",
            assayReference: "Assay संदर्भ",
            findings: "निष्कर्ष",
            surveillanceClassification:
                "निगरानी वर्गीकरण",
            validationDate: "सत्यापन तिथि",
            sentToSurveillanceText:
                "निगरानी के लिए भेजा गया",

            microscopicExamination: "सूक्ष्मदर्शी परीक्षण",
            cultureIsolation: "कल्चर / आइसोलेशन",
            pcrMolecularTest: "PCR / आणविक परीक्षण",
            serologicalTest: "सीरोलॉजिकल परीक्षण",
            rapidDiagnosticTest: "रैपिड डायग्नोस्टिक परीक्षण",
            milkQualityAnalysis: "दूध गुणवत्ता विश्लेषण",

            negative: "नकारात्मक",
            positive: "सकारात्मक",
            inconclusive: "अनिर्णायक",

            saveValidation: "सत्यापन सहेजें",
            sendForSurveillance: "निगरानी के लिए भेजें",
            laboratorySaved:
                "प्रयोगशाला परिणाम सफलतापूर्वक सहेजा गया।",

            governmentDashboard: "सरकारी डैशबोर्ड",
            surveillanceDashboard: "निगरानी डैशबोर्ड",
            governmentOverview: "सरकारी अवलोकन",
            recentReports: "हाल की रिपोर्ट",
            districtSummary: "जिला सारांश",
            riskDistribution: "जोखिम वितरण",
            clusterIntelligenceTitle: "क्लस्टर इंटेलिजेंस",
            gisMap: "GIS निगरानी मानचित्र",
            potentialEmergingClusters:
                "संभावित उभरते क्लस्टर",

            locationClusters: "स्थान क्लस्टर",
            symptomClusters: "लक्षण क्लस्टर",
            clusterScore: "क्लस्टर स्कोर",
            priority: "प्राथमिकता",
            signalReasons: "संकेत कारण",
            repeatedSymptoms: "दोहराए गए लक्षण",
            speciesDistribution: "प्रजाति वितरण",
            reportCount: "रिपोर्ट संख्या",

            highPriority: "उच्च प्राथमिकता",
            moderatePriority: "मध्यम प्राथमिकता",
            watch: "निगरानी",

            potentialClusterNotice:
                "संभावित क्लस्टर संकेतों की पुष्टि से पहले पशु चिकित्सकीय, प्रयोगशाला और महामारी विज्ञान समीक्षा आवश्यक है।",

            notifications: "सूचनाएँ",
            unreadNotifications: "अपठित सूचनाएँ",
            markAsRead: "पढ़ा हुआ चिन्हित करें",
            markAllAsRead: "सभी को पढ़ा हुआ चिन्हित करें",
            noNotifications: "कोई सूचनाएँ नहीं हैं।",
            notificationMarkedRead:
                "सूचना को पढ़ा हुआ चिन्हित किया गया।",
            allNotificationsRead:
                "सभी सूचनाओं को पढ़ा हुआ चिन्हित किया गया।",

            gisSurveillanceTitle: "GIS निगरानी",
            mapLegend: "मानचित्र संकेत",
            allRisk: "सभी जोखिम स्तर",
            clusterSignal: "क्लस्टर संकेत",
            reportLocation: "रिपोर्ट स्थान",
            mapLoading: "निगरानी मानचित्र लोड हो रहा है...",

            unableToLoad: "डेटा लोड नहीं किया जा सका।",
            unableToSubmit: "सबमिट नहीं किया जा सका।",
            sessionExpired:
                "आपका सत्र समाप्त हो गया है। कृपया फिर से लॉगिन करें।",
            unauthorized:
                "आपको इस पृष्ठ तक पहुँचने की अनुमति नहीं है।",
            somethingWentWrong:
                "कुछ गलत हो गया। कृपया फिर से प्रयास करें।",
            connectionError:
                "सर्वर से कनेक्ट नहीं हो सका।",

            aiDisclaimer:
                "AI-जनित जोखिम संकेत केवल प्रारंभिक चेतावनी और प्राथमिकता के लिए हैं। वे स्वचालित रोग निदान नहीं हैं।",
            veterinaryValidation:
                "किसी बीमारी या प्रकोप की पुष्टि के लिए पशु चिकित्सकीय और प्रयोगशाला सत्यापन आवश्यक है।",
        }
    };


    /* =====================================================
       LANGUAGE STORAGE
    ====================================================== */

    const STORAGE_KEY = "uyirthulir_language";


    function getCurrentLanguage() {
        const storedLanguage = localStorage.getItem(STORAGE_KEY);

        if (
            storedLanguage &&
            Object.prototype.hasOwnProperty.call(
                translations,
                storedLanguage
            )
        ) {
            return storedLanguage;
        }

        return "en";
    }


    function setCurrentLanguage(language) {
        if (
            !Object.prototype.hasOwnProperty.call(
                translations,
                language
            )
        ) {
            language = "en";
        }

        localStorage.setItem(STORAGE_KEY, language);

        document.documentElement.lang = language;

        window.dispatchEvent(
            new CustomEvent(
                "uyirthulirLanguageChanged",
                {
                    detail: {
                        language: language
                    }
                }
            )
        );
    }


    /* =====================================================
       TRANSLATION LOOKUP
    ====================================================== */

    function translate(key, language) {
        const selectedLanguage =
            language || getCurrentLanguage();

        const selectedTranslations =
            translations[selectedLanguage] || translations.en;

        if (
            Object.prototype.hasOwnProperty.call(
                selectedTranslations,
                key
            )
        ) {
            return selectedTranslations[key];
        }

        if (
            Object.prototype.hasOwnProperty.call(
                translations.en,
                key
            )
        ) {
            return translations.en[key];
        }

        return key;
    }


    /* =====================================================
       APPLY DATA-I18N
    ====================================================== */

    function applyTranslations(root = document) {
        const language = getCurrentLanguage();

        root.querySelectorAll("[data-i18n]").forEach(
            function (element) {
                const key = element.getAttribute("data-i18n");

                element.textContent = translate(
                    key,
                    language
                );
            }
        );


        root.querySelectorAll("[data-i18n-placeholder]").forEach(
            function (element) {
                const key = element.getAttribute(
                    "data-i18n-placeholder"
                );

                element.setAttribute(
                    "placeholder",
                    translate(
                        key,
                        language
                    )
                );
            }
        );


        root.querySelectorAll("[data-i18n-title]").forEach(
            function (element) {
                const key = element.getAttribute(
                    "data-i18n-title"
                );

                element.setAttribute(
                    "title",
                    translate(
                        key,
                        language
                    )
                );
            }
        );


        root.querySelectorAll("[data-i18n-aria-label]").forEach(
            function (element) {
                const key = element.getAttribute(
                    "data-i18n-aria-label"
                );

                element.setAttribute(
                    "aria-label",
                    translate(
                        key,
                        language
                    )
                );
            }
        );


        updateLanguageSelectors(language);
    }


    /* =====================================================
       UPDATE LANGUAGE SELECTORS
    ====================================================== */

    function updateLanguageSelectors(language) {
        document
            .querySelectorAll(
                "#languageSelector, .language-selector"
            )
            .forEach(
                function (selector) {
                    selector.value = language;
                }
            );
    }


    /* =====================================================
       LANGUAGE SELECTOR LISTENER
    ====================================================== */

    function initialiseLanguageSelectors() {
        const currentLanguage =
            getCurrentLanguage();

        document
            .querySelectorAll(
                "#languageSelector, .language-selector"
            )
            .forEach(
                function (selector) {
                    selector.value = currentLanguage;

                    selector.addEventListener(
                        "change",
                        function (event) {
                            const language =
                                event.target.value;

                            setCurrentLanguage(language);

                            applyTranslations();
                        }
                    );
                }
            );
    }


    /* =====================================================
       GLOBAL HELPER
    ====================================================== */

    window.t = function (key, language) {
        return translate(key, language);
    };


    window.translate = translate;


    window.applyTranslations =
        applyTranslations;


    window.getCurrentLanguage =
        getCurrentLanguage;


    window.setCurrentLanguage =
        setCurrentLanguage;


    window.translations =
        translations;


    /* =====================================================
       INITIALISE
    ====================================================== */

    document.addEventListener(
        "DOMContentLoaded",
        function () {
            document.documentElement.lang =
                getCurrentLanguage();

            initialiseLanguageSelectors();

            applyTranslations();
        }
    );


    window.addEventListener(
        "uyirthulirLanguageChanged",
        function () {
            applyTranslations();
        }
    );

})();