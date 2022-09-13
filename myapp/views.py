from contextvars import Context
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.style import context
from .models import person

from django.core.files.storage import FileSystemStorage

import torch
import os
from torchvision import transforms
from PIL import Image

from .insect import Klook , pchome

# Create your views here.
#def callname(request):
    #return HttpResponse('<h1>hello world</h1>')

#def callperson(request):
    #personaaa = person.objects.all()
    
    #context={
    #    'personaaa':personaaa,
    #}
    #return render(request,"person.html",context)

def predict_CatandDog(path):
    path = path
    test_pred_transforms = transforms.Compose([
        transforms.Resize((360 , 360)) , 
        transforms.ToTensor() , 
        transforms.Normalize((0 , 0 , 0) , (1 , 1 , 1))
    ])
    model = torch.load(".\myapp\model.pth",map_location=lambda storage, loc: storage) #如果GPU訓練CPU跑要加 map_location=torch.device("CPU")
    

    #img_item_path = os.path.join(".\media", path)
    img = Image.open(path)
        
    img_ts = test_pred_transforms(img)
    img_ts = torch.reshape(img_ts, (1, 3, 360, 360))
    output = model(img_ts)
    label = output.round().cpu()
    ch_label = "dog" if int(label)==1 else "cat"

    return ch_label

def indextest(request):
    print(request)
    print(request.POST.dict())
    if request.method == 'POST' and 'filepath' in request.FILES:
        fileObj=request.FILES['filepath']
        fs = FileSystemStorage()
        filepathname=fs.save(fileObj.name, fileObj)
        filepath = os.path.join(".\media", str(fileObj.name))
        filepathnameee = fs.url(filepathname)
        labelll = predict_CatandDog(filepath)
        context={'labelll':labelll,'filepathname':filepathnameee}
        return render(request,"index.html",context)
    else:
        return render(request,"index.html",{'labelll':"nothing",'filepathname':"http://127.0.0.1:8000/media/nothing.png"})


def insect(request):
    #klook = Klook(request.POST.get("city_name"))
    #kkday = Kkday(request.POST.get("city_name"))
    Pchome = pchome(request.POST.get("city_name"))
 
    context = {
        "tickets": Pchome.scrape() #kkday.scrape()
    }
 
    return render(request, "tickets/indexxx.html", context)







