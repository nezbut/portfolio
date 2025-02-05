async function fetchGithubInfo() {
  try {
    const response = await fetch("/api/github");
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

function updatePage(data) {
  if (!data) {
    return;
  }
  document.getElementById("repos").textContent = data.public_repos ?? "-";
  document.getElementById("followers").textContent = data.followers ?? "-";
  document.getElementById("following").textContent = data.following ?? "-";
}

window.addEventListener("DOMContentLoaded", async () => {
  const githubData = await fetchGithubInfo();
  updatePage(githubData);
});
