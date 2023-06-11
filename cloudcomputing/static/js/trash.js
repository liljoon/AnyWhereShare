//전역변수 : 현재 폴더 위치
//처음 path="/"
//토큰 accessToken =""
var currentProtocol = location.protocol; // 현재 프로토콜 (예: "http:", "https:")
var currentHost = location.host; // 현재 호스트 (예: "example.com", "localhost:3000")

var fullURL = currentProtocol + '//' + currentHost;
window.onload = function(){

    setTimeout(() => fetchTrashList(), 1000);
    const recoverButton = document.getElementById('recoverButton');
    const realDeleteButton = document.getElementById('realDeleteButton');
    const usermodeButton = document.querySelector('a[href="/user_mode"]');
    recoverButton.addEventListener('click', () => {handleFileRecover();});
    realDeleteButton.addEventListener('click', () => {handleFileDelete();});
    usermodeButton.addEventListener('click', () => { document.cookie = "path=/; path=/";});
}
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return ((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function getToken() {
    // 쿠키에서 액세스 토큰 가져오기
    const cookie = document.cookie;
    const tokenStartIndex = cookie.indexOf("accessToken=");
    if (tokenStartIndex > -1) {
        const tokenEndIndex = cookie.indexOf(";", tokenStartIndex);
        if (tokenEndIndex > -1) {
            return cookie.substring(tokenStartIndex + 12, tokenEndIndex);
        } else {
            return cookie.substring(tokenStartIndex + 12);
        }
    }
}
function fetchTrashList() {
    const accessToken = getToken();
    const fileListElement = document.getElementById("show");
    fileListElement.innerHTML = '';

    fetch(fullURL + '/files/trashlist/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach((element) => {
            const fileElement = document.createElement("div");
            fileElement.className = "uploaded_file";
            fileElement.addEventListener("click",
            () => {handleFileInfoClick(element);});
            const checkboxDiv = document.createElement("div");
            checkboxDiv.className = "d1";

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.className = 'check';
            checkbox.id = `resource_${element.resource_id}`;

            const checkboxLabel = document.createElement("label");
            checkboxLabel.htmlFor = `resource_${element.resource_id}`;

            checkboxDiv.appendChild(checkbox);
            checkboxDiv.appendChild(checkboxLabel);

            const hiddenID = document.createElement("div")
            hiddenID.textContent = element.resource_id;
            hiddenID.style.display = "none";

            const hiddenPath = document.createElement("div")
            hiddenPath.textContent = element.path;
            hiddenPath.style.display = "none";

            const nameElement = document.createElement("div");
            nameElement.className = "d2";
            nameElement.textContent = element.resource_name + element.suffix_name;

            const dateElement = document.createElement("div");
            dateElement.className = "d4";
            const createdDate = new Date(element.created_at);
            dateElement.textContent = createdDate.toLocaleString();

            const bookmarkElement = document.createElement("div");
            bookmarkElement.className = "d3";

            const bookmarkImage = document.createElement("img");
            bookmarkImage.src = "/static/img/bookmark_be.png";
            bookmarkImage.style.width = "20px";
            bookmarkImage.style.height = "20px";

            bookmarkElement.appendChild(bookmarkImage);

            fileElement.appendChild(checkboxDiv);
            fileElement.appendChild(hiddenID);
            fileElement.appendChild(hiddenPath);
            fileElement.appendChild(nameElement);
            fileElement.appendChild(dateElement);
            fileElement.appendChild(bookmarkElement);

            fileListElement.appendChild(fileElement);
        });
    })
    .catch(error => {
        console.log(error);
    });
}
// 파일 클릭 이벤트 핸들러
function handleFileInfoClick(element) {
    document.querySelector('.name span').textContent = element.resource_name;
    document.querySelector('.i1-2 p').textContent = element.suffix_name;
    document.querySelector('.i2-2 p').textContent = element.path;
    document.querySelector('.i3-2 p').textContent = formatBytes(element.size);
    document.querySelector('.i4-2 p').textContent = new Date(element.created_at);
}

function handleFileDelete() {
    const accessToken = getToken();
    var checkboxes = document.querySelectorAll(".check:checked");
    checkboxes.forEach((checkbox)=>{
        fetch(fullURL + '/files/realdelete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                'path': `${checkbox.parentNode.nextSibling.nextSibling.textContent}${checkbox.parentNode.nextSibling.nextSibling.nextSibling.textContent}`,
                'resource_id': `${checkbox.parentNode.nextSibling.textContent}`
        })
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error('삭제 요청에 실패했습니다');
            }
        })
        .catch(error => {
            console.error();
        });
    });
    setTimeout(() => fetchTrashList(), 1000);
}

function handleFileRecover() {
    const accessToken = getToken();
    var checkboxes = document.querySelectorAll(".check:checked");
    checkboxes.forEach((checkbox)=>{
        fetch(fullURL + '/files/recover/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                'resource_id': `${checkbox.parentNode.nextSibling.textContent}`
        })
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error('삭제 요청에 실패했습니다');
            }
        })
        .catch(error => {
            console.error();
        });
    });
    setTimeout(() => fetchTrashList(), 1000);
}