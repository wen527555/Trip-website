"use strict";

const mainContainer = document.querySelector("main");
const footer = document.querySelector("footer");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("search_btn");
const categoryList = document.getElementById("category_list");
const index_card = document.querySelector(".index_card");

let nextPage, keyword, attractionId;
//初始化loading狀態為false，表示沒有正在載入中的資料
let isLoading = false;

//網頁加載後立即獲取特定景點資訊
const getAttractionsId = (attractionId) => {
  fetch(`/attraction/${attractionId}`)
    .then((respose) => respose.json())
    .then((result) => {
      const attraction = result.data;
      //   const name = attraction.name;
      //   const mrt = attraction.mrt;
      //   const cat = attraction.category;
      //   const description = attraction.description;
      //   const address = attraction.address;
      //   const transport = attraction.transport;
      //   const images = attraction.images[0];
      console.log(attraction);
      //   console.log(name, mrt);
    })
    .catch((error) => console.error("Error", error));
};
getAttractionsId();

//網頁加載後立即獲取 categoryList
const getCategories = () => {
  fetch("/api/categories")
    .then((response) => response.json())
    .then((result) => {
      const categories = result.data.map((category) => {
        return ` <button>${category}</button>`;
      });
      categoryList.innerHTML = categories.join("");
    })
    .catch((error) => console.error("Error", error));
  categoryList.style.display = "none";
};

document.addEventListener("DOMContentLoaded", getCategories);

searchInput.addEventListener("click", () => {
  categoryList.style.display = "block";
});

//當點擊categoryList時將名稱添加到搜尋框中，並隱藏

categoryList.addEventListener("click", (event) => {
  if (event.target.tagName == "BUTTON") {
    searchInput.value = event.target.textContent;
    categoryList.style.display = "none";
  }
});

document.addEventListener("click", (event) => {
  if (
    !categoryList.contains(event.target) &&
    !searchInput.contains(event.target)
  ) {
    categoryList.style.display = "none";
  }
});

//獲取景點資訊

function getAttractions(page) {
  let url = `/api/attractions?page=${page}`;

  if (keyword) {
    url += `&keyword=${keyword}`;
  }
  isLoading = true;
  fetch(url)
    .then((response) => response.json())
    .then((result) => {
      appendCards(result);
      nextPage = result.nextPage;
    })
    .catch((error) => console.error("Error", error))
    .finally(() => {
      isLoading = false;
    });
}

getAttractions("0");

function appendCards(result) {
  let attractions = result.data;
  if (attractions == "") {
    mainContainer.innerHTML = "無搜尋結果";
  }
  attractions.forEach((attraction) => {
    let name = attraction.name;
    let mrt = attraction.mrt;
    let cat = attraction.category;
    let images = attraction.images[0];
    let id = attraction.id;

    let cards = `<div class="index_card" data-ID="${id}">
   <div class="index_img" style="background-image: url('${images}')"></div>
   <div class="index_name">${name}</div>
   <div class="index_inf">
     <div class="index_mrt">${mrt}</div>
     <div class="index_cat">${cat}</div>
   </div>
 </div> `;
    mainContainer.insertAdjacentHTML("beforeend", cards);
  });
  nextPage = result.nextPage;
  isLoading = false;
}

document.addEventListener("click", (event) => {
  const card = event.target.closest(".index_card");
  if (!card) return;

  const id = card.dataset.id;
  window.location.href = `/attraction/${id}`;
});

searchBtn.addEventListener("click", () => {
  keyword = searchInput.value.trim();
  if (keyword == "") {
    return;
  }
  mainContainer.innerHTML = "";
  nextPage = 0;
  //   getAttractionsKeyword("0", keyword);
  getAttractions("0");
});

function callback() {
  if (nextPage == null) {
    return;
  }
  if (isLoading == false) {
    getAttractions(nextPage);
  }
}

const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.5,
};

const observer = new IntersectionObserver(callback, options);

observer.observe(footer);
