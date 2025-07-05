# services/views/payme.py
from rest_framework import views, response
from config import settings
from services.payment import create_payment_session
from services.serializers import PaymentSerializer
from users.models import UserModel 

from payme import Payme

payme = Payme(payme_id=settings.PAYME_ID)

class PaymentCreate(views.APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        user_id = request.data.get('user_id')  # foydalanuvchini qo‘lda olamiz

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return response.Response({'detail': "Foydalanuvchi topilmadi"}, status=404)

        session = create_payment_session(user)

        if not session:
            return response.Response({'detail': "To‘lanmagan buyurtma yo‘q"}, status=400)

        # ❗ Asosan o‘zgargan joy shu:
        serializer = self.serializer_class(instance=session)

        payment_link = payme.initializer.generate_pay_link(
            id=session.id,
            amount=int(session.total_amount), 
            return_url='https://t.me/asadmaxmud_bot'
        )

        print(f"Amount {int(session.total_amount)}, Asl => {session.total_amount}")

        return response.Response({
            'payment': serializer.data,
            'payment_link': payment_link
        })