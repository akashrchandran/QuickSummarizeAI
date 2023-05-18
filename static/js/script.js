const toggler = document.getElementById("toggler");
const ytlink = document.getElementById("ytform");
const submitbtn = document.getElementById("submitbtn");
const summary = document.getElementById("summary");
const YTRegex = `^(?:https?://|//)?(?:www\\.|m\\.|.+\\.)?(?:youtu\\.be/|youtube\\.com/(?:embed/|v/|shorts/|feeds/api/videos/|watch\\?v=|watch\\?.+&v=))([\\w-]{11})(?![\\w-])`;

if (halfmoon.getPreferredMode() == "light-mode") {
  // Light mode is preferred
  toggler.classList.remove("toggled");
} else if (halfmoon.getPreferredMode() == "dark-mode") {
  // Dark mode is preferred
  toggler.classList.add("toggled");
} else if (halfmoon.darkModeOn) {
  toggler.classList.add("toggled");
}

toggler.addEventListener("click", () => {
  toggler.classList.toggle("toggled");
  halfmoon.toggleDarkMode();
});

ytlink.addEventListener("submit", (e) => {
  e.preventDefault();
  submitbtn.disabled = true;
  submitbtn.innerHTML = '<i class="fa fa-spinner fa-pulse fa-lg fa-fw"></i>';
  getSummary();
});

function toastWaitAlert() {
  halfmoon.initStickyAlert({
    content: "Please wait while we generate the summary...",
    title: "Process started alert",
    alertType: "alert-secondary",
    timeShown: 2000,
  });
}

function toastErrorAlert(error) {
  halfmoon.initStickyAlert({
    content: "Some error occured while processing: " + error,
    title: "Error alert",
    alertType: "alert-danger",
    timeShown: 5000,
  });
}

function toastSuccessAlert(error) {
  halfmoon.initStickyAlert({
    content: "Successfully generated summary",
    title: "Success alert",
    alertType: "alert-success",
    timeShown: 5000,
  });
}

async function getSummary() {
  let ytlink = document.getElementById("ytlink").value;
  let video_id = ytlink.match(YTRegex);
  if (video_id) {
    video_id = video_id[1];
  } else {
    toastErrorAlert("Invalid Youtube link");
    submitbtn.disabled = false;
    submitbtn.innerHTML = "Submit";
    return;
  }
  toastWaitAlert();
  const response = await fetch("/api/summary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ video_id: video_id }),
  });
  if (!response.ok) {
    const msg = await response.json();
    toastErrorAlert(msg.message);
    submitbtn.disabled = false;
    submitbtn.innerHTML = "Submit";
    return;
  }
  const data = await response.text();
  summary.innerHTML = data;
  toastSuccessAlert();
  submitbtn.disabled = false;
  submitbtn.innerHTML = "Submit";
}
