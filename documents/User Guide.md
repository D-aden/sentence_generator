# User Guide

## Installation

Before running the application, ensure that Python and Poetry are installed.

### Clone the Repository

```
git clone https://github.com/D-aden/sentence_generator
cd sentence_generator
```

### Install Dependencies

Install the project dependencies using Poetry:

```
poetry install
```

Activate the virtual environment:

```
poetry shell
```

This creates and activates an isolated environment containing all required packages.

---

# Running Tests


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

---

# Running the Application

Launch the application with:

```
python3 gui.py
```

## Application Settings

### N-gram Order

Controls how many previous words are used to predict the next word. Higher values generally produce more coherent and natural-looking text.

### Sentence Length

Sets the number of words in each generated sentence.

### Number of Sentences

Sets the total number of sentences to generate.

## Generating Text

1. Click **Generate Text**.
2. Select one or more CSV files from the file dialogue.
3. The application reads the article content, builds the model, and displays the generated text in the output area.
CSV files must contain a column named `article`, `content`, `text`, or `body`. Each row in that column is treated as one article. Any other columns are ignored.

---

# Troubleshooting

### No Text Is Generated

- Ensure that at least one file has been selected.
- Verify that the selected file contains data.

### Generated Text Appears Nonsensical

- Try increasing the N-gram order (e.g., 3–5).
- Use a larger dataset to improve text quality.

### Application Crashes or Produces Errors

- Check that all input values are valid integers.
- Ensure that the required dependencies have been installed successfully.
