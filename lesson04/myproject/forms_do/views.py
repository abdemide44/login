from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
# Create your views here.
def form1(request):
    if request.method=='POST':
        form=NameForm(request.POST);
        if form.is_valid() :
            name=form.cleaned_data['your_name'];
            return HttpResponse(f"you name is {name}")
        
        return render(request,'forms_do/name.html',{'form':form});
    form=NameForm();
    return render(request,'forms_do/name.html',{'form':form});