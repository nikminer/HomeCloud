var cpu=document.getElementById("cpuusage");
    requestCPU()
    setInterval(function(){requestCPU()},5000);

    function requestCPU(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','./cpuusage',true);
        xhr.send();
        xhr.onreadystatechange=function(){
            if(xhr.status==200){
                cpu.style.width=xhr.response+"%";   
                cpu.innerText=xhr.response+"%"
                if(xhr.response>75)
                    cpu.style.backgroundColor="#e77f67";
                else
                    cpu.style.backgroundColor="#63cdda";
            }else{
                
                console.log(xhr.statusText  );
            }
        }
    }