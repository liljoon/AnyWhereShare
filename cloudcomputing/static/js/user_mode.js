//전역변수 : 현재 폴더 위치
//처음 path="/"
//토큰 accessToken =""

window.onload = function(){
    fetchFileList();

    const fileInput = document.getElementById('file');
    const uploadButton = document.getElementById('uploadButton');
    const downloadButton = document.getElementById('downloadButton');
    const deleteButton = document.getElementById('deleteButton');
    const folderButton = document.getElementById('folderButton');
    fileInput.addEventListener('change', () => {handleFileUpload();});
    uploadButton.addEventListener('click', () => {fileInput.click();});
    downloadButton.addEventListener('click', () => {handleFileDownload();});
    deleteButton.addEventListener('click', () => {handleFileDelete();});
    folderButton.addEventListener('click', () => {handleFolderCreate();});
}
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return ((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function login() {
    fetch('http://localhost:8000/accounts/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: 'abc123',
            password: 'khu2023'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.cookie = `accessToken=${data.token}; path=/`;
        document.cookie = 'path=/; path=/';
    })
    .catch(error => {
        console.log(error)
    });
}

function getPath() {

    const cookie = document.cookie;
    const pathStartIndex = cookie.indexOf("path=");
    if (pathStartIndex > -1) {
        const pathEndIndex = cookie.indexOf(";", pathStartIndex);
        if (pathEndIndex > -1) {
            return cookie.substring(pathStartIndex + 5, pathEndIndex);
        } else {
            return cookie.substring(pathStartIndex + 5);
        }
    }
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
function fetchFileList() {

    const path = getPath();
    const accessToken = getToken();
    const fileListElement = document.getElementById("show");
    fileListElement.innerHTML = '';

    if(path != "/"){
        const fileElement = document.createElement("div");
        fileElement.className = "uploaded_file";
        const nameElement = document.createElement("div");
                nameElement.className = "d2";
                nameElement.textContent = '..';
                nameElement.addEventListener("click",
                () => {handleFileDoubleClick('..');});
        fileElement.appendChild(nameElement);
        fileListElement.appendChild(fileElement);
    }

    fetch('http://localhost:8000/files/list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            path: path
        })
    })
    .then(response => response.json())
    .then(data => {
        data.forEach((element) => {
            if(element.is_valid == 0)
                return;
            if(element.resource_name == '')
                return;
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

            const nameElement = document.createElement("div");
            nameElement.className = "d2";
            nameElement.textContent = element.resource_name + element.suffix_name;
            nameElement.addEventListener("dblclick",
            () => {handleFileDoubleClick(element.resource_name + element.suffix_name);});

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
// 파일 더블클릭 이벤트 핸들러
function handleFileDoubleClick(fileName) {

  let path = getPath()

    if(fileName.includes('.')){
        if(fileName == '..'){
            const parts = path.split("/");
            if (parts.length <= 2) {
                document.cookie = `path=/; path=/`;
                fetchFileList();
            }
            else {
                parts.pop();
                parts.pop();
                document.cookie = `path=${parts.join("/") + "/"}; path=/`;
                fetchFileList();
            }
        }
    }
    else {
        // 쿠키의 path 값을 파일명으로 업데이트
        if(path =="/"){
            path = fileName + "/";
            document.cookie = `path=${path}; path=/`;
        } else {
            path += fileName + "/";
            document.cookie = `path=${path}; path=/`;
        }
        fetchFileList();
    }
}

function handleFileDownload() {
    var path = getPath();
    const accessToken = getToken();

    if(path == "/")
    path = "";
    
    var checkboxes = document.querySelectorAll(".check:checked");
    checkboxes.forEach((checkbox)=>{
        fetch('http://localhost:8000/files/download/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                'path': `${path}${checkbox.parentNode.nextSibling.textContent}`
            })
        })
        .then(response => {
            if (response.status === 200) {
                fetchFileList();
                return response.blob();
            } else {
                throw new Error('다운로드 요청에 실패했습니다');
            }
        })
        .then(blob => {
            // Blob을 파일로 저장하거나 다른 방식으로 파일 다운로드를 처리할 수 있습니다.
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = checkbox.parentNode.nextSibling.textContent; // 다운로드할 파일의 이름을 지정합니다.
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error();
        });
    });
}

function handleFileUpload() {
    var path = getPath();
    const accessToken = getToken();

    if(path == "/")
        path = "";

    const fileInput = document.getElementById('file');
    const file = fileInput.files[0]; // 파일 객체 가져오기
    const formData = new FormData(); // FormData 객체 생성
    formData.append('file', file); // 파일 객체 추가
    formData.append('path', path); // path 값 추가

    fetch('http://localhost:8000/files/upload/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`
        },
        body: formData
    })
    .then(response => {
        if (response.status === 201) {
            fetchFileList();
            return response.json();
        } else {
            throw new Error('업로드 요청에 실패했습니다');
        }
    })
    .catch(error => {
        console.error();
    });
}

function handleFileDelete() {
    var path = getPath();
    const accessToken = getToken();
    var checkboxes = document.querySelectorAll(".check:checked");
    if(path == "/")
        path = "";
    checkboxes.forEach((checkbox)=>{
        fetch('http://localhost:8000/files/delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                'path': `${path}${checkbox.parentNode.nextSibling.textContent}`
        })
        })
        .then(response => {
            if (response.status === 200) {
                fetchFileList();
                return response.json();
            } else {
                throw new Error('삭제 요청에 실패했습니다');
            }
        })
        .catch(error => {
            console.error();
        });
    });
}

function handleFolderCreate() {
    var path = getPath();
    var name = prompt('생성할 폴더의 이름을 입력하세요:');
    const accessToken = getToken();
    fetch('http://localhost:8000/files/newfolder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                'name': name,
                'path': path
        })
        })
        .then(response => {
            if (response.status === 200) {
                fetchFileList();
                return response.json();
            } else {
                throw new Error('폴더생성 요청에 실패했습니다');
            }
        })
        .catch(error => {
            console.error();
        });
}
/*
[
    {
        "resource_id": 1,
        "resource_name": "test",
        "resource_type": "D",
        "suffix_name": "",
        "path": "",
        "is_bookmark": 0,
        "is_valid": 1,
        "created_at": "2023-06-01T21:16:02.606362+09:00",
        "modified_at": "2023-06-01T21:18:01.062931+09:00",
        "size": 2930921,
        "parent_resource_id": null,
        "user_account_id": "abc123"
    }
]
*/

/*

    "resource_id": 8,
    "resource_name": "Update",
    "resource_type": "F",
    "suffix_name": ".exe",
    "path": "test/",
    "is_bookmark": 0,
    "is_valid": 1,
    "created_at": "2023-06-01T21:18:01.057729+09:00",
    "modified_at": "2023-06-01T21:18:01.057764+09:00",
    "size": 1522176,
    "parent_resource_id": 1,
    "user_account_id": "abc123"

*/
