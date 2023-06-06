function login(){
    passwd_value = document.querySelector('#code').value; //text input value
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
						document.cookie='passwd=' + passwd_value;
						alert("로그인 성공!");
						location.href="http://" + location.host + "/guest_mode/"; //로그인 후 다음페이지
					}
					else
					{
						alert("유저 없음!"); // 알림
					}
				})
}


function generate_guest()
{
	fetch("http://localhost:8000/guest/generate/") //백엔드 주소로 바꿔야함
		.then(res => res.json())
		.then(data => {
			document.cookie = `passwd=${data.passwd}; path=/`;
			window.location.href="http://" + location.host+"/guest_mode"; // generate 후에 파일 저장 페이지
		}) //passwd 쿠키저장
}
