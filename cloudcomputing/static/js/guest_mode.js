/*function onClickUpload() {
    let myInput = document.getElementById("file");
    myInput.click();
}*/

function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        return decodeURIComponent(match[2]);
    }
    return null;
}


//수정
/*
document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('fileinput');
    var fileInfo = document.querySelector('.down');
  
    fileInput.addEventListener('change', function() {
      var file = fileInput.files[0];
      fileInfo.innerHTML = 'Selected File: ' + file.name;
      fileInfo.style.display = 'block';
  
      var form = document.getElementById('uploadForm');
      var formData = new FormData(form);
  
      var request = new XMLHttpRequest();
      request.open('POST', form.action);
      request.send(formData);
    });
  });
  
*/
//
function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var files = fileInput.files[0];

    var formData = new FormData();
    formData.append('file', files);

    fetch("http://127.0.0.1:8000/guest/upload/",{
        method: 'POST',
        body: formData,
    })
    .then(response=>{
        if(response.ok){
            location.reload();
        }
        else{
            console.log('파일 업로드 실패');
        }
    })
    .catch(error => {
        console.log('네트워크 오류');
    });

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
    let i=1;
    data.forEach(file => { // 각 파일별로 한줄씩 idx, file_name, url, share순서
        file_list.innerHTML += `
			<div class="uploaded_file">
                <div class="d1">
					<input type="checkbox" id="check${i}">
					<label for="check${i}"></label>
                </div>
				<div class="d2">${file['file_name']}</div>
				<div class="d4">
					<a href="${file['download_url']}">Download</a>
				</div>
				<div class="d3"><img src="/static/img/bookmark_be.png" style="width:20px; height:20px;"></div>
            </div>
		`;
        i++;
    });
})

const show_code = document.getElementById('show_code');
show_code.innerText = "Code : " + passwd_cookie;
