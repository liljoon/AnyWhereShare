"use strict";

const logInBtn = document.getElementById("logIn");
const guestModeBtn = document.getElementById("guestMode");
const createAccountBtn= document.getElementById("createAccount");

function moveToLogin(){
    location.href= "login/";
}

function guestLogin(){
    passwd_value = document.querySelector('#passwd').value; //text input value
		fetch("http://localhost:8000/guest/login/", {
				method: "POST",
				headers : {
					"Content-Type" : "application/json",
				},
				body: JSON.stringify({
					passwd : passwd_value
				})
				})
				.then(res => {
					if (res.status == 200)
					{
						document.cookie='passwd='+data.passwd_value
						alert("로그인 성공!");
						window.location.href=location.host+"/next"; //로그인 후 다음페이지
					}
					else
					{
						alert("유저 없음!"); // 알림
					}

				})
}


function moveToCreate(){
    location.href = "create/";
}

logInBtn.addEventListener('click',moveToLogin);
guestModeBtn.addEventListener('click',guestLogin);
createAccountBtn.addEventListener('click', moveToCreate);