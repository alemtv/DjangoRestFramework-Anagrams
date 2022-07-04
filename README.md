# Django REST framework - Anagrams API
The project is to build an API that allows fast searches for [anagrams](https://en.wikipedia.org/wiki/Anagram). 

## Main algorithm
Using the sorted function in python, all words are converted to anagram_key value. Example: word “dog” convert to “dgo”. The relationship between anagram_key and words is stored in DB tables. Search is performed according to the anagram_key field.

According to this model, the list of anagrams must be returned very quickly. Because the database searches for a single record by primary_key (Anagram.anagram_key).

Also this model makes it easy to collect statistical information such as: words with the most anagrams or groups of anagrams by size.

![DB view](https://saniokas.pythonanywhere.com/static/blog/images/db_view.jpg)

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
6. **Run the development server**
```
python manage.py runserver
```
