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

const getAttractionsId = () => {
  fetch(`/api/attraction/${attractionId}`)
    .then((respose) => respose.json())
    .then((result) => {
      const attraction = result.data;
      const name = attraction.name;
      const mrt = attraction.mrt;
      const cat = attraction.category;
      const description = attraction.description;
      const address = attraction.address;
      const transport = attraction.transport;
      const images = attraction.images[0];
      console.log(attraction);
      attrs_img.style.backgroundImage = `url(${images})`;
      attrs_name.textContent = name;
      attrs_inf.textContent = cat + " at " + mrt;
      attrs_description.textContent = description;
      attrs_address.textContent = address;
      attrs_transport.textContent = transport;
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
