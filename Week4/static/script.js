function verifyCheckbox(event) {
    let checkbox = document.getElementById("agree");
    if (!checkbox.checked) {
        event.preventDefault();
        alert("請勾選同意條款");
        return false;
    }
    return true;
}

function verifyPositiveInteger(event) {
    let inputValue = document.getElementById("integer").value;
    let floatValue = parseFloat(inputValue);
    if (Number.isNaN(floatValue) || floatValue < 1 || !Number.isInteger(floatValue)) {
        alert("請輸入大於0的正整數");
        event.preventDefault();
        return false;
    }
    return true;
}

