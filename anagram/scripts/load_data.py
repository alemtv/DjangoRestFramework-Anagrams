from anagram.models import Wordbook, Anagram
import datetime
from itertools import islice


def run():
    input_file = 'anagram/data/dictionary.txt'
    print(f'Starting processing the input file: {input_file}')
    with open(input_file) as file:
        lines = file.readlines()

        total_rec = len(lines)
        print(f'Total records in the input file: {total_rec}')

        Wordbook.objects.all().delete()
        Anagram.objects.all().delete()

        count = 0
        anagram_add_rec = 0
        word_add_rec = 0
        anagram_list = [{}]
        word_list = []
        batch_size = 100

        print(f'Create a list of unique words. Time: {datetime.datetime.now()}')
        print_total = 0
        for word in lines:
            # create a list of unique words
            count += 1
            print_total += 1
            word = word.lower().strip()
            if word not in word_list: word_list.append(word)
            if print_total % 10000 == 0: print(
                f'Processed {print_total} records out of {total_rec}. Time: {datetime.datetime.now()}')

        print(f'Creating a list of anagrams. Time: {datetime.datetime.now()}')
        total_word = len(word_list)
        print_total = 0
        for word in word_list:
            # create a list of anagrams
            anagram = ''.join(sorted(word))
            new_count = 0
            print_total += 1

            for x in anagram_list:
                # updating an existing entry
                if x.get('anagram') == anagram:
                    new_list = x.get('word_list') + ',' + word
                    new_count = int(x.get('anagrams_count')) + 1
                    x.update({"word_list": new_list, "anagrams_count": new_count})
                    break

            if new_count == 0:
                # a new entry is created
                anagram_list.append({ "anagram": anagram, "word_list": word, "anagrams_count": 1 })

            if print_total % 10000 == 0: print(
                f'Processed {print_total} records out of {total_word}. Time: {datetime.datetime.now()}')

        print(f'Start Anagram bulk load. Time: {datetime.datetime.now()}')
        batch_records = []
        batch_count = 0
        print_total = 0
        for x in anagram_list:
            batch_count += 1
            print_total += 1
            if x.get('anagram'):
                batch_records.append(Anagram(
                        anagram_key=x.get('anagram'),
                        word_list=x.get('word_list'),
                        anagrams_count=x.get('anagrams_count')
                    )
                )

            if batch_count == batch_size:
                Anagram.objects.bulk_create(batch_records)
                batch_count = 0
                batch_records = []
                anagram_add_rec += batch_size

            if print_total % 10000 == 0: print(
                f'Processed {print_total} records out of {total_word}. Time: {datetime.datetime.now()}')

        anagrams_left = len(batch_records)
        if batch_records:
            Anagram.objects.bulk_create(batch_records)
            anagram_add_rec += anagrams_left

        print(f'Start Wordbook bulk load. Time: {datetime.datetime.now()}')
        batch_records = []
        batch_count = 0
        print_total = 0
        for word in word_list:
            batch_count += 1
            print_total += 1
            anagram = ''.join(sorted(word))
            f_key = Anagram.objects.filter(anagram_key=anagram).get()

            batch_records.append(Wordbook(
                word=word,
                word_length=len(word),
                anagram_key=f_key)
            )

            if batch_count == batch_size:
                Wordbook.objects.bulk_create(batch_records)
                batch_count = 0
                batch_records = []
                word_add_rec += batch_size

            if print_total % 10000 == 0: print(
                f'Processed {print_total} records out of {total_word}. Time: {datetime.datetime.now()}')

        words_left = len(batch_records)
        if batch_records:
            Wordbook.objects.bulk_create(batch_records)
            word_add_rec += words_left

    print(f'Input file processing completed')
    print(f'Total records in file       : {count}')
    print(f'Total Wordbook records saved: {word_add_rec}')
    print(f'Total Anagram records saved : {anagram_add_rec}')
