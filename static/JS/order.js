//取得付款資訊
const btnBackIndex = document.querySelector(".btnBackIndex");
btnBackIndex.addEventListener("click", () => {
  window.location.href = `/`;
});
const orderInfo = document.querySelector(".thank_info");
const orderContact = document.querySelector(".thank_contact");
const urlParams = new URLSearchParams(window.location.search);
const orderNumber = urlParams.get("number");
console.log(orderNumber);

async function getOrder() {
  try {
    const response = await fetch(`/api/order/${orderNumber}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    });
    const result = await response.json();
    const order = result.data;
    const trip = order.trip;
    const attraction = order.trip.attraction;
    console.log(order);
    const number = order.number;
    const name = attraction.name;
    const date = trip.date;
    const time = trip.time;
    const price = order.price;
    const image = attraction.image;
    const contactName = order.contact.name;
    const contactEmail = order.contact.email;
    const contactPhone = order.contact.phone;

    const renderInfo = `
    <div class="thankInfo_left">
      <div class="thank_title2" id="thank_number">訂單編號：${number}</div>
      <div class="thank_title2">
        景點：
        <div class="thank_text" id="thank_name">
          ${name}
        </div>
      </div>
      <div class="thank_title2">
        日期：
        <div class="thank_text" id="thank_date">${date}</div>
      </div>
      <div class="thank_title2">
        時間：
        <div class="thank_text" id="thank_time">${time}</div>
      </div>
      <div class="thank_title2">
        費用：
        <div class="thank_text" id="thank_price">新台幣${price}元</div>
      </div>
      </div>
      <div class="thank_image" style="background-image: url('${image}')"></div>
      `;
    const renderContact = `
      <div class="thank_title2">
      聯絡姓名：
      <div class="thank_text" id="thank_contact_name">${contactName}</div>
    </div>
    <div class="thank_title2">
      聯絡手機：
      <div class="thank_text" id="thank_contact_email">${contactPhone}</div>
    </div>
    <div class="thank_title2">
      Email：
      <div class="thank_text" id="thank_contact_phone">${contactEmail}</div>
    </div>`;
    orderInfo.insertAdjacentHTML("beforeend", renderInfo);
    orderContact.insertAdjacentHTML("beforeend", renderContact);
  } catch (error) {
    // console.log(error);
    console.log("API呼叫失敗:" + error.message);
  }
}
getOrder();
