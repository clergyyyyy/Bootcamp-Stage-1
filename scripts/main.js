let url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1';
let currentIndex = 3; // 從第 4 筆資料開始
const pageSize = 10; // 每次加載 10 筆

document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const closeBtn = document.querySelector(".close-btn");
    const sideMenu = document.querySelector(".side-menu");

    // 打開側選單
    hamburger.addEventListener("click", () => {
        sideMenu.classList.add("active"); // 顯示側選單
    });

    // 關閉側選單
    closeBtn.addEventListener("click", () => {
        sideMenu.classList.remove("active"); // 隱藏側選單
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const loadBtn = document.querySelector(".loadbtn");

    // 初始化載入資料
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const results = data.data.results;

            // 更新 .promotion 的前三筆資料
            updatePromotion(results.slice(0, 3));

            // 取代 .big-box 的預設內容並載入卡片 (3-13)
            replaceDefaultCards(results.slice(3, 13));

            // 更新當前Index
            currentIndex = 13;

            // 如果資料超過 13 筆，顯示按鈕
            if (results.length > 13) {
                loadBtn.style.display = "flex";
            }

            // 按鈕加載更多資料邏輯
            loadBtn.addEventListener("click", () => {
                appendMoreCards(results);
            });
        })
        .catch(error => console.error("Error fetching JSON:", error));
});

// 更新 .promotion 區塊
function updatePromotion(data) {
    const promotionSections = document.querySelectorAll(".promotion");

    data.forEach((item, index) => {
        const img = promotionSections[index].querySelector("img");
        const h2 = promotionSections[index].querySelector("h2");

        const imageUrl = getValidImageUrl(item.filelist);
        img.src = imageUrl;
        img.alt = item.stitle;
        h2.textContent = item.stitle;
    });
}

// 用動態資料取代預設卡片內容
function replaceDefaultCards(data) {
    const bigBox = document.querySelector(".big-box");

    // 清空 .big-box 的預設內容
    bigBox.innerHTML = "";

    // 動態添加卡片內容
    data.forEach(item => {
        const card = createCardElement(item);
        bigBox.appendChild(card);
    });

    adjustLastRowRules(); // 調整最後一行的寬度
}

// 動態加載更多卡片
function appendMoreCards(data) {
    const bigBox = document.querySelector(".big-box");
    const loadBtn = document.querySelector(".loadbtn");

    const nextBatch = data.slice(currentIndex, currentIndex + pageSize);
    nextBatch.forEach(item => {
        const card = createCardElement(item);
        bigBox.appendChild(card);
    });

    currentIndex += pageSize; // 更新當前索引

    // 如果所有資料已加載完，隱藏按鈕
    if (currentIndex >= data.length) {
        loadBtn.style.display = "none";
    }

    adjustLastRowRules(); // 調整最後一行的寬度
}

// 創建單個卡片元素
function createCardElement(item) {
    const card = document.createElement("div");
    card.classList.add("card");

    const img = document.createElement("img");
    const imageUrl = getValidImageUrl(item.filelist);
    img.src = imageUrl;
    img.alt = item.stitle;
    img.style.objectFit = "cover"; // 確保圖片填滿範圍
    img.style.width = "100%"; // 撐滿父容器

    const h2 = document.createElement("h2");
    h2.textContent = item.stitle;

    card.appendChild(img);
    card.appendChild(h2);

    return card;
}

// 獲取有效的圖片網址
function getValidImageUrl(filelist) {
    const urls = filelist.split("https://").filter(url => url.endsWith(".jpg"));
    return urls.length > 0 ? `https://${urls[0]}` : "images/image.png"; // 使用預設圖片
}

// 調整最後一行的卡片寬度
function adjustLastRowRules() {
    const bigBox = document.querySelector(".big-box");
    const visibleCards = Array.from(bigBox.querySelectorAll(".card"));

    const totalVisible = visibleCards.length;
    const remainder = totalVisible % 4; // 計算餘數
    const gap = 20; // 與 CSS gap 一致

    // 移除之前的 inline-style 避免累積
    visibleCards.forEach(card => {
        card.style.flex = "";
        card.style.maxWidth = "";
    });

    // 應用規則
    if (window.matchMedia("(min-width: 601px) and (max-width: 1200px)").matches) {

        if (window.matchMedia("(min-width: 601px) and (max-width: 1200px)").matches) {
            if (remainder === 1) {
                // 只有 1 個卡片，佔滿整行
                visibleCards[totalVisible - 1].style.flex = `1 1 calc(100%)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc(100%)`;
            } else if (remainder === 2) {
                // 最後 2 個卡片均分整行
            // 最後 2 個卡片均分整行，間距為 gap
                visibleCards[totalVisible - 2].style.flex = `1 1 calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 2].style.maxWidth = `calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 1].style.flex = `1 1 calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc(50% - ${gap}px / 2)`;
            } else if (remainder === 3) {
                // 最後 3 個卡片均分整行
                visibleCards[totalVisible - 3].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 3].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 2].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 2].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 1].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
            } else if (remainder === 0) {
                // 最後 4 個卡片均分整行
                visibleCards[totalVisible - 4].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 4].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 3].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 3].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 2].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 2].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 1].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
            }
        }    
    } else if (window.matchMedia("(min-width: 360px) and (max-width: 600px)").matches) {
        // 在 360px ~ 600px 的範圍內應用 JavaScript 調整
        
        // 確保 container2 寬度為 90%
        const container2 = document.querySelector(".container2");
        if (container2) {
            container2.style.width = "90%";
        }

        // 確保 container2 寬度為 90%
        if (bigBox) {
            bigBox.style.margin = "12px 0";
        }
    
        // 確保 promotion 獨占一行
        const promotions = document.querySelectorAll(".small-box .promotion");
        if (container2) {
            container2.style.width = "90%";
        }

        promotions.forEach(promotion => {
            promotion.style.flex = "1 1 100%"; // 每張 promotion 獨占一行
            promotion.style.maxWidth = "100%"; // 撐滿父容器寬度
        });
    
        // 確保 card 獨占一行
        const visibleCards = document.querySelectorAll(".big-box .card");
        visibleCards.forEach(card => {
            card.style.flex = "1 1 100%"; // 每張卡片獨占一行
            card.style.maxWidth = "100%"; // 撐滿父容器寬度
        });
    } else {
        // 移除 360px ~ 600px 的 JavaScript 設置，讓其他尺寸使用 CSS 規則
        const promotions = document.querySelectorAll(".small-box .promotion");
        promotions.forEach(promotion => {
            promotion.style.flex = ""; // 清空 JavaScript 設置
            promotion.style.maxWidth = ""; // 清空 JavaScript 設置
        });
    
        const visibleCards = document.querySelectorAll(".big-box .card");
        visibleCards.forEach(card => {
            card.style.flex = ""; // 清空 JavaScript 設置
            card.style.maxWidth = ""; // 清空 JavaScript 設置
        });

        const menu = document.querySelector(".menu");
        if (menu) {
            menu.style.display = ""; // 確保不覆蓋 CSS
        }

    }    
}

// 監聽視窗尺寸變化
window.addEventListener("resize", () => {
    adjustLastRowRules();
});
