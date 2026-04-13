from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializer import CalculatorSerializer
from .models import Calculator
import re

class Kalkulator(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculatorSerializer

    def get_queryset(self):
        return Calculator.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        expression = self.request.data.get('expression')
        clean_expression = re.sub(r'[^0-9+\-*/.()]', '', expression)

        try:
            result = str(eval(clean_expression))
        except Exception as e:
            result = "Error"

        serializer.save(user=self.request.user, result=result, expression=expression)