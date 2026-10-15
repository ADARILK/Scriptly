const generateBtn = document.getElementById("generateBtn");
const topicInput = document.getElementById("topic");
const contentTypeSelect = document.getElementById("contentType");
const toneSelect = document.getElementById("tone");
const lengthSelect = document.getElementById("length");

const errorBox = document.getElementById("errorBox");
const loadingOverlay = document.getElementById("loadingOverlay");

const logPanel = document.getElementById("logPanel");
const logContent = document.getElementById("logContent");

const resultsPanel = document.getElementById("resultsPanel");
const researchOutput = document.getElementById("researchOutput");
const writerOutput = document.getElementById("writerOutput");
const editorOutput = document.getElementById("editorOutput");

generateBtn.addEventListener("click", async () => {
  const topic = topicInput.value.trim();

  errorBox.classList.add("hidden");
  errorBox.textContent = "";

  if (!topic) {
    errorBox.textContent = "Please enter a topic first.";
    errorBox.classList.remove("hidden");
    return;
  }

  generateBtn.disabled = true;
  loadingOverlay.classList.remove("hidden");
  resultsPanel.classList.add("hidden");
  logPanel.classList.add("hidden");

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: topic,
        content_type: contentTypeSelect.value,
        tone: toneSelect.value,
        length: lengthSelect.value,
      }),
    });

    const payload = await response.json();

    if (!response.ok || !payload.success) {
      throw new Error(payload.error || "Something went wrong.");
    }

    const data = payload.data;

    logContent.textContent = data.logs.join("\n");
    logPanel.classList.remove("hidden");

    researchOutput.textContent = data.research.raw_output;
    writerOutput.textContent = data.draft.raw_output;
    editorOutput.textContent = data.final.raw_output;

    resultsPanel.classList.remove("hidden");
  } catch (err) {
    errorBox.textContent = err.message || "Request failed.";
    errorBox.classList.remove("hidden");
  } finally {
    generateBtn.disabled = false;
    loadingOverlay.classList.add("hidden");
  }
});

topicInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    generateBtn.click();
  }
});
