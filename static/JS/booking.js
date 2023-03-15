"use strict";

// const btnOpenBookingPage = document.getElementById("nav_booking");
const btnOpenBookingPage = document.querySelector(".nav_booking");
const signInModel = document.getElementById("model_signIn");

//定義取得cookie的函數;
function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

const openSignInFrom = function () {
  signInModel.classList.add("show");
  overlay.classList.add("show");
};

btnOpenBookingPage.addEventListener("click", (event) => {
  //   const token = getCookie("access_token");
  //   if (!token) {
  //     openSignInFrom();
  //   } else {
  const OpenBookingPage = event.target.closest(".nav_booking");
  if (!OpenBookingPage) return;
  window.location.href = `/booking`;
  //   }
});
