"use strict";
const order_info = document.querySelectorAll(".order_info");

async function getBooking() {
  if (!token) {
    openSignInFrom();
  } else {
    try {
      const response = await fetch(`/api/booking`, {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const bookingData = await response.json();
        renderBooking(bookingData);
      } else {
        console.log("API呼叫失敗:" + response.status);
      }
    } catch (error) {
      console.log("API呼叫失敗:" + error.message);
    }
  }
}
// let ordersdata = [];
let trip = [];
const totalPrice = document.querySelector(".order_totalPrice");

const orderData = function () {
  const order_name = document.querySelector(".order_name").textContent.slice(6);
  const order_date = document.querySelector(".order_date").textContent;
  const order_time = document.querySelector(".order_time").textContent;
  const order_address = document.querySelector(".order_address").textContent;
  const imageElement = document.querySelector(".order_image");
  const imageUrl = imageElement.style.backgroundImage
    .slice(4, -1)
    .replace(/"/g, "");
  const attraction_id = imageElement.getAttribute("attraction_id");
  const total_price = totalPrice.textContent.slice(6, -1);

  let data = {
    attraction: {
      id: attraction_id,
      name: order_name,
      address: order_address,
      image: imageUrl,
    },
    date: order_date,
    time: order_time,
    price: total_price,
  };

  trip.push(data);
};
// console.log(trip);
function renderBooking(bookingData) {
  const data = bookingData.data;
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
    const attraction_id = attraction.id;
    order_info.forEach((e) => {
      e.classList.remove("hidden");
    });
    const renderBooking = `
          <div class="order_Section" id="order_Section1">
          <div class="order_username">您好，${username}，待預定的行程如下：</div>
          <div class="order_image" style="background-image: url('${image}')" attraction_id="${attraction_id}" ></div>
          <div class="order_Section1_middle">
            <div class="order_name" ">台北一日遊：${name}</div>
            <div class="order_title2">
              日期：
              <div class="order_text order_date" id="order_date" ">${date}</div>
            </div>
            <div class="order_title2">
              時間：
              <div class="order_text order_time" id="order_time" ">${time}</div>
            </div>
            <div class="order_title2">
              費用：
              <div class="order_text order_price" id="order_price" ">新台幣${price}元</div>
            </div>
            <div class="order_title2">
              地點：
              <div class="order_text order_address" id="order_address" ">${address}</div>
            </div>
          </div>
          <div class="order_deletebtn">
            <img
              src="../static/css/picture/icon_delete.png"
              id="order_deletebtn" onclick="deleteBooking()"
            />
          </div>
        </div>
`;
    if (price === 2000) {
      totalPrice.innerText = "總價：新台幣2000元";
    } else {
      totalPrice.innerText = "總價：新台幣2500元";
    }
    main.insertAdjacentHTML("beforeend", renderBooking);
    orderData();
  } else {
    const noBooking = `   
    <div class="order_Section order_Section1"> 
    <div class="noBooking">目前沒有任何待預約的行程</div>
    </div>`;
    main.insertAdjacentHTML("beforeend", noBooking);
  }
}
document.addEventListener("DOMContentLoaded", getBooking);

//刪除旅遊行程
async function deleteBooking() {
  if (!token) {
    openSignInFrom();
  } else {
    try {
      const response = await fetch(`/api/booking`, {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        if (data) {
          location.reload();
          console.log("已成功刪除行程");
        }
      } else {
        console.log("API呼叫失敗:" + response.status);
      }
    } catch (error) {
      console.log("API呼叫失敗:" + error.message);
    }
  }
}

TPDirect.setupSDK(
  128060,
  "app_FumkJDgsJknsS3H1zvKb88gRyGE2jYgyrfdxdREjWh0b59yij2ff6rSj3J2r",
  "sandbox"
);

TPDirect.card.setup({
  fields: {
    number: {
      // css selector
      element: document.getElementById("card-number"),
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      // DOM object
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: document.getElementById("card-ccv"),
      placeholder: "ccv",
    },
  },
  styles: {
    // Style all elements
    input: {
      color: "gray",
    },
    // Styling ccv field
    "input.ccv": {
      "font-size": "16px",
    },
    // Styling expiration-date field
    "input.expiration-date": {
      "font-size": "16px",
    },
    // Styling card-number field
    "input.card-number": {
      "font-size": "16px",
    },
    // style focus state
    ":focus": {
      color: "black",
    },
    // style valid state
    ".valid": {
      color: "#448899",
    },
    // style invalid state
    ".invalid": {
      color: "red",
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    "@media screen and (max-width: 400px)": {
      input: {
        color: "#448899",
      },
    },
  },
  // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

//檢查聯絡資訊輸入格式
const btnPayment = document.querySelector(".payment_btn");
const contactEmail = document.querySelector("#contact_email");
const contactPhone = document.querySelector("#contact_phone");
const contactName = document.querySelector("#contact_name");
const phoneRegex = /^09\d{8}$/;
const emailRegex = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
const nameRegex = /^[\u4E00-\u9FA5a-zA-Z]{2,10}$/;

const checkContactStatus = (input, regex) => {
  const image = input.nextElementSibling;
  image.src = regex.test(input.value)
    ? "../static/css/picture/check.png"
    : "../static/css/picture/cancel.png";
};

const phoneInfo = contactPhone.addEventListener("input", () =>
  checkContactStatus(contactPhone, phoneRegex)
);
const emailInfo = contactEmail.addEventListener("input", () =>
  checkContactStatus(contactEmail, emailRegex)
);

const nameInfo = contactName.addEventListener("input", () =>
  checkContactStatus(contactName, nameRegex)
);

// listen for TapPay Field
TPDirect.card.onUpdate(function (update) {
  /* Disable / enable submit button depend on update.canGetPrime  */

  if (
    contactPhone.value === "" ||
    contactEmail.value === "" ||
    contactName.value === ""
  ) {
    notifyBox.classList.add("show");
    notifyMsg.innerText = "請確認聯絡資訊填寫格式是否正確";
  }

  if (update.canGetPrime) {
    btnPayment.removeAttribute("disabled");
    btnPayment.addEventListener("click", onSubmit);
  } else {
    btnPayment.removeEventListener("click", onSubmit);
    // btnPayment.style.opacity = "30%";
    btnPayment.setAttribute("disabled", true);
  }

  // 檢查信用卡資訊輸入格式

  if (update.status.number === 2) {
    checkInputStatus("#card-number", "hasError");
  } else if (update.status.number === 0) {
    checkInputStatus("#card-number", "hasSuccess");
  } else {
    checkInputStatus("#card-number", "");
  }

  if (update.status.expiry === 2) {
    checkInputStatus("#card-expiration-date", "hasError");
  } else if (update.status.expiry === 0) {
    checkInputStatus("#card-expiration-date", "hasSuccess");
  } else {
    checkInputStatus("#card-expiration-date", "");
  }

  if (update.status.ccv === 2) {
    checkInputStatus("#card-ccv", "hasError");
  } else if (update.status.ccv === 0) {
    checkInputStatus("#card-ccv", "hasSuccess");
  } else {
    checkInputStatus("#card-ccv", "");
  }
});

function checkInputStatus(selector, status) {
  const element = document.querySelector(selector);
  const image = element.nextElementSibling;

  if (status === "hasError") {
    image.src = "../static/css/picture/cancel.png";
  } else if (status === "hasSuccess") {
    image.src = "../static/css/picture/check.png";
  } else if (status) {
    image.src = "";
  }
}

function onSubmit(event) {
  event.preventDefault();

  const tappayStatus = TPDirect.card.getTappayFieldsStatus();

  // Check TPDirect.card.getTappayFieldsStatus().canGetPrime before TPDirect.card.getPrime
  if (tappayStatus.canGetPrime === false) {
    console.log("can not get prime");
    return;
  }

  // Get prime
  TPDirect.card.getPrime(function (result) {
    if (result.status !== 0) {
      console.log("get prime error: " + result.msg);
      return;
    }
    console.log("get prime 成功，prime: " + result.card.prime);

    let orders = {
      prime: result.card.prime,
      orders: {
        trip: trip,
        contact: {
          name: contactName.value,
          phone: contactPhone.value,
          email: contactEmail.value,
        },
      },
    };
    createOrder(orders);
  });
}

//建立新的付款訂單
async function createOrder(orders) {
  try {
    const response = await fetch(`/api/orders`, {
      method: "POST",
      body: JSON.stringify(orders),
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    });
    const result = await response.json();
    // console.log(result.data);
    const orderData = result.data;
    const orderNumber = orderData.number;
    console.log(orderData.payment.status);
    if (orderData.payment.status === 0) {
      window.location.href = `/thankyou?number=${orderNumber}`;
    } else {
      notifyBox.classList.add("show");
      notifyMsg.innerText =
        "訂單編號：" + orderNumber + "\n 付款失敗，\n 請檢查付款資訊是否正確";
    }
  } catch (error) {
    console.log("API呼叫失敗:" + error.message);
  }
}
