import json
import openai
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# Configura la tua chiave API di OpenAI
openai.api_key = settings.OPENAI_API_KEY

# ID del modello che desideri utilizzare
MODEL_ID = 'gpt-4'

# La tua vista chat esistente
def chat(request):
    return render(request, 'chat.html')

@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        message = data.get('message')

        try:
            # Comunicazione con OpenAI e ricezione della risposta
            response = openai.ChatCompletion.create(
                model=MODEL_ID,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert lawyer well-versed in all areas of Italian law."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=0.2,
                max_tokens=990
            )

            # Estrai il messaggio dalla risposta
            bot_reply = response.choices[0].message.content.strip()

            # Restituzione della risposta al frontend
            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            print(e)
            return HttpResponseServerError(str(e))

def upload_tuning_file(request):
    if request.method == "POST":
        try:
            with open("fine-tuning.json", "rb") as f:
                response = openai.File.create(file=f, purpose="fine-tuning")
            return JsonResponse({"file_id": response.id})
        except Exception as e:
            return HttpResponseServerError(str(e))
    else:
        return render(request, 'upload.html')
