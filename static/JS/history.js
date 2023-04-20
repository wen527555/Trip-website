"use strict";
const history_info = document.querySelector(".history_Container");

async function getHistory() {
  try {
    const response = await fetch(`/api/history`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      const result = await response.json();
      renderHistory(result);
    } else {
      console.log("API呼叫失敗:" + response.status);
    }
  } catch (error) {
    // console.log(error);
    console.log("API呼叫失敗:" + error.message);
  }
}

function renderHistory(result) {
  const historyData = result.data;
  if (historyData !== null) {
    historyData.forEach((history) => {
      const name = history.attraction_name;
      const date = history.date;
      const time = history.time;
      const address = history.attraction_address;
      //   console.log(orderNumber);
      const renderInfo = `
<div class="history_box">
<div class="history_box＿left">
  <div class="history_name">${name}</div>
  <div class="history_title2">
    日期：
    <div class="history_text history_date" id="history_date" ">${date}</div>
  </div>
  <div class="history_title2">
    時間：
    <div class="history_text history_time" id="history_time" ">${time}</div>
  </div>
  <div class="history_title2">
    地點：
    <div class="history_text history_address" id="history_address" ">${address}</div>
  </div>
  </div>
<button class="history_btn">
  訂單詳細資訊
</button>
</div>
`;
      history_info.insertAdjacentHTML("beforeend", renderInfo);
    });

    const historyBtns = document.querySelectorAll(".history_btn");
    historyBtns.forEach((historyBtn, index) => {
      historyBtn.addEventListener("click", () => {
        const orderNumber = historyData[index].order_number;
        window.location.href = `/thankyou?number=${orderNumber}`;
      });
    });
  } else {
    const nohistory = `   
    <div class="history_Container"> 
    <div class="nohistory">沒有歷史紀錄</div>
    </div>`;
    history_info.insertAdjacentHTML("beforeend", nohistory);
  }
}

document.addEventListener("DOMContentLoaded", getHistory);
