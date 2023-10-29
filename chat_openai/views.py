import json  # Importa il modulo json
import openai  # Importa il modulo openai
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# Configura la tua chiave API di OpenAI
openai.api_key = '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'

# ID del modello fine-tuned
FINE_TUNED_MODEL_ID = 'YOUR_FINE_TUNED_MODEL_ID'

# La tua vista chat esistente
def chat(request):
    return render(request, 'chat.html')

# Una vista basata su classe per gestire le richieste AJAX dalla tua chat
@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)  # Deserializza il corpo della richiesta
        message = data.get('message')

        try:
            # Comunicazione con OpenAI e ricezione della risposta
            response = openai.ChatCompletion.create(
                model=FINE_TUNED_MODEL_ID,
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
                max_tokens=1000  # Se desideri limitare la risposta, puoi decommentare questa linea
            )

            # Estrai il messaggio dalla risposta
            bot_reply = response.choices[0].message.content.strip()

            # Restituzione della risposta al frontend
            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            # Gestione degli errori per qualsiasi problema nell'interazione con l'API
            print(e)  # Aggiungi questa linea
            return HttpResponseServerError(str(e))

# Nuova vista per caricare il file di fine-tuning
def upload_tuning_file(request):
    if request.method == "POST":
        try:
            with open("fine-tuning.json", "rb") as f:
                response = openai.File.create(file=f, purpose="fine-tuning")
            return JsonResponse({"file_id": response.id})
        except Exception as e:
            return HttpResponseServerError(str(e))
    else:
        return render(request, 'upload.html')  # una semplice pagina per l'upload se desideri averla
