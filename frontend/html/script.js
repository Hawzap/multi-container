const API_URL = "/api/users";

const statusElement = document.getElementById("status");
const tableBody = document.querySelector("#users-table tbody");
const refreshButton = document.getElementById("refresh");

function createRow(user) {
  const row = document.createElement("tr");
  for (const value of [user.id, user.name, user.email]) {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.append(cell);
  }
  return row;
}

function renderUsers(users) {
  tableBody.replaceChildren(...users.map(createRow));
}

async function loadUsers() {
  statusElement.textContent = "Завантаження...";
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const users = await response.json();
    renderUsers(users);
    statusElement.textContent = `Користувачів: ${users.length}`;
  } catch (error) {
    tableBody.replaceChildren();
    statusElement.textContent = `Не вдалося отримати дані: ${error.message}`;
  }
}

refreshButton.addEventListener("click", loadUsers);
loadUsers();
