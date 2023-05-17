const toggler = document.getElementById('toggler');
const ytlink = document.getElementById('ytform');
const submitbtn = document.getElementById('submitbtn');
const YTRegex = `^(?:https?://|//)?(?:www\\.|m\\.|.+\\.)?(?:youtu\\.be/|youtube\\.com/(?:embed/|v/|shorts/|feeds/api/videos/|watch\\?v=|watch\\?.+&v=))([\\w-]{11})(?![\\w-])`

toggler.addEventListener('click', () => {
    toggler.classList.toggle('toggled');
    halfmoon.toggleDarkMode();
});

ytlink.addEventListener('submit', (e) => {
    e.preventDefault();
    submitbtn.disabled = true;
    submitbtn.innerHTML = '<i class="fa fa-spinner fa-pulse fa-lg fa-fw"></i>';
    toastWaitAlert();
    getSummary();
});

function toastWaitAlert() {
    halfmoon.initStickyAlert({
      content: "Please wait while we generate the summary...",
      title: "Process started alert",
      alertType: "alert-secondary",
      timeShown: 10000,
    });
  }

async function getSummary() {
    let ytlink = document.getElementById('ytlink').value;
    console.log(ytlink);
    let video_id = ytlink.match(YTRegex)[1];
    const response = await fetch('/api/summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_id: video_id })
    });

    const data = await response.json();
    console.log(data);
    // return data;
}