"use strict";
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

function update_data(name, value) {
  const data = JSON.parse(localStorage.getItem("form")) || {};
  data[name] = value;
  localStorage.setItem("form", JSON.stringify(data));
}

function replace_initials(element) {
  $$(".input__" + element.name).forEach((e) => (e.textContent = element.value));
  $$(".input__" + element.name + "_initial").forEach(
    (e) => (e.textContent = element.value[0])
  );
  update_data(element.name, element.value);
}
function save() {
  update_data(this.name || this.dataset.name, this.value || this.textContent);
  document
    .querySelectorAll(".input__" + this.name || this.dataset.name)
    .forEach((a) => {
      a.textContent = this.value || this.textContent;
    });
}
function getGrade(num) {
  return num >= 90 && num <= 110 ? "Average" : "Borderline";
}

window.addEventListener("DOMContentLoaded", () => {
  const pages = $$("main>section");
  const tabs = $$(".tab");
  let current = 0;
  const backButton = $$("main>div button")[0];
  const nextButton = $$("main>div button")[1];
  const inputs = $$("main [name]");
  const data_inputs = $$("main [contenteditable]");

  nextButton.addEventListener("click", () => {
    if (current === pages.length - 1) return;
    pages[current] && pages[current].classList.remove("open");
    tabs[current] && tabs[current].classList.remove("active");

    pages[current + 1] && pages[++current].classList.add("open");
    tabs[current] && tabs[current].classList.add("active");
  });

  backButton.addEventListener("click", () => {
    if (current === 0) return;
    pages[current] && pages[current].classList.remove("open");
    tabs[current] && tabs[current].classList.remove("active");

    pages[current - 1] && pages[--current].classList.add("open");
    tabs[current] && tabs[current].classList.add("active");
  });

  inputs.forEach((input) => {
    update_data(input.name, input.value);
    input.addEventListener("change", save);
  });

  data_inputs.forEach((input) =>
    update_data(
      input.name || input.dataset.name,
      input.value || input.textContent
    )
  );
  data_inputs.forEach((input) => input.addEventListener("input", save));

  $("[name=dob]").addEventListener("change", function () {
    // console.log('')
    const today = new Date();
    let year = today.getFullYear() - this.valueAsDate.getFullYear();
    let month = today.getMonth() - this.valueAsDate.getMonth();
    if (month < 0) {
      month = month + 12;
      year--;
    }
    $$(".input__month").forEach((ele) => (ele.textContent = month));
    $$(".input__year").forEach((ele) => (ele.textContent = year));
    update_data("year", year);
    update_data("month", month);
  });

  $$("table[data-name]").forEach((table) => {
    const name = table.dataset.name;
    function populate() {
      const sum = Array.from(inputs).reduce(
        (sum, r) => sum + parseFloat(r.value || 0),
        0
      );
      $(`.input__${name}_average`).textContent =
        Math.floor((sum / inputs.length) * 100) / 100;
      const arr = Array.from(inputs).map((ele) => ele.value || 0);
      update_data(name, arr);
    }
    const inputs = table.querySelectorAll("input");
    const trackerTable = $(`.${name}_report`);
    const trackers = trackerTable && trackerTable.querySelectorAll(`span`);
    inputs.forEach((input, index) => {
      input.addEventListener("change", () => {
        trackers &&
          trackers[index] &&
          (trackers[index].textContent = input.value);
        $(`.input__${name}_${index}`) &&
          ($(`.input__${name}_${index}`).textContent = getGrade(input.value));
        populate();
      });
    });
  });
  $("#submit").addEventListener("click", () => {
    // const form = new FormData();
    // const data = localStorage.getItem('form');

    // for(const key in data) form.append(key, data[key]);

    fetch("/get_report/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accept: "application/json",
      },
      body: localStorage.getItem("form"),
    })
      .then(() => {
        // localStorage.removeItem('form')
        location.href = "/get_report/";
        const form = $("form.hidden");
        form.classList.remove("hidden");
        form.report_name.value = JSON.parse(localStorage.getItem("form"))[
          "name"
        ];
        localStorage.removeItem("form");
      })
      .catch((err) => {
        console.log("Recheck the form, ", err);
        location.href = "/";
      });
  });
});
