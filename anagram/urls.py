from django.urls import path, re_path
from . import views

urlpatterns = [
    path('words/', views.wordManagement, name='words'),
    path('words/<str:word>/', views.deleteWord, name='deleteWord'),
    path('anagrams/<str:word>/', views.getAnagrams, name='anagrams'),
    path('statistics/', views.getStatistics, name='statistics'),
    path('compare/', views.wordsCompare, name='wordsCompare'),
    path('most-anagrams/', views.getMostAnagrams, name='getMostAnagrams'),
    path('anagrams-group/<int:size>', views.getAnagramsGroup, name='getAnagramsGroup'),
    path('delete/<str:word>', views.deleteAnagrams, name='deleteAnagrams'),
]