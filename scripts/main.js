let url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1';
let currentIndex = 3;
const pageSize = 10;

document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const closeBtn = document.querySelector(".close-btn");
    const sideMenu = document.querySelector(".side-menu");

    hamburger.addEventListener("click", () => {
        sideMenu.classList.add("active");
    });

    closeBtn.addEventListener("click", () => {
        sideMenu.classList.remove("active");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const loadBtn = document.querySelector(".loadbtn");

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const results = data.data.results;

            updatePromotion(results.slice(0, 3));

            replaceDefaultCards(results.slice(3, 13));

            // 更新Index
            currentIndex = 13;

            if (results.length > 13) {
                loadBtn.style.display = "flex";
            }

            loadBtn.addEventListener("click", () => {
                appendMoreCards(results);
            });
        })
        .catch(error => console.error("Error fetching JSON:", error));
});


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


function replaceDefaultCards(data) {
    const bigBox = document.querySelector(".big-box");

    bigBox.innerHTML = "";

    data.forEach(item => {
        const card = createCardElement(item);
        bigBox.appendChild(card);
    });

    adjustLastRowRules();
}

function appendMoreCards(data) {
    const bigBox = document.querySelector(".big-box");
    const loadBtn = document.querySelector(".loadbtn");

    const nextBatch = data.slice(currentIndex, currentIndex + pageSize);
    nextBatch.forEach(item => {
        const card = createCardElement(item);
        bigBox.appendChild(card);
    });

    currentIndex += pageSize;

    if (currentIndex >= data.length) {
        loadBtn.style.display = "none";
    }

    adjustLastRowRules();
}

function createCardElement(item) {
    const card = document.createElement("div");
    card.classList.add("card");

    const img = document.createElement("img");
    const imageUrl = getValidImageUrl(item.filelist);
    img.src = imageUrl;
    img.alt = item.stitle;
    img.style.objectFit = "cover";
    img.style.width = "100%";

    const h2 = document.createElement("h2");
    h2.textContent = item.stitle;

    card.appendChild(img);
    card.appendChild(h2);

    return card;
}


function getValidImageUrl(filelist) {
    const urls = filelist.split("https://").filter(url => url.endsWith(".jpg"));
    return urls.length > 0 ? `https://${urls[0]}` : "images/image.png";
}

function adjustLastRowRules() {
    const bigBox = document.querySelector(".big-box");
    const visibleCards = Array.from(bigBox.querySelectorAll(".card"));

    const totalVisible = visibleCards.length;
    const remainder = totalVisible % 4;
    const gap = 20;

    visibleCards.forEach(card => {
        card.style.flex = "";
        card.style.maxWidth = "";
    });

    if (window.matchMedia("(min-width: 601px) and (max-width: 1200px)").matches) {

        if (window.matchMedia("(min-width: 601px) and (max-width: 1200px)").matches) {
            if (remainder === 1) {
                visibleCards[totalVisible - 1].style.flex = `1 1 calc(100%)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc(100%)`;
            } else if (remainder === 2) {
                visibleCards[totalVisible - 2].style.flex = `1 1 calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 2].style.maxWidth = `calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 1].style.flex = `1 1 calc(50% - ${gap}px / 2)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc(50% - ${gap}px / 2)`;
            } else if (remainder === 3) {
                visibleCards[totalVisible - 3].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 3].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 2].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 2].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
                visibleCards[totalVisible - 1].style.flex = `1 1 calc((100% - 60px) / 4)`;
                visibleCards[totalVisible - 1].style.maxWidth = `calc((100% - ${gap * 3}px) / 4)`;
            } else if (remainder === 0) {
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
        
        const container2 = document.querySelector(".container2");
        if (container2) {
            container2.style.width = "90%";
        }

        if (bigBox) {
            bigBox.style.margin = "12px 0";
        }
    
        const promotions = document.querySelectorAll(".small-box .promotion");
        if (container2) {
            container2.style.width = "90%";
        }

        promotions.forEach(promotion => {
            promotion.style.flex = "1 1 100%";
            promotion.style.maxWidth = "100%";
        });
    
        const visibleCards = document.querySelectorAll(".big-box .card");
        visibleCards.forEach(card => {
            card.style.flex = "1 1 100%";
            card.style.maxWidth = "100%";
        });
    } else {
        const promotions = document.querySelectorAll(".small-box .promotion");
        promotions.forEach(promotion => {
            promotion.style.flex = "";
            promotion.style.maxWidth = "";
        });
    
        const visibleCards = document.querySelectorAll(".big-box .card");
        visibleCards.forEach(card => {
            card.style.flex = "";
            card.style.maxWidth = "";
        });

        const menu = document.querySelector(".menu");
        if (menu) {
            menu.style.display = "";
        }

    }    
}

window.addEventListener("resize", () => {
    adjustLastRowRules();
});
