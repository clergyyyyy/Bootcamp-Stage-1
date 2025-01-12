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
