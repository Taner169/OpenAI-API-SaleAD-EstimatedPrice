from django.shortcuts import render
from .models import SaleAd
from django.core.files.storage import FileSystemStorage
import openai

openai.api_key = 'Your OpenAI Key' 

def send_prompt_to_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        return "An error occurred while getting a response from ChatGPT."

def sale_ad_view(request):
    context = {}
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        details = request.POST.get('details', '').strip()

        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

      
        description_prompt = f"beskriv objected på beskrivningen {details} och på bilden {uploaded_file_url}, Inkludera attribut såsom material, färgschema och eventuella speciella egenskaper, Avsluta med ett sammanfattande stycke som fångar varans försäljningspunkter på ett övertygande sätt, och nämn eventuella tecken på slitage om sådana finns. Sök upp denna bild på finn.no och blocket.se och ge ungefärlig pris på varan på bilden. Skippa upladdade bildens namn. max 200 ord"

        description = send_prompt_to_chatgpt(description_prompt)

        new_ad = SaleAd(title=details, image=filename, description=description)
        new_ad.save()

        context = {
            'uploaded_file_url': uploaded_file_url,
            'description': description
        }

    return render(request, 'saleads/index.html', context)
