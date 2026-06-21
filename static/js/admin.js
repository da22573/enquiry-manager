const rowsContainer = document.getElementById("enquiry-rows");
const countLabel = document.getElementById("enquiry-count");
const feedback = document.getElementById("admin-feedback");
const searchInput = document.getElementById("filter-search");
const serviceFilter = document.getElementById("filter-service");
const statusFilter = document.getElementById("filter-status");
const detailModal = document.getElementById("detail-modal");
const detailContent = document.getElementById("detail-content");
const closeModalButton = document.getElementById("close-modal");

let enquiries = [];

function formatDate(isoString) {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(isoString));
}

function showFeedback(message, type) {
  feedback.innerHTML = `<div class="alert alert--${type}">${message}</div>`;
}

function buildQueryString() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) {
    params.set("q", searchInput.value.trim());
  }
  if (serviceFilter.value) {
    params.set("service", serviceFilter.value);
  }
  if (statusFilter.value) {
    params.set("status", statusFilter.value);
  }
  return params.toString();
}

async function loadEnquiries() {
  countLabel.textContent = "Loading enquiries...";
  rowsContainer.innerHTML = "";

  try {
    const query = buildQueryString();
    const response = await fetch(`/api/enquiries${query ? `?${query}` : ""}`);
    enquiries = await response.json();
    renderTable();
  } catch (error) {
    countLabel.textContent = "Unable to load enquiries.";
    showFeedback("Could not load enquiries. Please refresh the page.", "error");
  }
}

function statusLabel(status) {
  return status === "reviewed" ? "Reviewed ✓" : "New";
}

function statusToggleAriaLabel(status) {
  if (status === "new") {
    return "Status: new. Click to mark as reviewed.";
  }
  return "Status: reviewed. Click to mark as new.";
}

function renderTable() {
  rowsContainer.innerHTML = "";

  if (enquiries.length === 0) {
    countLabel.textContent = "No enquiries match your filters.";
    return;
  }

  countLabel.textContent = `${enquiries.length} enquir${enquiries.length === 1 ? "y" : "ies"} shown`;

  enquiries.forEach((enquiry) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td data-label="Name">${escapeHtml(enquiry.fullName)}</td>
      <td data-label="Email"><a href="mailto:${escapeHtml(enquiry.email)}">${escapeHtml(enquiry.email)}</a></td>
      <td data-label="Service">${escapeHtml(enquiry.service)}</td>
      <td data-label="Submitted">${formatDate(enquiry.submittedAt)}</td>
      <td data-label="Status">
        <button
          type="button"
          class="status-toggle status-toggle--${enquiry.status}"
          data-action="toggle-status"
          data-id="${enquiry.id}"
          aria-label="${statusToggleAriaLabel(enquiry.status)}"
        >
          ${statusLabel(enquiry.status)}
        </button>
      </td>
      <td data-label="Details">
        <button class="button button--secondary" type="button" data-action="view" data-id="${enquiry.id}">
          View
        </button>
      </td>
    `;

    rowsContainer.appendChild(row);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function openDetails(enquiryId) {
  const enquiry = enquiries.find((item) => item.id === enquiryId);
  if (!enquiry) {
    return;
  }

  detailContent.innerHTML = `
    <div>
      <dt>Name</dt>
      <dd>${escapeHtml(enquiry.fullName)}</dd>
    </div>
    <div>
      <dt>Email</dt>
      <dd><a href="mailto:${escapeHtml(enquiry.email)}">${escapeHtml(enquiry.email)}</a></dd>
    </div>
    <div>
      <dt>Phone</dt>
      <dd>${enquiry.phone ? escapeHtml(enquiry.phone) : "Not provided"}</dd>
    </div>
    <div>
      <dt>Service</dt>
      <dd>${escapeHtml(enquiry.service)}</dd>
    </div>
    <div>
      <dt>Status</dt>
      <dd>${escapeHtml(enquiry.status)}</dd>
    </div>
    <div>
      <dt>Submitted</dt>
      <dd>${formatDate(enquiry.submittedAt)}</dd>
    </div>
    <div>
      <dt>Description</dt>
      <dd>${escapeHtml(enquiry.description)}</dd>
    </div>
  `;

  detailModal.showModal();
}

async function toggleStatus(enquiryId) {
  const enquiry = enquiries.find((item) => item.id === enquiryId);
  if (!enquiry) {
    return;
  }

  const nextStatus = enquiry.status === "new" ? "reviewed" : "new";

  try {
    const response = await fetch(`/api/enquiries/${enquiryId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: nextStatus }),
    });

    if (!response.ok) {
      showFeedback("Could not update enquiry status.", "error");
      return;
    }

    await loadEnquiries();
    showFeedback("Enquiry status updated.", "success");
  } catch (error) {
    showFeedback("Could not update enquiry status.", "error");
  }
}

rowsContainer.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }

  const enquiryId = button.dataset.id;
  if (button.dataset.action === "view") {
    openDetails(enquiryId);
  }
  if (button.dataset.action === "toggle-status") {
    toggleStatus(enquiryId);
  }
});

closeModalButton.addEventListener("click", () => detailModal.close());
detailModal.addEventListener("click", (event) => {
  const dialogDimensions = detailModal.getBoundingClientRect();
  const clickedOutside =
    event.clientX < dialogDimensions.left ||
    event.clientX > dialogDimensions.right ||
    event.clientY < dialogDimensions.top ||
    event.clientY > dialogDimensions.bottom;

  if (clickedOutside) {
    detailModal.close();
  }
});

[searchInput, serviceFilter, statusFilter].forEach((element) => {
  element.addEventListener("input", loadEnquiries);
  element.addEventListener("change", loadEnquiries);
});

loadEnquiries();
