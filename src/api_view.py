from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Calculator
from .serializer import CalculatorSerializer
import re

class CalculatorAPI(APIView):
    # Если хочешь, чтобы API видели все, ставь AllowAny
    permission_classes = [AllowAny]

    def get(self, request):
        """Получаем всю историю вычислений"""
        calculations = Calculator.objects.all().order_by('-created_at')
        serializer = CalculatorSerializer(calculations, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Принимаем выражение, считаем и сохраняем"""
        expression = request.data.get('expression', '')

        # 1. Очистка (безопасность)
        clean_expr = re.sub(r'[^0-9+\-*/.()]', '', expression)

        # 2. Расчет
        try:
            if not clean_expr:
                raise ValueError("Bo'sh ifoda")
            result = str(eval(clean_expr))
        except Exception:
            return Response({"error": "Invalid expression"}, status=400)

        # 3. Сохранение (если юзер не залогинен, ставим None)
        user = request.user if request.user.is_authenticated else None
        calc = Calculator.objects.create(
            user=user,
            expression=expression,
            result=result
        )

        serializer = CalculatorSerializer(calc)
        return Response(serializer.data, status=200)


