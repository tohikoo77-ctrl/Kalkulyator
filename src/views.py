from django.shortcuts import render, redirect
from .models import Calculator

def calculator_view(request):
    if request.method == "POST":
        expression = request.POST.get("expression")

        try:
            result = str(eval(expression))
        except:
            result = "Xatolik"

        Calculator.objects.create(
            user=request.user,
            expression=expression,
            result=result
        )

        return redirect('calculator')

    calculations = Calculator.objects.filter(user=request.user)

    return render(request, 'dizayn.html', {
        'calculations': calculations
    })