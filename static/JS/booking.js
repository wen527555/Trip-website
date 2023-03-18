"use strict";

// import { openSignInFrom } from "./user.js";
const btnBookingPage = document.getElementById("nav_booking");

const order_name = document.querySelector(".order_name");
const order_date = document.querySelector(".order_date");
const order_time = document.querySelector(".order_time");
const order_price = document.querySelector(".order_price");
const order_address = document.querySelector(".order_address");
const order_image = document.querySelector(".order_image");
const order_username = document.querySelector(".order_username");
const token = getCookie("access_token");

function getBooking() {
  if (!token) {
    openSignInFrom();
  } else {
    fetch(`/api/booking`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          console.log("API呼叫失敗:" + response.status);
        }
      })
      .then((bookingData) => {
        renderBooking(bookingData);
      })
      .catch((error) => {
        console.log("API呼叫失敗:" + error.message);
      });
  }
}

function renderBooking(bookingData) {
  console.log(bookingData);
  const data = bookingData.data;
  console.log(data);
  const main = document.getElementById("main_booking");
  if (data !== null) {
    const attraction = bookingData.data.attraction;
    const name = attraction.name;
    const date = data.date;
    const time = data.time;
    const price = data.price;
    const address = attraction.address;
    const image = attraction.image[0];
    const username = data.username;
    const renderBooking = `

          <div class="order_Section order_Section1">
          <div class="order_username">您好，${username}，待預定的行程如下：</div>
          <div class="order_image" style="background-image: url('${image}')"></div>
          <div class="order_Section1_middle">
            <div class="order_name">台北一日遊：${name}</div>
            <div class="order_title2">
              日期：
              <div class="order_text order_date" id="order_date">${date}</div>
            </div>
            <div class="order_title2">
              時間：
              <div class="order_text order_time" id="order_time">${time}</div>
            </div>
            <div class="order_title2">
              費用：
              <div class="order_text order_price" id="order_price">新台幣${price}元</div>
            </div>
            <div class="order_title2">
              地點：
              <div class="order_text order_address" id="order_address">${address}</div>
            </div>
          </div>
          <div class="order_deletebtn">
            <img
              src="../static/css/picture/icon_delete.png"
              id="order_deletebtn" onclick="deleteBooking()"
            />
          </div>
        </div>
        <div class="order_Section order_Section2">
          <hr />
          <div class="order_title">您的聯絡資訊</div>
          <form class="contact_form">
            <div class="input_box">
              <label class="order_text" for="contact_name">聯絡姓名：</label>
              <input type="text" id="contact_name" />
            </div>
            <div class="input_box">
              <label class="order_text" for="contact_email">聯絡信箱：</label>
              <input type="email" id="contact_email" />
            </div>
            <div class="input_box">
              <label class="order_text" for="contact_phone">手機號碼：</label>
              <input type="text" id="contact_phone" />
            </div>
          </form>
          <div class="order_text2">
            請保持手機暢通，準時到達，導覽人員將用手機與您聯繫，務必留下正確的聯絡方式。
          </div>
        </div>
        <div class="order_Section order_Section3">
          <hr />
          <div class="order_title">信用卡付款資訊</div>
          <form class="creditCard_number">
            <div class="input_box">
              <label class="order_text" for="creditCard_number">卡片號碼：</label>
              <input type="text" id="creditCard_number" />
            </div>
            <div class="input_box">
              <label class="order_text" for="creditCard_date">過期時間：</label>
              <input type="email" id="creditCard_date" />
            </div>
            <div class="input_box">
              <label class="order_text" for="creditCard_password"
                >驗證密碼：</label
              >
              <input type="text" id="creditCard_password" />
            </div>
          </form>
        </div>

        <div class="order_Section order_Section4">
          <hr />
          <div class="order_Section4_right">
            <div class="order_totalPrice" id="order_totalPrice"></div>
            <button class="payment_btn">確認訂購並付款</button>
          </div>
        </div>`;
    main.insertAdjacentHTML("beforeend", renderBooking);

    // const booking = ``;
    // main.insertAdjacentHTML("beforeend", booking);
    // order_name.textContent = "台北一日遊：" + name;
    // order_date.textContent = date;
    // order_time.textContent = time;
    // order_price.textContent = "新台幣" + price + "元";
    // order_address.textContent = address;
    // order_image.style.backgroundImage = `url(${image})`;
  } else {
    const noBooking = `<div class="noBooking">目前沒有任何待預約的行程</div>`;
    main.insertAdjacentHTML("beforeend", noBooking);
  }
}

document.addEventListener("DOMContentLoaded", getBooking);

const nav_booking = btnBookingPage.addEventListener("click", () => {
  if (!token) {
    openSignInFrom();
  } else {
    window.location.href = `/booking`;
  }
});

//建立旅遊行程
function CreateBooking() {
  const bookingDate = document.getElementById("booking_date");
  const attraction_Id = window.location.pathname.split("/")[2];
  let bookingPrice = null;
  let bookingTime = null;
  if (morning.checked) {
    bookingTime = "早上9點至中午12點";
    bookingPrice = 2000;
  } else {
    bookingTime = "下午2點至下午4點";
    bookingPrice = 2500;
  }

  if (!token) {
    openSignInFrom();
  } else if (
    bookingDate.value === "" ||
    bookingTime === null ||
    bookingPrice === null
  ) {
    console.log("所有欄位皆須填寫，請勿空白");
  } else {
    fetch(`/api/booking`, {
      method: "POST",
      body: JSON.stringify({
        attractionId: attraction_Id,
        date: bookingDate.value,
        time: bookingTime,
        price: bookingPrice,
      }),
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data !== null) {
          window.location.href = `/booking`;
        } else {
          console.log("建立行程失敗");
        }
      })
      .catch((error) => {
        // console.log(error);
        console.log("API呼叫失敗:" + error.message);
      });
  }
}
const btnCreateBooking = document.querySelector(".booking_btn");
btnCreateBooking.addEventListener("click", CreateBooking);

//刪除旅遊行程
function deleteBooking() {
  if (!token) {
    openSignInFrom();
  } else {
    fetch(`/api/booking`, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          console.log("API呼叫失敗:" + response.status);
        }
      })
      .then((data) => {
        location.reload();
        console.log("已成功刪除行程");
      });
  }
}
