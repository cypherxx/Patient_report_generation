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
  if (num >= 130) return "Very Superior";
  else if (num >= 120 && num <= 129) return "Superior";
  else if (num >= 110 && num <= 119) return "Above average";
  else if (num >= 85 && num <= 109) return "Average";
  else if (num >= 70 && num <= 84) return "Borderline";
  else if (num >= 50 && num <= 69) return "Mild Intellectual Disability";
  else if (num >= 35 && num <= 49) return "Moderate";
  else if (num >= 20 && num <= 34) return "Severe";
  else return "Profound";
}
function digit_vocab() {
  const opts = $("#digit_vocab").querySelectorAll("div");
  if (this.value == 0) {
    opts[0].classList.remove("hidden");
    opts[1].classList.add("hidden");
  } else {
    opts[0].classList.add("hidden");
    opts[1].classList.remove("hidden");
  }
  $$(".digit").forEach((ele) => {
    ele.textContent = this.value == 0 ? "Digit Span" : "Vocabulary";
  });

  update_data("digit_vocab", this.value);
}

function get_data(key) {
  return JSON.parse(localStorage.getItem("form"))[key];
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
  const recommended = $$(".recomendate");
  const test_sections = $$(".has_tests>.test");
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
    input.dispatchEvent(new Event("change"));
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
  });
  $("[name=dob]").dispatchEvent(new Event("change"));

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
        (get_data("verbal_tests_average") ||
          0 + get_data("performance_tests_average") ||
          0) / 2;
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
      input.dispatchEvent(new Event("change"));
    });
  });
  let arr = [];
  choices.forEach((choice) => {
    arr.push(choice.checked);
  });
  update_data("tests", arr);
  choices.forEach((choice, index) => {
    if (choice.checked) test_sections[index].classList.remove("hidden");
    else test_sections[index].classList.add("hidden");
    choice.addEventListener("change", function () {
      const { tests } = JSON.parse(localStorage.getItem("form"));
      tests[index] = choice.checked;
      if (choice.checked) test_sections[index].classList.remove("hidden");
      else test_sections[index].classList.add("hidden");
      update_data("tests", tests);
    });
  });

  const recommended_initial = Array.from({ length: 12 }, () => false);
  //update_data("recommendations", recommended_initial);
  recommended.forEach((item, i) => {
    recommended_initial[i] = item.checked;
    item.addEventListener("change", function () {
      //const re = get_data("recommendations");
      recommended_initial[i] = item.checked;
      update_data("recommendations", recommended_initial);
    });
  });

  update_data("recommendations", recommended_initial);
  // 7 rows, 5 columns
  const data = Array.from({ length: 7 }, () =>
    Array.from({ length: 5 }, () => false)
  );
  // update_data('sattler_table', data)
  checkboxes.forEach((c, i) => {
    data[Math.floor(i / 5)][i % 5] = c.checked;
    c.addEventListener("change", function () {
      data[Math.floor(i / 5)][i % 5] = c.checked;
      update_data("sattler_table", data);
    });
  });
  update_data("sattler_table", data);
  const newgender = $("#gender").value;

  if (newgender == "Male") {
    const x = $$(".input__heshe");
    const y = $$(".input__hisher");
    const z = $$(".input__boygirl");
    const p = $$(".input__himher");
    for (var i = 0; i < x.length; i++) {
      x[i].innerHTML = " he ";
    }
    for (var i = 0; i < y.length; i++) {
      y[i].innerHTML = " his ";
    }
    for (var i = 0; i < z.length; i++) {
      z[i].innerHTML = " boy ";
    }
    for (var i = 0; i < p.length; i++) {
      p[i].innerHTML = " him ";
    }
  } else {
    const x = $$(".input__heshe");
    const y = $$(".input__hisher");
    const z = $$(".input__boygirl");
    const p = $$(".input__himher");
    for (var i = 0; i < x.length; i++) {
      x[i].innerHTML = " she ";
    }
    for (var i = 0; i < y.length; i++) {
      y[i].innerHTML = " her ";
    }
    for (var i = 0; i < z.length; i++) {
      z[i].innerHTML = " girl ";
    }
    for (var i = 0; i < p.length; i++) {
      p[i].innerHTML = " her ";
    }
  }

  $("#gender").addEventListener("change", () => {
    const newgender = $("#gender").value;
    if (newgender == "Female") {
      const x = $$(".input__heshe");
      const y = $$(".input__hisher");
      const z = $$(".input__boygirl");
      const p = $$(".input__himher");
      for (var i = 0; i < x.length; i++) {
        x[i].innerHTML = " she ";
      }
      for (var i = 0; i < y.length; i++) {
        y[i].innerHTML = " her ";
      }
      for (var i = 0; i < z.length; i++) {
        z[i].innerHTML = " girl ";
      }
      for (var i = 0; i < p.length; i++) {
        p[i].innerHTML = " her ";
      }
    } else {
      const x = $$(".input__heshe");
      const y = $$(".input__hisher");
      const z = $$(".input__boygirl");
      const p = $$(".input__himher");
      for (var i = 0; i < x.length; i++) {
        x[i].innerHTML = " he ";
      }
      for (var i = 0; i < y.length; i++) {
        y[i].innerHTML = " his ";
      }
      for (var i = 0; i < z.length; i++) {
        z[i].innerHTML = " boy ";
      }
      for (var i = 0; i < p.length; i++) {
        p[i].innerHTML = " him ";
      }
    }
  });
  $("#digit").addEventListener("change", digit_vocab);
  $("#submit").addEventListener("click", () => {
    let x = document.getElementById("submit").value;
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
        localStorage.removeItem("form");
      })
      .catch((err) => {
        localStorage.removeItem("form");
        console.log("Recheck the form, ", err);
        location.href = "/get_report/";
      });
  });
  $("[name=dob]").dispatchEvent(new Event("change"));
  $("#digit").dispatchEvent(new Event("change"));
});
