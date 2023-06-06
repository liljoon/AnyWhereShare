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