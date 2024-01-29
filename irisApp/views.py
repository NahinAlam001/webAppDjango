from django.shortcuts import render

from joblib import load
model = load('./savedModels/model.joblib')

def main(request):
    if request.method == "POST":
        spl = request.POST['spl']
        spw = request.POST['spw']
        ptl = request.POST['ptl']
        ptw = request.POST['ptw']

        y_pred = model.predict([[spl, spw, ptl, ptw]])

        if y_pred[0] == 0:
            y_pred = 'Setosa'
        elif y_pred == 1:
            y_pred = 'Versicolor'
        else:
            y_pred = 'Verginica'

        return render(request, 'irisApp/main.html', {'result': y_pred})
    return render(request, 'irisApp/main.html')