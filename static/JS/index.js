"use strict";

const mainContainer = document.querySelector("main");
const footer = document.querySelector("footer");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("search_btn");
const categoryList = document.getElementById("category_list");
// const index_card = document.querySelector(".index_card");

let nextPage, keyword, attractionId;
//初始化loading狀態為false，表示沒有正在載入中的資料
let isLoading = false;

const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.2,
};

const footerObserver = new IntersectionObserver(callback, options);
footerObserver.observe(footer);

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

//獲取景點資訊

const getAttractions = async (page) => {
  let url = `/api/attractions?page=${page}`;

  if (keyword) {
    url += `&keyword=${keyword}`;
  }
  try {
    isLoading = true;
    const response = await fetch(url);
    const result = await response.json();
    appendCards(result);
    nextPage = result.nextPage;
  } catch (error) {
    console.error("Error", error);
  } finally {
    isLoading = false;
  }
};

getAttractions(0);

const getAttractionCard = document.addEventListener("click", (event) => {
  const card = event.target.closest(".index_card");
  if (!card) return;

  const id = card.dataset.id;
  window.location.href = `/attraction/${id}`;
});

//網頁加載後立即獲取 categoryList
const getCategories = async () => {
  try {
    const response = await fetch("/api/categories");
    const result = await response.json();
    const categories = result.data.map((category) => {
      return ` <button>${category}</button>`;
    });
    categoryList.innerHTML = categories.join("");
  } catch (error) {
    console.error("Error", error);
  }
  categoryList.style.display = "none";
};

document.addEventListener("DOMContentLoaded", getCategories);

searchInput.addEventListener("click", () => {
  categoryList.style.display = "block";
});

//當點擊categoryList時將名稱添加到搜尋框中

categoryList.addEventListener("click", (event) => {
  if (event.target.tagName == "BUTTON") {
    searchInput.value = event.target.textContent;
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

searchBtn.addEventListener("click", () => {
  keyword = searchInput.value.trim();
  if (keyword == "") {
    return;
  }
  mainContainer.innerHTML = "";
  nextPage = 0;
  getAttractions("0");
});

function callback(entries) {
  const [entry] = entries;
  if (nextPage == null) {
    return;
  }
  if (!entry.isIntersecting && isLoading == false) {
    getAttractions(nextPage);
  }
}
