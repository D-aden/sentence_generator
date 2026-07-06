
# Markov Chain Text Generator
 
An application that reads articles from CSV files, builds an n-gram Markov model, and generates new text by sampling from that model.
 

## Documents 
[Specification Document](./documents/Specification%20Document.md)

[Implementation Document](./documents/Implementation%20Document.md)

[Testing Document](./documents/Testing%20Documentation.md)

[User Guide](./documents/User%20Guide.md)

## Weekly Reports
[Week 1 Report](./weekly%20reports/WeeklyReport1.pdf)

[Week 2 Report](./weekly%20reports/WeeklyReport2.pdf)

[Week 3 Report](./weekly%20reports/WeeklyReport3.pdf)

[Week 4 Report](./weekly%20reports/WeeklyReport4.pdf)

[Week 5 Report](./weekly%20reports/WeeklyReport5.pdf)

[Week 6 Report](./weekly%20reports/WeeklyReport6.pdf)

## Installation
 
Before running the application, ensure that Python and Poetry are installed on your system.
 
### Clone the Repository
 
```
git clone https://github.com/D-aden/sentence_generator

cd sentence_generator
```
 
### Install Dependencies
 
```
poetry install

poetry shell
```
 

 
## Running the Application
 
```
python3 gui.py
```
 
### Generating Text
 
1. Click **Generate Text**.
2. Select one or more CSV files from the file dialog.
3. The application reads the article content, builds the model, and displays the generated text in the output area. CSV files must contain a column named `article`, `content`, `text`, or `body`. Each row in that column is treated as one article. Any other columns are ignored. Keep in mind that if a word has no successor, the model will attempt to start to generate a new sentence, however the number of attempts for regeneration has a **limit of 100**. 
 
### Parameters
 
| Parameter | Description | Default |
||||
| N-gram Order | The number of previous words used to predict the next word. Higher values produce more coherent text but require a larger dataset. | 2 |
| Sentence Length | Sets the number of words in each generated sentence.| 15 |
| Number of Sentences | Sets the total number of sentences to generate. | 5 |
 

 
## Running Tests
 

### Unit tests
```
poetry run coverage run -m unittest test_main.py
```
 
### Integration tests
```
poetry run coverage run -a -m unittest integration_tests.py
```

### Generate a test coverage report with:
```
poetry run coverage report
```