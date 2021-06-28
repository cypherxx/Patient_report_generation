"use strict";
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

function update_data(name, value) {
  const data = JSON.parse(localStorage.getItem("form")) || {};
  data[name] = value;
  localStorage.setItem("form", JSON.stringify(data));
}

function raven(age) {
  const ravens_class = "ravens_test";
  const ravens_value = age >= 11 ? "Standard" : "Colour";
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
function digit_vocab(age) {
  const opts = $("#digit_vocab").querySelectorAll("div");
  if (age >= 11) {
    opts[0].classList.remove("hidden");
    opts[1].classList.add("hidden");
  } else {
    opts[0].classList.add("hidden");
    opts[1].classList.remove("hidden");
  }
  $$(".digit").forEach((ele) => {
    ele.textContent = age >= 11 ? "Digit Span" : "Vocabulary";
  });
}

function get_data (key) {
  return JSON.parse(localStorage.getItem('form'))[key]
}

window.addEventListener('DOMContentLoaded', () => {
  const pages = $$('main>section')
  const tabs = $$('.tab')
  let current = 0
  const backButton = $$('main>div button')[0]
  const nextButton = $$('main>div button')[1]
  const inputs = $$('main [name]')
  const data_inputs = $$('main [contenteditable]')
  const choices = $$('.test_choice')
  const test_sections = $$('.has_tests>.test')
  // Sattler Checkoboxes
  const checkboxes = $$("#sattler_table input[type=checkbox]");
  function finish(back = false) {
    const handler = back ? backButton : nextButton;
    const p = pages[current];
    if (p.classList.contains("has_tests")) {
      const visible_test = p.querySelector(".test:not(.hidden)");
      visible_test || handler.dispatchEvent(new Event("click"));
    }
    tabs.forEach((t, i) => {
      if (i < current) t.classList.add("finished");
      else t.classList.remove("finished");
    });
  }

  nextButton.addEventListener("click", () => {
    if (current === pages.length - 1) return;
    pages[current] && pages[current].classList.remove("open");
    tabs[current] && tabs[current].classList.remove("active");

    pages[current + 1] && pages[++current].classList.add("open");
    tabs[current] && tabs[current].classList.add("active");
    finish();
  });

  backButton.addEventListener("click", () => {
    if (current === 0) return;
    pages[current] && pages[current].classList.remove("open");
    tabs[current] && tabs[current].classList.remove("active");

    pages[current - 1] && pages[--current].classList.add("open");
    tabs[current] && tabs[current].classList.add("active");
    finish(true);
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
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      pages[current] && pages[current].classList.remove("open");
      tabs[current] && tabs[current].classList.remove("active");

      current = index;
      pages[current] && pages[current].classList.add("open");
      tabs[current] && tabs[current].classList.add("active");

      finish();
    });
  });

  $("[name=dob]").addEventListener("change", function () {
    if (!this.valueAsDate) return;
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
    update_data("age", year);
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
      const avg = Math.floor((sum / inputs.length) * 100) / 100;
      $(`.input__${name}_average`).textContent = avg;
      $(`.input__${name}_verbose`).textContent = getGrade(avg);
      const arr = Array.from(inputs).map((ele) => ele.value || 0);

      update_data(`${name}_average`, avg);
      update_data(name, arr);

      // Change total score
      const total_score =
        ((get_data("verbal_tests_average") || 0) +
          get_data("performance_tests_average") || 0) / 2;
      $(".full_score").textContent = total_score;
      update_data("full_score", total_score);
    }
    const inputs = table.querySelectorAll("input");
    const trackerTable = $(`.${name}_report`);
    const trackers =
      trackerTable && trackerTable.querySelectorAll("span:not(.digit)");
    inputs.forEach((input, index) => {
      input.addEventListener("change", () => {
        trackers &&
          trackers[index] &&
          (trackers[index].textContent = input.value);
        $(`.input__${name}_${index}`) &&
          $$(`.input__${name}_${index}`).forEach((i) => {
            i.textContent = getGrade(input.value);
          });
        populate();
      });
    });
  });

  let { tests: initial } = JSON.parse(localStorage.getItem("form"));
  initial = [false, false, false, false, false, false];
  update_data("tests", initial);
  test_sections.forEach((s, i) => {
    if (initial[i]) s.classList.remove("hidden");
    else s.classList.add("hidden");
  });
  choices.forEach((choice, index) => {
    choice.checked = initial[index];
    choice.addEventListener("change", function () {
      const { tests } = JSON.parse(localStorage.getItem("form"));
      tests[index] = choice.checked;
      if (choice.checked) test_sections[index].classList.remove("hidden");
      else test_sections[index].classList.add("hidden");
      update_data("tests", tests);
    });
  });

  // 7 rows, 5 columns
  const data = Array.from({ length: 7 }, () =>
    Array.from({ length: 5 }, () => false)
  );
  update_data("sattler_table", data);
  checkboxes.forEach((c, i) => {
    c.addEventListener("change", function () {
      data[Math.floor(i / 5)][i % 5] = c.checked;
      update_data("sattler_table", data);
    });
  });

  const newgender = $("#gender").value;

  if (newgender == "Male") {
    const x = $$(".input__heshe");
    const y = $$(".input__hisher");
    const z = $$(".input__boygirl");
    for (var i = 0; i < x.length; i++) {
      x[i].innerHTML = " he ";
    }
    for (var i = 0; i < y.length; i++) {
      y[i].innerHTML = " his ";
    }
    for (var i = 0; i < z.length; i++) {
      z[i].innerHTML = " boy ";
    }
  }

  $("#gender").addEventListener("change", () => {
    const newgender = $("#gender").value;
    if (newgender == "Female") {
      const x = $$(".input__heshe");
      const y = $$(".input__hisher");
      const z = $$(".input__boygirl");
      for (var i = 0; i < x.length; i++) {
        x[i].innerHTML = " she ";
      }
      for (var i = 0; i < y.length; i++) {
        y[i].innerHTML = " her ";
      }
      for (var i = 0; i < z.length; i++) {
        z[i].innerHTML = " girl ";
      }
    }
  });
  $("#submit").addEventListener("click", () => {
    const x = document.getElementById("submit").value;
    update_data("update_record", x);
    fetch("/get_report/", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        accept: "application/json",
      },

      body: localStorage.getItem("form"),
    })
      .then(() => {
        location.href = "/get_report/";
        const form = $("form.hidden");
        form.classList.remove("hidden");
        form.report_name.value = JSON.parse(localStorage.getItem("form")).name;
        localStorage.removeItem("form");
      })
      .catch((err) => {
        console.log("Recheck the form, ", err);
        location.href = "/get_report/";
      });
  });
  $("[name=dob]").dispatchEvent(new Event("change"));
});

