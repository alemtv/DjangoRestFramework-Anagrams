from django.db import models


class Wordbook(models.Model):
    word = models.CharField(max_length=45, primary_key=True)
    word_length = models.PositiveIntegerField(null=False)
    anagram_key = models.ForeignKey('Anagram', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.word


class Anagram(models.Model):
    anagram_key = models.CharField(max_length=45, primary_key=True)
    word_list = models.TextField()
    anagrams_count = models.PositiveIntegerField(null=False)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.word_list

    def anagram_update(self, new_word):
        try:
            Wordbook.objects.get(word=new_word)
        except:
            self.anagrams_count += 1
            self.word_list = self.word_list + ',' + new_word
            self.save(update_fields=['anagrams_count', 'word_list'])

    def get_anagram_list(self, word, limit):
        add_count = 0
        answer = []
        words = self.word_list.split(",")
        for list_element in words:
            if list_element != word:  # word is not considered to be its own anagram
                add_count += 1
                # collect a list of anagrams
                answer.append(list_element)
                if limit != 0 and add_count >= limit:
                    # list limit reached
                    break
        return answer

    def delete_anagram_word(self, word):
        if self.anagrams_count == 1:
            self.delete()
        else:
            count = 0
            new_words_list = ''
            words = self.word_list.split(",")
            for list_element in words:
                if list_element != word:
                    count += 1
                    if count == 1:
                        new_words_list = list_element
                    else:
                        new_words_list = new_words_list + ',' + list_element

            self.anagrams_count = count
            self.word_list = new_words_list
            self.save(update_fields=['anagrams_count', 'word_list'])
