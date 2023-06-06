"use strict";

const logInBtn = document.getElementById("logIn");
const guestModeBtn = document.getElementById("guestMode");
const createAccountBtn= document.getElementById("createAccount");

function moveToLogin(){
    location.href= "login/";
}

function guestLogin(){
    location.href="guest_login/";
}


function moveToCreate(){
    location.href = "create/";
}

logInBtn.addEventListener('click',moveToLogin);
guestModeBtn.addEventListener('click',guestLogin);
createAccountBtn.addEventListener('click', moveToCreate);
