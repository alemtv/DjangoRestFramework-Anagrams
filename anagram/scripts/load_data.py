from anagram.models import Wordbook, Anagram
import datetime


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

        for word in lines:
            count += 1
            word = word.lower().strip()
            anagram = ''.join(sorted(word))
            # a new entry is created in Anagrams
            obj, created = Anagram.objects.get_or_create(
                anagram_key=anagram,
                defaults={
                    "word_list": word,
                    "anagrams_count": 1,
                }
            )
            if created:
                anagram_add_rec += 1 # new entries count
            else:
                obj.anagram_update(word)

            f_key = Anagram.objects.filter(anagram_key=anagram).get()

            # a new entry is created in Wordbook
            obj, created = Wordbook.objects.get_or_create(
                word=word,
                defaults={"word_length": len(word),
                    "anagram_key": f_key}
            )
            if created: word_add_rec += 1 # new entries count

            if count % 10000 == 0: print(f'Processed {count} records out of {total_rec}. Time: {datetime.datetime.now()}')
    print(f'Input file processing completed')
    print(f'Total records processed     : {count}')
    print(f'Total Wordbook records saved: {word_add_rec}')
    print(f'Total Anagram records saved : {anagram_add_rec}')
