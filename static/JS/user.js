"use strict";

const overlay = document.querySelector(".overlay");
const btnCloseModel = document.querySelectorAll(".btn_close_model");
const btnOpenSignInFrom = document.querySelector(".nav_signin");
const signInFrom = document.querySelector(".model_signIn");
const registerFrom = document.querySelector(".model_register");
const registerLink = document.getElementById("turnToRegister");
const signInLink = document.getElementById("turnToSignIn");

//model
const turnToRegister = function (e) {
  e.preventDefault();
  signInFrom.classList.add("hidden");
  registerFrom.classList.remove("hidden");
};

const turnToSignIn = function (e) {
  e.preventDefault();
  registerFrom.classList.add("hidden");
  signInFrom.classList.remove("hidden");
};

const openSignInFrom = function (e) {
  e.preventDefault();
  signInFrom.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const closeModel = function () {
  signInFrom.classList.add("hidden");
  registerFrom.classList.add("hidden");
  overlay.classList.add("hidden");
};

registerLink.addEventListener("click", turnToRegister);
signInLink.addEventListener("click", turnToSignIn);
btnOpenSignInFrom.addEventListener("click", openSignInFrom);
btnCloseModel.forEach((btn) => btn.addEventListener("click", closeModel));
overlay.addEventListener("click", closeModel);

//會員狀態
fetch("/api/categories")
  .then((response) => response.json())
  .then((result) => {});
