var currentProtocol = location.protocol; // 현재 프로토콜 (예: "http:", "https:")
var currentHost = location.host; // 현재 호스트 (예: "example.com", "localhost:3000")

var fullURL = currentProtocol + '//' + currentHost;

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

    fetch(fullURL + "/guest/upload/",{
        method: 'POST',
        body: formData,
    })
    .then(response=>{
        if(response.ok){
			alert("업로드 완료!");
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

function copyToClipboard(text) {
  // 텍스트를 임시로 저장할 textarea 엘리먼트를 생성합니다.
  var textarea = document.createElement('textarea');
  textarea.value = text;

  // textarea를 body에 추가합니다.
  document.body.appendChild(textarea);

  // textarea의 내용을 선택하고 복사합니다.
  textarea.select();
  document.execCommand('copy');

  // textarea를 제거합니다.
  document.body.removeChild(textarea);
}

function copylink_click_event(url) {
	fetch(fullURL + '/share/' + '?url=' + url)
	.then(res => res.json())
	.then(data => {
		const copylink_btn = document.querySelector('.copylink');

		copylink_btn.disabled = true;
		copylink_btn.innerText = data['url'];
		copyToClipboard(data['url']);
		alert('복사 완료!');
	})
	.catch(err => alert('error!'))
}

function create_qr_event(url){
 	window.open('/popup_share/' + '?url=' + url, 'target', 'top=100, left=300, width=500, height=600, \
		toolbar=no, menubar=no, location=no, status=no, scrollbars=no, resizable=no');
 }

function update_preview(data)
{
	const file_name = document.querySelector('.detailed .tl .name span');
	file_name.innerText = data['file_name'];
	const file_type = document.querySelector('.r_detail .i1 .i1-1 p');
	file_type.innerText = '파일형식 : ' + data['suffix_name'];
	const file_path = document.querySelector('.r_detail .i2 .i2-1 p');
	file_path.innerText= '파일위치 : ' + "/";
	const file_size = document.querySelector('.r_detail .i3 .i3-1 p');
	file_size.innerText = '크기 : ' + data['size'] + 'bytes';
	const upload_date = document.querySelector('.r_detail .i4 .i4-1 p');
	upload_date.innerText = '업로드 날짜 : ' + data['created_at'];

	// share 관련 Update
	const copylink_btn = document.querySelector('.copylink');
	copylink_btn.addEventListener('click', (event) =>{
		copylink_click_event(data['download_url']);
	});

	const create_qr_btn = document.querySelector('.createqr');
	create_qr_btn.addEventListener('click', (event) =>{
		create_qr_event(data['download_url']);
	});
}


let file_list = document.querySelector('.down');
let passwd_cookie = getCookie('passwd');
if (passwd_cookie == null)
    alert("No passwd!");
fetch(fullURL + "/guest/list/", { // 파일 정보 api호출
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
			<div class="uploaded_file file${i}">
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
	const file_divs = file_list.children;
	for (let i = 0; i < file_divs.length; i++) {
		const file_div = file_divs[i];
		file_div.addEventListener('click', function(event) {
			update_preview(data[i]);
		});
	}
})

const show_code = document.getElementById('show_code');
show_code.innerText = "Code : " + passwd_cookie;
