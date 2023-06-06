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


let file_list = document.querySelector('.down');
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
		file_list.innerHTML += `
			<div class="uploaded_file">
                <div class="d1">
					<input type="checkbox" id="check2">
					<label for="check2"></label></label>
                </div>
					<div class="d2">${file['file_name']}</div>
					<div class="d4">
						<a href="${file['download_url']}">Download</a>
					</div>
					<div class="d3"><img src="/static/img/bookmark_be.png" style="width:20px; height:20px;"></div>
            </div>
		`;
    });
})

const show_code = document.getElementById('show_code');
show_code.innerText = "Code : " + passwd_cookie;
