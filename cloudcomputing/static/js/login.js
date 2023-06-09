 "use strict";

const loginId = document.getElementById('LOGIN_ID');
const loginPw = document.getElementById('LOGIN_PW');
const loginBtn = document.getElementById('LOGIN_BTN');

var currentProtocol = location.protocol; // 현재 프로토콜 (예: "http:", "https:")
var currentHost = location.host; // 현재 호스트 (예: "example.com", "localhost:3000")

var fullURL = currentProtocol + '//' + currentHost;

function color() {
    if((loginId.value.length>0 && loginId.value.indexOf("@")!==-1)
        && loginPw.value.length>=5){
        loginBtn.style.backgroundColor = "#0095F6";
        loginBtn.disabled = false;
    }else{
        loginBtn.style.backgroundColor = "#C0DFFD";
        loginBtn.disabled = true;
    }
}

function login() {
  const userId = document.getElementById('id1').value;
  const password = document.getElementById('pw').value;

    fetch(fullURL + '/accounts/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: userId,
            password: password
        })
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status === 401) {
            throw new Error('아이디 또는 패스워드가 틀립니다');
        } else {
            throw new Error('로그인 요청에 실패했습니다');
        }
    })
    .then(data => {
        console.log('로그인 성공')
        document.cookie = `accessToken=${data.token}; path=/;`;
        document.cookie = 'path=/; path=/;';
        window.location.href = fullURL + '/user_mode/';
    })
    .catch(error => {
        alert('아이디 또는 패스워드가 틀립니다');
    });
}

function moveToMain(){
    location.replace("./main.html");
}

loginId.addEventListener('keyup', color);
loginPw.addEventListener('keyup', color);
loginBtn.addEventListener('click',moveToMain);
