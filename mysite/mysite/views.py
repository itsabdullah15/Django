# I created this file #Abdullah
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
    # return HttpResponse("hello <a href='https://www.google.com'>Google</a>")


def about(request):
    return HttpResponse("About Abdullah")

def analyze(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Get the checkbox
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charactercounter = request.POST.get('charactercounter', 'off')

    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        param = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', param)

    if fullcaps == "on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()
        param = {'purpose': 'Changed to uppercase', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', param)

    if newlineremover == "on":
        analyzed = ""
        for char in djtext:
            if char != '\n' and char!='\r':
                analyzed = analyzed + char
        param = {'purpose': 'New line is removed', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', param)
    
    if extraspaceremover == "on":
        analyzed=""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):
                analyzed = analyzed + char
        param = {'purpose': 'Space is removed', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', param)
    
    if charactercounter == "on":
        analyzed = 0
        for char in djtext:
            if char != " ":
                analyzed += 1
        
        param = {'purpose': 'Character Counter', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', param)
    if(removepunc != "on" and fullcaps != "on" and extraspaceremover != "on" and newlineremover != "on" and charactercounter != "on"):
        return HttpResponse("please select any operation and try again")

    return render(request, 'analyze.html', param)
