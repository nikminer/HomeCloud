from django.shortcuts import redirect

def handle_uploaded_file(f,path,request):
    with open(path+'/'+str(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return redirect("http://"+request.get_host()+"/file/explorer"+path)