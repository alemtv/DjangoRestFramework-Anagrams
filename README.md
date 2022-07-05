# Django REST framework - Anagrams API
The project is to build an API that allows fast searches for [anagrams](https://en.wikipedia.org/wiki/Anagram). 

## Main algorithm
Using the sorted function in python, all words are converted to anagram_key value. Example: word “dog” convert to “dgo”. The relationship between anagram_key and words is stored in DB tables. Search is performed according to the anagram_key field.

According to this model, the list of anagrams must be returned very quickly. Because the database searches for a single record by primary_key (Anagram.anagram_key).

Also this model makes it easy to collect statistical information such as: words with the most anagrams or groups of anagrams by size.

![DB view](https://saniokas.pythonanywhere.com/static/blog/images/db_view.jpg)

**WordBook** - table to store all words (provided in dictionary.txt).
**Anagram** - table to store the relationships between anagram_key and the world list. Anagram table is updated each time a new word is created or an existing word is deleted.

## Installation
1. **Create and activate the virtual environment.** 
2. **Clone the project.** Open the command line, go to the folder where you want to save the project and enter the following command:
```
git clone https://github.com/saniokas/DjangoRestFramework-Anagrams.git
```
3. **Install project dependencies.** If you are using a virtual environment, be sure to activate and enter the virtual environment, enter the source folder in which the project is located at the command line (cd DjangoRestFramework-Anagrams), and run the following command:
```bash
pip install -r requirements.txt
```
4. **Migrate the database.** Run the following command to migrate the database:
```bash
python manage.py migrate
```
5. **Create administrator account**
```
python manage.py createsuperuser
```
6. **Install demo data.** The data loading script (anagram/scripts/load_data.py) is used for loading the data from txt file. It will take about one hour.
```
python manage.py runscript load_data
```
7. **Run the development server**
```
python manage.py runserver
```

## API endpoints
- `POST /words`: Takes a JSON array of English-language words and adds them to the corpus (data store).
- `GET /anagrams/{word}`:
  - Returns a JSON array of English-language words that are anagrams of the word passed in the URL.
  - This endpoint support an optional query param that indicates the maximum number of results to return (`/anagrams/{word}/?limit=2`).
- `DELETE /words/{word}`: Deletes a single word from the data store.
- `DELETE /words`: Deletes all contents of the data store.
- `GET /statistics`: Endpoint that returns a count of words in the corpus and min/max/median/average word length.
- `GET /most-anagrams`: Endpoint that identifies words with the most anagrams.
- `POST /compare`: Endpoint that takes a set of words and returns whether or not they are all anagrams of each other .
- `GET /anagrams-group/x`: Endpoint to return all anagram groups of size >= *x*. Output (maximum of 20 values are returned).
- `DELETE /delete/{word}`: Endpoint to delete a word *and all of its anagrams* 
