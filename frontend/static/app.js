document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const textArea = document.getElementById("contract_text");
    const fileInput = document.getElementById("file");
    const fileName = document.getElementById("upload-filename");
    const formStatus = document.getElementById("form-status");
    const loadDemoButton = document.getElementById("load-demo");
    const severityFilter = document.getElementById("severity-filter");
    const resultCards = Array.from(document.querySelectorAll(".result-card"));
    const submitButton = form ? form.querySelector(".primary-button") : null;

    const demoText = [
        "We may terminate your access to the service at any time without prior notice if we determine, in our sole discretion, that your use creates legal or operational risk.",
        "All disputes arising out of these terms must be resolved through binding arbitration, and you waive the right to participate in a class action lawsuit.",
        "We may share account and usage information with third-party partners, affiliates, and service providers for analytics, personalization, and commercial purposes.",
        "Subscriptions renew automatically unless cancelled before the renewal date, and payments already processed are non-refundable except where required by law."
    ].join(" ");

    if (fileInput && fileName) {
        fileInput.addEventListener("change", () => {
            const selected = fileInput.files && fileInput.files[0];
            fileName.textContent = selected ? selected.name : "No file selected";
        });
    }

    if (loadDemoButton && textArea) {
        loadDemoButton.addEventListener("click", () => {
            textArea.value = demoText;
            textArea.focus();
            if (formStatus) {
                formStatus.textContent = "Demo contract text loaded. You can analyze it directly or replace it with your own.";
            }
        });
    }

    if (form && submitButton) {
        form.addEventListener("submit", () => {
            submitButton.disabled = true;
            submitButton.textContent = "Analyzing...";

            if (formStatus) {
                formStatus.textContent = "Reading the document and generating the clause analysis.";
            }
        });
    }

    if (severityFilter && resultCards.length) {
        severityFilter.addEventListener("change", () => {
            const selected = severityFilter.value;

            resultCards.forEach((card) => {
                const matches = selected === "all" || card.dataset.severity === selected;
                card.classList.toggle("is-hidden", !matches);
            });
        });
    }
});
