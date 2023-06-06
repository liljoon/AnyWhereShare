function onClickUpload() {
    let myInput = document.getElementById("file");
    myInput.click();
}

function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        return decodeURIComponent(match[2]);
    }
    return null;
}


let file_list = document.querySelector('#file_list');
let passwd_cookie = getCookie('passwd');
if (passwd_cookie == null)
    alert("No passwd!");
fetch("http://localhost:8000/guest/list/", { // 파일 정보 api호출
    method : 'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body:JSON.stringify({
        'passwd' : passwd_cookie
    })
})
.then(res => res.json())
.then(data =>{
    data.forEach(file => { // 각 파일별로 한줄씩 idx, file_name, url, share순서
        file_list.innerHTML += `<p>idx: ${file['id']}
             file: ${file['file_name']}
             <a href="${file['download_url']}">Download</a>
             <a href="/next">Share</a>
             </p>`; // Share 링크는 share페이지로 넘어가도록 설정해야함
    });
})