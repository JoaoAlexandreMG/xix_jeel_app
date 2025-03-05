function showDiv(id) {
  // Hide all sections
  const sections = document.querySelectorAll("section");
  sections.forEach((section) => {
    section.classList.remove("active");
  });

  // Show the selected section
  const selectedSection = document.getElementById(id);
  if (selectedSection) {
    selectedSection.classList.add("active");
  }

  // Update active link
  const links = document.querySelectorAll(".menu-link");
  links.forEach((link) => {
    link.classList.remove("active");
  });
  const activeLink = document.querySelector(`a[href="#${id}"]`);
  if (activeLink) {
    activeLink.classList.add("active");
  }
}
function showEventDay(day) {
  const days = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"];
  days.forEach((d) => {
    const eventDay = document.getElementById(d);
    if (eventDay) {
      eventDay.classList.remove("active");
    }
  });
  const selectedEventDay = document.getElementById(day);
  if (selectedEventDay) {
    selectedEventDay.classList.add("active");
  }
  const eventDivs = document.querySelectorAll(".programacao_diaria");
  eventDivs.forEach((div) => {
    div.style.display = "none";
  });
  const selectedEventDiv = document.getElementById(`eventos_${day}`);
  if (selectedEventDiv) {
    selectedEventDiv.style.display = "block";
  }
}
