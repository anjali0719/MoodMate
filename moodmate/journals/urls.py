from django.urls import path
from journals.views import analyze_mood, search_journal_entries, student_form

urlpatterns = [
    path("analyze-mood/", analyze_mood, name="analyze-mood"),
    path('search-entries/', search_journal_entries, name="search-journal-entries"),
    # path('student-form/', student_form, name="student-form"),
]
