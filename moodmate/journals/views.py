import os
import json
from dotenv import load_dotenv
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from openai import OpenAI
from journals.models import JournalEntry
from journals.search import typesense_client

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Create your views here.
def generate_title(user_input):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short, engaging titles for journal entries."
                },
                {
                    "role": "user",
                    "content": f"Generate a short and meaningful title for the following journal entry:\n\n{user_input}"
                }
            ]
        )
        title = completion.choices[0].message.content.strip()
        return title
    except Exception as e:
        # Fallback if LLM fails
        print(f"Error while generating the title: {e}")
        return "Untitled Journal"


@require_POST
@csrf_exempt
def analyze_mood(request):
    data = json.loads(request.body)
    try:
        user_input = data.get("user_input", None)
        if not user_input:
            return HttpResponse("Please enter something to get started")
        
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": 'user',
                    'content': user_input
                }
            ]
        )

        journal_entry = JournalEntry.objects.create(
            input_text=user_input,
            journal_title=generate_title(user_input),
            response_text=completion.choices[0].message.content
        )

        context = {
            'user_input': journal_entry.input_text,
            'response_msg': journal_entry.response_text,
            'journal_title': journal_entry.journal_title
        }
        
        return render(request, template_name='journals/student.html', context=context)
    
    except Exception as e:
        print(f"Something went wrong, while processing the request: {e}")
        return HttpResponse("Something went wrong, please try again later")


@require_GET
@csrf_exempt
def search_journal_entries(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({ 'results': [] })
    
    search_parameters = {
        'q': query,
        'query_by': 'input_text,response_text',
        'sort_by': 'created_at:desc'
    }

    # signal might have given error while schema creation - check how it can be fixed
    # check if search api key is required? or admin key will work
    # create_schema func can be called on conditional basis
    try:
        results = typesense_client.collections['journal_entries'].documents.search(search_parameters)
        return JsonResponse({ 'results': results })
    except Exception as e:
        print(f"Something went wrong in search: {e}")
        return { 'results': [] }


def student_form(request):
    return render(request, 'journals/student.html')
