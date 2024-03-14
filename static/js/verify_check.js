function validateForm() {
    let x = document.getElementsByName('email')[0].value;
    let at_pos = x.indexOf("@");
    let dot_pos = x.lastIndexOf(".");
    if (at_pos<1 || dot_pos<at_pos+2 || dot_pos+2>=x.length){
        alert("不是一个有效的 e-mail 地址");
        return false;
    }
    return true
}

