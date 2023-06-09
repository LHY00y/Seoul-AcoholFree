from django.shortcuts import render
# Create your views here.


def index(request):
    # request.id 랑 같은 코드의 경찰서 정보가져오기
    # context에 정보 넘기기

    return render(request, 'map/index.html')