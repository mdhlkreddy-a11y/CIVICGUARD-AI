const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("reportForm");
const message = document.getElementById("message");
const reportsList = document.getElementById("reportsList");
const submitBtn = document.getElementById("submitBtn");

// Submit report
form.addEventListener("submit", async function(event) {
    event.preventDefault();

    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";
    message.textContent = "";

    const reportData = {
        title: document.getElementById("title").value.trim(),
        description: document.getElementById("description").value.trim(),
        category: document.getElementById("category").value,
        location: document.getElementById("location").value.trim()
    };

    try {
        const response = await fetch(`${API_URL}/reports`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(reportData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Submission failed");
        }

        message.textContent = "✅ Report submitted successfully!";
        message.style.color = "green";

        form.reset();

        await loadReports();

    } catch (error) {
        message.textContent = "❌ " + error.message;
        message.style.color = "red";
        console.error(error);

    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Report";
    }
});


// Load submitted reports
async function loadReports() {
    try {
        const response = await fetch(`${API_URL}/reports`);

        if (!response.ok) {
            throw new Error("Could not load reports");
        }

        const reports = await response.json();

        reportsList.replaceChildren();

        if (reports.length === 0) {
            reportsList.textContent = "No reports submitted yet.";
            return;
        }

        reports.forEach(report => {
            const card = document.createElement("div");
            card.className = "report-card";

            const title = document.createElement("h3");
            title.textContent = report.title;

            const description = document.createElement("p");
            description.textContent = report.description;

            const category = document.createElement("p");
            category.textContent = "Category: " + report.category;

            const location = document.createElement("p");
            location.textContent = "Location: " + report.location;

            const status = document.createElement("p");
            status.className = "status";
            status.textContent = "Status: " + report.status;

            const id = document.createElement("p");
            id.textContent = "Report ID: " + report.id;

            card.append(title, description, category, location, status, id);
            reportsList.appendChild(card);
        });

    } catch (error) {
        reportsList.textContent = "Unable to connect to backend.";
        console.error(error);
    }
}

// Load reports when page opens
loadReports();