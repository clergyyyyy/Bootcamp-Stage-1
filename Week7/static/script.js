function confirmDelete() {
        return confirm("確定要刪除此留言嗎？");
    };

    
    
    async function updateName() {
        const name = document.getElementById("updateName").value.trim();
        if (!name) {
            alert("請輸入欲更新的姓名");
            return;
        }
    
        try {
            const response = await fetch(`/api/member`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: name }) // 將新的名字以 JSON 格式傳送
            });
    
            const data = await response.json();
    
            if (data.ok) {
                alert("姓名更新成功！");
                document.getElementById("result_name").innerHTML = `<p>更新成功</p>`;
            } else {
                alert("姓名更新失敗Failed to Update");
            }
        } catch (error) {
            console.error("更新失敗", error);
            alert("發生錯誤，請稍後再試！");
        }
    }
    

async function searchMember() {
    const username = document.getElementById("searchUsername").value.trim();
    if (!username) {
        alert("請輸入會員帳號");
        return;
    }

    try {
        const response = await fetch(`/api/member?username=${encodeURIComponent(username)}`);
        console.log(`${encodeURIComponent(username)}`);

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            const text = await response.text();
            console.error("Unexpected response:", text);
            alert("伺服器回應錯誤，請稍後再試");
            return;
        }

        const data = await response.json();
        const resultDiv = document.getElementById("result_username");
        if (data.data) {
            resultDiv.innerHTML = `<p>${data.data.name} (${data.data.username})</p>`
        } else {
            resultDiv.innerHTML = "<p>無此會員</p>";
        }
        
    } catch (error) {
        console.error("查詢失敗", error);
        alert("發生錯誤，請稍後再試！");
    }
}




/*function verifyCheckbox(event) {
    let checkbox = document.getElementById("agree");
    if (!checkbox.checked) {
        event.preventDefault();
        alert("請勾選同意條款");
        return false;
    }
    return true;
}*/

/*function verifyPositiveInteger(event) {
    let inputValue = document.getElementById("integer").value;
    let floatValue = parseFloat(inputValue);
    if (Number.isNaN(floatValue) || floatValue < 1 || !Number.isInteger(floatValue)) {
        alert("請輸入大於0的正整數");
        event.preventDefault();
        return false;
    }
    return true;
}*/
