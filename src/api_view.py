from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # Hamma uchun ruxsat
from .models import Calculator
from .serializer import CalculatorSerializer
import re
import google.generativeai as genai

# 1. Oddiy Kalkulyator API
class CalculatorAPI(APIView):
    permission_classes = [AllowAny] # Endi login so'ramaydi

    def get(self, request):
        calculations = Calculator.objects.all().order_by('-created_at')
        serializer = CalculatorSerializer(calculations, many=True)
        return Response(serializer.data)

    def post(self, request):
        expression = request.data.get('expression', '')
        clean_expr = re.sub(r'[^0-9+\-*/.()]', '', expression)

        try:
            if not clean_expr:
                return Response({"error": "Ifoda bo'sh"}, status=400)
            result = str(eval(clean_expr))
        except Exception:
            return Response({"error": "Noto'g'ri ifoda"}, status=400)

        # Login qilgan bo'lsa user-ni ulaydi, qilmagan bo'lsa None (bazada null bo'ladi)
        user = request.user if request.user.is_authenticated else None

        calc = Calculator.objects.create(
            user=user,
            expression=expression,
            result=result
        )

        serializer = CalculatorSerializer(calc)
        return Response(serializer.data, status=200)

# 2. Gemini AI Kalkulyator API
genai.configure(api_key="AIzaSyBxWR9t8_-u4mJnzN5QyiXUDnQ2gep0WIE")
# Modelni gemini-1.5-flash qildim, chunki u ancha tez va barqaror
model = genai.GenerativeModel('gemini-2.5-flash-lite')

class GeminiKalkulator(APIView):
    permission_classes = [AllowAny] # Bu ham hamma uchun ochiq

    def post(self, request):
        expression = request.data.get('expression', '')
        if not expression:
            return Response({"error": "Savol yozilmadi"}, status=400)

        prompt = f"""
        Sen aqlli matematik yordamchisan. 
        Foydalanuvchi so'rovi: {expression}
        Faqat natijani va qisqacha izohni qaytar. 
        Javobingni O'zbek tilida ber.
        """

        try:
            response = model.generate_content(prompt)
            result = response.text
        except Exception as e:
            result = f"Gemini xatosi: {str(e)}"

        user = request.user if request.user.is_authenticated else None

        Calculator.objects.create(
            user=user,
            expression=expression,
            result=result
        )

        return Response({
            "expression": expression,
            "result": result,
            "engine": "Google Gemini AI"
        })


