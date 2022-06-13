from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max, Min
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from anagram.models import Wordbook, Anagram
from .serializers import WordbookSerializer, AnagramSerializer


@api_view(['GET'])
def getAnagrams(request, word):
    limit = 0    # an optional query param that indicates the maximum number of results to return

    # get anagram_key value which will be used for data selection
    anagram = ''.join(sorted(word))

    # get optional query param ?limit=1
    try:
        if request.query_params: limit = int(request.query_params['limit'])
    except Exception:
        print(f" Bad request: {word}/{request.query_params} ")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        # get word list by anagram_key
        obj = Anagram.objects.get(anagram_key=anagram)
    except Exception:
        return Response({'anagrams': []}, status=status.HTTP_200_OK)

    return Response({'anagrams': obj.get_anagram_list(word, limit)}, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
def wordManagement(request):
    # Takes a JSON array of English-language words and adds them to the corpus (data store).
    if request.method == 'POST':
        if request.data:
            try:
                for word in request.data.get('words'):
                    word = word.lower().strip()
                    anagram = ''.join(sorted(word))

                    # created or updated Anagram record
                    obj, created = Anagram.objects.get_or_create(
                        anagram_key=anagram,
                        defaults={"word_list": word,
                                  "anagrams_count": 1}
                    )
                    if not created:
                        obj.anagram_update(word)

                    f_key = Anagram.objects.filter(anagram_key=anagram).get()

                    # if word does not exist, a new Wordbook record is created
                    Wordbook.objects.get_or_create(
                        word=word,
                        defaults={"word_length": len(word),
                                  "anagram_key": f_key}
                    )

                return Response(status=status.HTTP_201_CREATED)
            except Exception:
                print(f"Unexpected error during creation process")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Deletes all contents of the data store.
    if request.method == 'DELETE':
        Wordbook.objects.all().delete()
        Anagram.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def deleteWord(request, word):
    word_obj = get_object_or_404(Wordbook, word=word)
    if request.method == 'GET':
        serializer = WordbookSerializer(word_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Deletes a single word from the data store.
    elif request.method == 'DELETE':
        anagram = ''.join(sorted(word))
        try:
            anagram_obj = Anagram.objects.get(anagram_key=anagram)
        except Exception:
            # nothing to do
            return Response(status=status.HTTP_200_OK)

        word_obj.delete()
        anagram_obj.delete_anagram_word(word)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
# Endpoint that returns a count of words in the corpus and min/max/median/average word length
def getStatistics(request):
    min_value = Wordbook.objects.all().aggregate(Min('word_length'))
    max_value = Wordbook.objects.all().aggregate(Max('word_length'))
    avg_value = Wordbook.objects.all().aggregate(Avg('word_length'))
    count = Wordbook.objects.all().count()
    length_list = Wordbook.objects.values('word_length').order_by('word_length')
    if count % 2 == 0:
        tmp_1 = length_list[count // 2 - 1]
        tmp_2 = length_list[count // 2]
        median = (tmp_1.get('word_length') + tmp_2.get('word_length')) / 2
    else:
        tmp_1 = length_list[count // 2]
        median = tmp_1.get('word_length')

    content = {
        "count": count,
        "min": min_value['word_length__min'],
        "max": max_value['word_length__max'],
        "median": median,
        "average": avg_value['word_length__avg']
    }
    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
# Endpoint that takes a set of words and returns whether or not they are all anagrams of each other
def wordsCompare(request):

    if request.method == 'GET':
        content = {"msg": "Ready"}
        return Response(content, status=status.HTTP_200_OK)

    if request.method == 'POST':
        answer = 'The words in the list are anagram of each other'

        if request.data:
            # get first word from the list
            try:
                first_word_anagram = ''.join(sorted(request.data.get('words')[0]))
                for word in request.data.get('words'):
                    # compare all words with each other
                    if first_word_anagram != ''.join(sorted(word)):
                        answer = 'The words in the list are not anagram of each other'
                        break
            except Exception:
                answer = 'Bad request'
        else:
            answer = 'Input list is empty'

        content = {"answer": answer}
        return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
# Endpoint that identifies words with the most anagrams
def getMostAnagrams(request):
    max_obj = Anagram.objects.all().order_by('-anagrams_count')[0]
    anagram_obj = Anagram.objects.filter(anagrams_count=max_obj.anagrams_count)
    serializer = AnagramSerializer(anagram_obj, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    #content = {"anagrams": anagram_obj.word_list}
    #return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
# Endpoint to return all anagram groups of size >= x
def getAnagramsGroup(request, size):
    # set a default value of returned responses
    limit = 20
    anagram_obj = Anagram.objects.filter(anagrams_count__gte=size).order_by('-anagrams_count').values()[:limit]
    serializer = AnagramSerializer(anagram_obj, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
# Endpoint to delete a word and all of its anagrams
def deleteAnagrams(request, word):
    anagram = ''.join(sorted(word))
    anagram_obj = get_object_or_404(Anagram, anagram_key=anagram)
    word_obj = Wordbook.objects.filter(anagram_key=anagram)
    if request.method == 'GET':
        serializer = AnagramSerializer(anagram_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if word_obj:
            word_obj.delete()

        if anagram_obj:
            anagram_obj.delete()

        return Response(status=status.HTTP_200_OK)
