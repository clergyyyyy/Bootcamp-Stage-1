function verifyCheckbox(event) {
    let checkbox = document.getElementById("agree");
    if (!checkbox.checked) {
        event.preventDefault();
        alert("請勾選同意條款");
        return false;
    }
    return true;
}
