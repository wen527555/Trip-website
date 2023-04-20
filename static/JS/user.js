"use strict";

const overlay = document.querySelector(".overlay");
const btnBookingPage = document.getElementById("nav_booking");
const btnCloseModel = document.querySelectorAll(".btn_close_model");
const btnOpenSignInFrom = document.getElementById("nav_signin");
const btnSignOut = document.getElementById("nav_register");
const signInModel = document.getElementById("model_signIn");
const registerModel = document.querySelector(".model_register");
const registerLink = document.getElementById("showRegisterForm");
const signInLink = document.getElementById("showLogInForm");

const logIn_email = document.getElementById("logIn_email");
const logIn_password = document.getElementById("logIn_password");

const register_email = document.getElementById("register_email");
const register_password = document.getElementById("register_password");
const register_name = document.getElementById("register_name");
const btnMenu = document.getElementById("nav_menu");
const menuList = document.querySelector(".menuList");

const token = getCookie("access_token");
const nav_booking = btnBookingPage.addEventListener("click", () => {
  if (!token) {
    openSignInFrom();
  } else {
    window.location.href = `/booking`;
  }
});

//model
const turnToRegister = function () {
  signInModel.classList.remove("show");
  registerModel.classList.add("show");
  clear_all();
};

const turnToSignIn = function () {
  registerModel.classList.remove("show");
  signInModel.classList.add("show");
  clear_all();
};

const closeModel = function () {
  signInModel.classList.remove("show");
  registerModel.classList.remove("show");
  overlay.classList.remove("show");
  menuList.style.display = "none";
  clear_all();
};

const openSignInFrom = function () {
  signInModel.classList.add("show");
  overlay.classList.add("show");
};

const openMenu = function () {
  menuList.style.display = "block";
  overlay.classList.add("show");
};

function clear_all() {
  register_name.value = "";
  register_email.value = "";
  register_password.value = "";
  logIn_email.value = "";
  logIn_password.value = "";
  signInMsg.value = "";
  registerMsg.value = "";
  registerMsg.style.display = "none";
  hasMsg = false;
}

registerLink.addEventListener("click", turnToRegister);
signInLink.addEventListener("click", turnToSignIn);
btnCloseModel.forEach((btn) => btn.addEventListener("click", closeModel));
overlay.addEventListener("click", closeModel);
btnOpenSignInFrom.addEventListener("click", openSignInFrom);
btnMenu.addEventListener("click", openMenu);

const registerBtn = document.getElementById("register_button");
const registerMsg = document.querySelector(".registerMsg");
let hasMsg = false;

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

//會員狀態
async function getCurrentUser() {
  if (!token) {
    btnMenu.style.display = "none";
    btnOpenSignInFrom.style.display = "block";
  }
  try {
    const response = await fetch(`/api/user/auth`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    if (data["data"] != null) {
      btnMenu.style.display = "block";
      btnOpenSignInFrom.style.display = "none";
    } else {
      btnMenu.style.display = "none";
      btnOpenSignInFrom.style.display = "block";
    }
  } catch (error) {
    // console.log(error);
    console.log("API呼叫失敗:" + error.message);
  }
}

document.addEventListener("DOMContentLoaded", getCurrentUser);

//會員註冊驗證
async function registerSystem() {
  const emailRegex = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
  const nameRegex = /^[\u4E00-\u9FA5a-zA-Z]{2,10}$/;
  const passwordPegex = /^(?=.*[A-Z]).{8,15}$/;
  if (register_email.value !== "" && !emailRegex.test(register_email.value)) {
    registerMsg.style.display = "block";
    registerMsg.textContent = "信箱格式錯誤，請重新輸入";
    hasMsg = true;
  } else if (
    register_name.value !== "" &&
    !nameRegex.test(register_name.value)
  ) {
    registerMsg.style.display = "block";
    registerMsg.textContent = "姓名格式須包含2~10個中文或英文字";
    hasMsg = true;
  } else if (
    register_password.value !== "" &&
    !passwordPegex.test(register_password.value)
  ) {
    registerMsg.style.display = "block";
    registerMsg.textContent = "密碼格式至少為8個字且需含一個大寫英文字母";
    hasMsg = true;
  } else {
    try {
      const response = await fetch(`/api/user`, {
        method: "POST",
        body: JSON.stringify({
          name: register_name.value,
          email: register_email.value,
          password: register_password.value,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      registerMsg.style.display = "block";
      registerMsg.textContent = data["message"];
      hasMsg = true;
    } catch (error) {
      console.log(error);
    }
  }
}
registerBtn.addEventListener("click", registerSystem);

//會員登入驗證
const signInBtn = document.getElementById("signIn_button");
const signInMsg = document.querySelector(".signInMsg");
// const token = localStorage.getItem("access_token");
// localStorage.setItem("access_token", token);

async function logInSystem() {
  try {
    const response = await fetch(`/api/user/auth`, {
      method: "PUT",
      body: JSON.stringify({
        email: logIn_email.value,
        password: logIn_password.value,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log(data);
    if (data["ok"]) {
      location.reload();
    } else {
      signInMsg.style.display = "block";
      signInMsg.textContent = data["message"];
      hasMsg = true;
    }
  } catch (error) {
    console.log(error);
  }
}

signInBtn.addEventListener("click", logInSystem);

//會員登出
async function logOutUser() {
  try {
    const response = await fetch(`/api/user/auth`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    if (data["ok"]) {
      btnSignOut.classList.remove("show");
      btnOpenSignInFrom.classList.remove("show");
      window.location.reload();
    } else {
      console.log("登出失敗");
    }
  } catch (error) {
    console.log(error);
  }
}

btnSignOut.addEventListener("click", logOutUser);

//歷史購物紀錄
const BtnHistoryPage = document.getElementById("nav_history");
const nav_history = BtnHistoryPage.addEventListener("click", () => {
  if (!token) {
    openSignInFrom();
  } else {
    window.location.href = `/history`;
  }
});

const notifyBox = document.querySelector(".notify_box");
const btnCloseNotify = document.querySelector(".btn_close_notify");
const notifyMsg = document.querySelector(".notify_message");

//付款狀態通知
const closeNotify = function () {
  notifyBox.classList.remove("show");
};
btnCloseNotify.addEventListener("click", closeNotify);
