from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Calculator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return User.objects.first()  


def calculator_view(request):
    user = get_user(request)

    if request.method == "POST":
        expression = request.POST.get("expression")

        try:
            result = str(str + int(expression))
        except:
            result = "Xatolik"

        Calculator.objects.create(
            user=user,
            expression=expression,
            result=result
        )

        return redirect('home')

    calculations = Calculator.objects.filter(user=user)

    return render(request, 'dizayn.html', {
        'calculations': calculations
    })

@csrf_exempt
def calculate_api(request):
    if request.method == "POST":
        user = get_user(request)

        try:
            data = json.loads(request.body)
            expression = data.get("expression")

            result = str(eval(expression))

            calc = Calculator.objects.create(
                user=user,
                expression=expression,
                result=result
            )

            return JsonResponse({
                "id": calc.id,
                "expression": expression,
                "result": result
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def history_api(request):
    user = get_user(request)

    calculations = Calculator.objects.filter(user=user).values(
        'id', 'expression', 'result', 'created_at'
    )

    return JsonResponse(list(calculations), safe=False)