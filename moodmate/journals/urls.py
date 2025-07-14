from django.urls import path
from journals.views import analyze_mood, search_journal_entries, chat

urlpatterns = [
    path("analyze-mood/", analyze_mood, name="analyze-mood"),
    path('search-entries/', search_journal_entries, name="search-journal-entries"),
    path('chat/', chat, name="chat"),
]
