import { parsePhoneNumberWithError } from "https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.17/+esm";

const form = document.getElementById("enquiry-form");
const feedback = document.getElementById("form-feedback");
const submitButton = document.getElementById("submit-button");
const descriptionInput = document.getElementById("description");
const descriptionCounter = document.getElementById("description-counter");

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function updateDescriptionCounter() {
  const count = descriptionInput.value.length;
  descriptionCounter.textContent = `${count} / 1000`;
}

function validatePhone(countryRegion, nationalNumber) {
  const trimmed = nationalNumber.trim();

  if (!trimmed) {
    return { ok: true };
  }

  try {
    const phone = parsePhoneNumberWithError(trimmed, countryRegion);

    if (!phone.isValid()) {
      return {
        ok: false,
        message: "Enter a valid phone number for the selected country.",
      };
    }

    return { ok: true };
  } catch {
    return {
      ok: false,
      message: "Enter a valid phone number for the selected country.",
    };
  }
}

function setFieldError(fieldName, message) {
  const field = document.querySelector(`[data-field="${fieldName}"]`);
  const error = document.getElementById(`error-${fieldName}`);

  if (!field || !error) {
    return;
  }

  if (message) {
    field.classList.add("field--invalid");
    error.textContent = message;
    error.hidden = false;
  } else {
    field.classList.remove("field--invalid");
    error.textContent = "";
    error.hidden = true;
  }
}

function clearErrors() {
  ["fullName", "email", "phone", "service", "description"].forEach((fieldName) => {
    setFieldError(fieldName, "");
  });
}

function validateForm(formData) {
  const errors = {};
  const fullName = formData.get("fullName").trim();
  const email = formData.get("email").trim();
  const phoneCountry = formData.get("phoneCountry").trim();
  const phoneNational = formData.get("phoneNational").trim();
  const service = formData.get("service").trim();
  const description = formData.get("description").trim();

  if (!fullName) {
    errors.fullName = "Full name is required.";
  } else if (fullName.length > 100) {
    errors.fullName = "Full name must be 100 characters or fewer.";
  }

  if (!email) {
    errors.email = "Email address is required.";
  } else if (!emailPattern.test(email)) {
    errors.email = "Enter a valid email address.";
  }

  const phoneResult = validatePhone(phoneCountry, phoneNational);
  if (!phoneResult.ok) {
    errors.phone = phoneResult.message;
  }

  if (!service) {
    errors.service = "Please select a service.";
  }

  if (!description) {
    errors.description = "Please describe your enquiry.";
  } else if (description.length < 10) {
    errors.description = "Description must be at least 10 characters.";
  } else if (description.length > 1000) {
    errors.description = "Description must be 1000 characters or fewer.";
  }

  return errors;
}

function showFeedback(message, type) {
  feedback.innerHTML = `<div class="alert alert--${type}">${message}</div>`;
  feedback.scrollIntoView({ behavior: "smooth", block: "center" });
  feedback.focus({ preventScroll: true });
}

function clearFeedback() {
  feedback.innerHTML = "";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearFeedback();
  clearErrors();

  const formData = new FormData(form);
  const clientErrors = validateForm(formData);

  Object.entries(clientErrors).forEach(([fieldName, message]) => {
    setFieldError(fieldName, message);
  });

  if (Object.keys(clientErrors).length > 0) {
    showFeedback("Please fix the highlighted fields before submitting.", "error");
    return;
  }

  submitButton.disabled = true;

  try {
    const response = await fetch("/api/enquiries", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fullName: formData.get("fullName").trim(),
        email: formData.get("email").trim(),
        phoneCountry: formData.get("phoneCountry").trim(),
        phoneNational: formData.get("phoneNational").trim(),
        service: formData.get("service").trim(),
        description: formData.get("description").trim(),
      }),
    });

    const payload = await response.json();

    if (!response.ok) {
      Object.entries(payload.errors || {}).forEach(([fieldName, message]) => {
        setFieldError(fieldName, message);
      });
      showFeedback("We could not submit your enquiry. Please review the form.", "error");
      return;
    }

    form.reset();
    document.getElementById("phoneCountry").value = "GB";
    updateDescriptionCounter();
    showFeedback("Thank you. Your enquiry was received and will be reviewed shortly.", "success");
  } catch (error) {
    showFeedback("Something went wrong. Please try again in a moment.", "error");
  } finally {
    submitButton.disabled = false;
  }
});

["fullName", "email", "phoneNational", "phoneCountry", "service", "description"].forEach((fieldName) => {
  const input = document.getElementById(fieldName);
  input.addEventListener("input", () => setFieldError("phone", ""));
  input.addEventListener("change", () => setFieldError("phone", ""));
});

["fullName", "email", "service", "description"].forEach((fieldName) => {
  const input = document.getElementById(fieldName);
  input.addEventListener("input", () => setFieldError(fieldName, ""));
});

descriptionInput.addEventListener("input", updateDescriptionCounter);
updateDescriptionCounter();
