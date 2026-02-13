const startBtn = document.getElementById("startBtn");
const statusElement = document.getElementById("status");
const frame = document.getElementById("frame");
const openLink = document.getElementById("openLink");

startBtn.addEventListener("click", async () => {
  statusElement.textContent = "Creating session...";
  frame.src = "";
  openLink.style.display = "none";

  try {
    const response = await fetch("/start", { method: "POST" });
    const data = await response.json();

    if (data.error) {
      statusElement.textContent = "Error: " + data.error;
      return;
    }

    statusElement.textContent = "Session ready.";
    frame.src = data.conversation_url;

    openLink.href = data.conversation_url;
    openLink.style.display = "inline";
    
  } catch (err) {
    statusElement.textContent = "Unexpected error.";
  }
});
