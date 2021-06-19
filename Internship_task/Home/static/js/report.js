"use strict";
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

function update_data(name, value) {
  const data = JSON.parse(localStorage.getItem("form")) || {};
  data[name] = value;
  localStorage.setItem("form", JSON.stringify(data));
}

function raven(age) {
  const ravens_class = 'ravens_test';
  const ravens_value = age>=11?"Standard":"Colour";
  $$(".input__" + ravens_class).forEach((e) => (e.textContent = ravens_value));
  $$(".input__" + ravens_class + "_initial").forEach(
    (e) => (e.textContent = ravens_value[0])
  );
  update_data(ravens_class, ravens_value);
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
function digit_vocab(age){
  $$('.digit').forEach(ele=>{
    ele.textContent = age>=11?"Digit Span":"Vocabulary";
  })
}

function get_data(key){
  return JSON.parse(localStorage.getItem('form'))[key];
}

window.addEventListener("DOMContentLoaded", () => {
  const pages = $$("main>section");
  const tabs = $$(".tab");
  let current = 0;
  const backButton = $$("main>div button")[0];
  const nextButton = $$("main>div button")[1];
  const inputs = $$("main [name]");
  const data_inputs = $$("main [contenteditable]");
  const choices = $$(".test_choice");

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

  // Development - Move when tab is clicked
  tabs.forEach((tab, index)=>{

    tab.addEventListener('click', ()=>{
      pages[current] && pages[current].classList.remove("open");
      tabs[current] && tabs[current].classList.remove("active");

      current = index;
      pages[current] && pages[current].classList.add("open");
      tabs[current] && tabs[current].classList.add("active");
    })
  })

  $("[name=dob]").addEventListener("change", function () {
    const today = new Date();
    let year = today.getFullYear() - this.valueAsDate.getFullYear();
    let month = today.getMonth() - this.valueAsDate.getMonth();
    if (month < 0) {
      month = month + 12;
      year--;
    }
    $$(".input__month").forEach((ele) => (ele.textContent = month));
    $$(".input__year").forEach((ele) => (ele.textContent = year));
    $("[name=age]").value = year;
    update_data('age', year);
    update_data("year", year);
    update_data("month", month);

    raven(year);
    digit_vocab(year);
  });

  $$("table[data-name]").forEach((table) => {
    const name = table.dataset.name;
    function populate() {
      const sum = Array.from(inputs).reduce(
        (sum, r) => sum + parseFloat(r.value || 0),
        0
      );
      const avg =
        Math.floor((sum / inputs.length) * 100) / 100;
      $(`.input__${name}_average`).textContent = avg;
      $(`.input__${name}_verbose`).textContent = getGrade(avg);
      const arr = Array.from(inputs).map((ele) => ele.value || 0);

      update_data(`${name}_average`, avg);
      update_data(name, arr);

      // Change total score
      const total_score = (get_data('verbal_tests_average')|| 0 + get_data('performance_tests_average') || 0)/2;
      $('.full_score').textContent = total_score;
      update_data('full_score', total_score)
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

  choices.forEach((choice, index)=>{
    update_data('tests', [false, false, false, false, false, false]);
    choice.addEventListener('change', function(){
      const {tests} = JSON.parse(localStorage.getItem('form'));
      tests[index] = choice.checked;
      update_data('tests', tests);
      pages[index] && pages[index].classList.toggle('hidden');
    })
  })

  $("#submit").addEventListener("click", () => {

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
