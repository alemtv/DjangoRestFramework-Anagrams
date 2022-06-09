from rest_framework import serializers
from anagram.models import Wordbook, Anagram


class WordbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordbook
        fields = ['word']


class AnagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anagram
        fields = ['word_list','anagrams_count']