"use strict";

const attrs_img = document.querySelector(".attrs_img");
const attrs_name = document.querySelector(".attrs_name");
const attrs_inf = document.querySelector(".attrs_inf");
const attrs_description = document.querySelector(".attrs_description");
const attrs_address = document.querySelector(".attrs_address");
const attrs_transport = document.querySelector(".attrs_transport");
const attractionId = window.location.pathname.split("/")[2];
const morning = document.getElementById("booking_time_morning");
const price = document.getElementById("price");
const btnLeft = document.querySelector(".slide_btn_left");
const btnRight = document.querySelector(".slide_btn_right");
const dotContainer = document.querySelector(".dots");

//Slider
const slider = function () {
  const slides = document.querySelectorAll(".slide");
  let curslide = 0;
  const maxSlide = slides.length - 1;
  //functions
  const goToSlide = function (slide) {
    slides.forEach(
      (s, i) => (s.style.transform = `translateX(${100 * (i - slide)}%)`)
    );
  };

  const nextSlide = function () {
    if (curslide === maxSlide) {
      curslide = 0;
    } else {
      curslide++;
    }
    goToSlide(curslide);
    activateDot(curslide);
  };
  const preSlide = function () {
    if (curslide === 0) {
      curslide = maxSlide;
    } else {
      curslide--;
    }
    goToSlide(curslide);
    activateDot(curslide);
  };

  const createDots = function () {
    slides.forEach(function (_, i) {
      dotContainer.insertAdjacentHTML(
        "beforeend",
        `<button class="dots_dot" data-slide="${i}"></button>`
      );
    });
  };

  const activateDot = function (slide) {
    document
      .querySelectorAll(".dots_dot")
      .forEach((dot) => dot.classList.remove("dots_dot--active"));
    document
      .querySelector(`.dots_dot[data-slide="${slide}"]`)
      .classList.add("dots_dot--active");
  };

  const init = function () {
    goToSlide(0);
    createDots();
    activateDot(0);
  };
  init();

  //Event handlers
  btnRight.addEventListener("click", nextSlide);
  btnLeft.addEventListener("click", preSlide);

  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") preSlide();
    e.key === "ArrowRight" && nextSlide();
  });

  dotContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("dots_dot")) {
      const { slide } = e.target.dataset;
      goToSlide(slide);
      activateDot(slide);
    }
  });
};

const getAttractionsId = () => {
  fetch(`/api/attraction/${attractionId}`)
    .then((respose) => respose.json())
    .then((result) => {
      let attraction = result.data;
      const name = attraction.name;
      const mrt = attraction.mrt;
      const cat = attraction.category;
      const description = attraction.description;
      const address = attraction.address;
      const transport = attraction.transport;
      const images = attraction.images;
      images.forEach((image, i) => {
        let div = document.createElement("div");
        div.classList.add("slide");
        div.style.backgroundImage = `url(${image})`;
        div.style.transform = `translateX(${100 * i}%)`;
        attrs_img.appendChild(div);
      });
      attrs_name.textContent = name;
      attrs_inf.textContent = cat + " at " + mrt;
      attrs_description.textContent = description;
      attrs_address.textContent = address;
      attrs_transport.textContent = transport;
      slider();
    })
    .catch((error) => console.error("Error", error));
};
getAttractionsId();

function updatePrice() {
  if (morning.checked) {
    price.innerText = "新台幣2000元";
  } else {
    price.innerText = "新台幣2500元";
  }
}
