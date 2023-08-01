document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      // e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }


  // -------------------------------------- Moja część kodu ---------------------------------------------------------

  // deklaracja listy gdzie będą przetrzymywane id kategorii, które zaznaczy użytkownik
  const categoriesList = [];

  // Pobranie wszystkich kategorii z html (Inputy mają value = category.id)
  const categories = document.querySelectorAll("input[name='categories']");

  // Pobranie wszystkich instytucji z html (Inputy mają value = institution.id)
  const institutions = document.querySelectorAll("input[name='organization']");

  // Ukrycie wszystkich instytucji na start - bo nie zaznaczono żadnych kategorii jeszcze
  for (let institution of institutions) {
  institution.parentElement.parentElement.style.display = 'block';
  }

  function checkCategoryInInstitution() {
    for (let institution of institutions) {

      // Licznik zwiększający swoją wartość jeśli szukana kategoria nie jest akceptowana przez instytucję
      let counter = 0;

      // Pobranie kategorii, które akceptuje dana instytucja (pobrane z html - wcześniej z ctx)
      let institutionCategoryNumbers = institution.nextElementSibling.nextElementSibling.firstElementChild.nextElementSibling.innerText

      // Sprawdzenie czy kategoria jest akceptowana przez instytucję - pętla dla wszystkich instytucji
      for (let element of categoriesList) {
        if (!institutionCategoryNumbers.includes(element)) {
          counter += 1;
        } else {
        }
      }
      if (counter != 0) {
        // Jeśli counter większy od 0 to ukrywamy instytucję
        institution.parentElement.parentElement.style.display = 'none';

      } else {
        // w przeciwnym wypadku pokazujemy instytucję
        institution.parentElement.parentElement.style.display = 'block';
      }
    }
  }

 // Dodanie eventu tworzącego listę z wybranymi przez użytkownika kategoriami
  for (let category of categories) {
    category.addEventListener('change', function () {
      // Pobranie id kategorii
      const catvalue = this.value;

      // Jeśli zaznaczono kategorię
      if (this.checked) {
        categoriesList.push(catvalue); // Lista kategorii zwiększona o id wybranej kategorii
        console.log(categoriesList);

        // Sprawdzenie i filtrowanie Instytucji
        checkCategoryInInstitution();

      // Jeśli odznaczono kategorię
      } else {
        const arr = categoriesList.filter(function (number) {
          return number !== catvalue;
        }); // Usunięcie kategorii z listy - stworzenie nowej listy bez danego id

        categoriesList.length = 0; // Wyzerowanie starej listy
        categoriesList.push(...arr); // Uzupełnienie listy starej o nową (bez odznaczonej kategorii)
        console.log(categoriesList);

        // Sprawdzenie i filtrowanie Instytucji
        checkCategoryInInstitution();
      }
    });
  }

  // Deklaracja zmiennych dla wybranej instytucji
  let chosenInstitutionId = null;
  let chosenInstitutionName = null;

  // Pobranie z formularza instytucji (event na klik)
  for (let institution of institutions) {
    institution.addEventListener('change', function () {
      if (this.checked) {
        chosenInstitutionId = this.value;
        chosenInstitutionName = institution.nextElementSibling.nextElementSibling.firstElementChild.innerText;
      } else {
        chosenInstitutionId = null;
        chosenInstitutionName = null;
      }
    });
  }


    // Pobranie listy wszystkich kategorii - elementy listy to para (lista) danych - id i name - nie używane w kodzie
    const fullCategoriesList = []
    for (let category of categories) {
      let el = [category.value, category.nextElementSibling.nextElementSibling.innerText]
      fullCategoriesList.push(el);
    }


  // Event dla przycisku "dalej" (dodano id="summary") do podsumowania
  summaryButton = document.querySelector("#summary");
  summaryButton.addEventListener("click", function () {

    // Pobranie elementów z formularza (poza kategoriami i instytucją) i nadpisanie na stronie html
    let address = document.querySelector("input[name='address']").value;
    let city = document.querySelector("input[name='city']").value;
    let postcode = document.querySelector("input[name='postcode']").value;
    let phone = document.querySelector("input[name='phone']").value;
    let date = document.querySelector("input[name='data']").value;
    let time = document.querySelector("input[name='time']").value;
    let moreInfo = document.querySelector("textarea[name='more_info']").value;
    let bags = document.querySelector("input[name='bags']").value;

    const summaryBag = document.querySelector(".icon-bag").nextElementSibling;
    summaryBag.innerText = bags + " worków w dobrym stanie";

    const summaryInstitution = document.querySelector(".icon-hand").nextElementSibling;
    summaryInstitution.innerText = "Dla fundacji: " + chosenInstitutionName;

    const summaryAddressInfo = document.querySelector("#address li");
    summaryAddressInfo.innerText = address;
    summaryAddressInfo.nextElementSibling.innerText = city;
    summaryAddressInfo.nextElementSibling.nextElementSibling.innerText = postcode;
    summaryAddressInfo.nextElementSibling.nextElementSibling.nextElementSibling.innerText = phone;

    const receiptDate = document.querySelector("#receiptDate li");
    receiptDate.innerText = date;
    receiptDate.nextElementSibling.innerText = time;
    receiptDate.nextElementSibling.nextElementSibling.innerText = moreInfo;

  });
});
