window.onload=function(){
    //head에 직성할때 써야 하는 코드

            var id1= document.querySelector('#id1')
            var pwMsg = document.querySelector('#pwMsg');

            pwMsg.style.fontWeight="bold";
            regId=/^[A-Z][a-zA-Z0-9]{4,}$/

            id1.addEventListener("blur",function(){
                if(!regId.test(id1.value)){
                        alert("아이디는 5글자 이상 첫글자는 대문자이고 영문자, 숫자만 가능 ")
                        id1.value="";

                    }
            })


            document.querySelector('#subm').onclick=function(){
                if(id1.value==""){
                    alert("아이디를 입력하세요")
                    return false

                }else{
                    if(!regId.test(id1.value)){
                        alert("아이디는 5글자 이상 첫글자는 대문자이고 영문자, 숫자만 가능 ")
                        id1.value="";
                        return false;
                    }
                }
                createAccount();

            }

            document.querySelector('#pw2').addEventListener("focus",function(){
                if(document.querySelector('#pw').value==""){
                    alert("패스워드를 먼저 입력하세요");
                    document.querySelector('#pw').focus()
                }

            })

            document.querySelector('#pw2').addEventListener("blur",function(){
            if(document.querySelector('#pw').value != document.querySelector('#pw2').value){
                    pwMsg.style.color="red";
                    pwMsg.innerHTML="비밀번호가 일치하지 않습니다."
                    return false;
                }else if(document.querySelector('#pw').value==""){}
                else{
                    pwMsg.style.color="green";
                    pwMsg.innerHTML="비밀번호가 일치합니다."
                }



            })
        }

function createAccount() {
  // 사용자 입력값 가져오기
  const userId = document.getElementById('id1').value;
  const password = document.getElementById('pw').value;
  const username = document.getElementById('name').value;
  const email = document.getElementById('email').value;

  // 요청 보내기
  fetch('http://localhost:8000/accounts/signup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "user_id": userId,
      "password": password,
      "username": username,
      "email": email
    })
  })
    .then(response => {
        
        if (response.status === 201) {
            window.location.href = 'http://localhost:8000/login/';
        } else if (response.status === 400) {
            throw new Error('입력 조건에 맞지 않습니다');
        } else {
            throw new Error('회원가입 요청에 실패했습니다');
        }
    })
    .catch(error => {
      // 오류 처리
      console.error('요청 중 오류가 발생했습니다:', error);
    });
}
