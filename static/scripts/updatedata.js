
    requestCPU()
    requestSwap()
    requestVirt()
    setInterval(function(){requestCPU(); requestVirt();requestSwap()},5000);

    function requestCPU(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','./cpuusage',true);
        xhr.send();
        xhr.onreadystatechange=function(){
            if(xhr.status==200){
                cpuusage.style.width=xhr.response+"%";   
                cpuusage.innerText=xhr.response+"%"
                if(xhr.response>75)
                    cpuusage.style.backgroundColor="#e77f67";
                else
                    cpuusage.style.backgroundColor="#63cdda";
            }
        }
    }

    function requestVirt(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','./virtualusage',true);
        xhr.send();
        xhr.onreadystatechange=function(){
            if(xhr.status==200){
                virtusage.style.width=xhr.response+"%";   
                virtusage.innerText=xhr.response+"%"
                if(xhr.response>75)
                    virtusage.style.backgroundColor="#e77f67";
                else
                    virtusage.style.backgroundColor="#63cdda";
            }
        }
    }

    function requestSwap(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','./swapusage',true);
        xhr.send();
        xhr.onreadystatechange=function(){
            if(xhr.status==200){
                swapusage.style.width=xhr.response+"%";   
                swapusage.innerText=xhr.response+"%"
                if(xhr.response>75)
                    swapusage.style.backgroundColor="#e77f67";
                else
                    swapusage.style.backgroundColor="#63cdda";
            }
        }
    }