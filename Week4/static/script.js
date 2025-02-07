function verifyCheckbox(event) {
    let checkbox = document.getElementById("agree");
    if (!checkbox.checked) {
        event.preventDefault(); // 阻止表單提交
        alert("請勾選同意條款");
        return false; // ❌ 驗證失敗，表單不提交
    }
    return true; // ✅ 驗證通過
}
