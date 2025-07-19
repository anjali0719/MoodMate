import os
import json
from dotenv import load_dotenv
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from openai import OpenAI
from journals.models import JournalEntry, ChatSession
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
            return JsonResponse({'message': "Please enter something to get started"}, status=400)
        
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": 'user',
                    'content': user_input
                }
            ]
        )

        chat_session_id = data.get("chat_session_id", None)
        if not chat_session_id:
            chat_session = ChatSession.objects.create(title=generate_title(user_input))
        else:
            chat_session = ChatSession.objects.get(id=chat_session_id)

        journal_entry = JournalEntry.objects.create(
            input_text=user_input,
            response_text=completion.choices[0].message.content,
            chat_session=chat_session
        )

        # context = {
        #     'user_input': journal_entry.input_text,
        #     'response_msg': journal_entry.response_text,
        # }

        return JsonResponse({
            'error': False,
            'response': completion.choices[0].message.content,
            'journal_id': journal_entry.id,
        })
        
        # return render(request, template_name='journals/chat.html', context=context)

    
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

    # create_schema func can be called on conditional basis
    try:
        # reindexing:
        # journal_obj = JournalEntry.objects.all()
        # for obj in journal_obj:
        #     typesense_client.collections['journal_entries'].documents.upsert({
        #         'id': str(obj.id),
        #         'journal_title': obj.journal_title,
        #         'input_text': obj.input_text,
        #         'response_text': obj.response_text,
        #         'created_at': int(obj.created_at.timestamp())
        #     })
            
        results = typesense_client.collections['journal_entries'].documents.search(search_parameters)
        return JsonResponse({ 'results': results })
    except Exception as e:
        print(f"Something went wrong in search: {e}")
        return { 'results': [] }


def chat(request):
    chat_sessions = ChatSession.objects.all().order_by('-created_at')
    return render(request, 'journals/chat.html', {'chat_sessions': chat_sessions})


@require_GET
@csrf_exempt
def chat_list(request):
    # As of now, we use context to send the chat session on nav bar, so this may not be reqd
    # Nav Bar: ChatSessions
    # chat_sessions = ChatSession.objects.all().order_by('-created_at')

    # res = {
    #     'chat_list': list(chat_sessions.values('id', 'title'))
    # }
    res = {}

    # Open a chat
    chat_session_id = request.GET.get('chat_session_id', None)
    if chat_session_id:
        try:
            session_obj = ChatSession.objects.get(id=chat_session_id)
            chat_entry = JournalEntry.objects.filter(chat_session=session_obj).order_by('created_at')

            res['chat_obj'] = list(chat_entry.values('id', 'input_text', 'response_text', 'created_at'))
        
        except ChatSession.DoesNotExist:
            return JsonResponse({
                'error': 404,
                'message': f"No chat with Id: {chat_session_id} exists in our record"
            }, status= 404)
    
    return JsonResponse(res, safe=False)
