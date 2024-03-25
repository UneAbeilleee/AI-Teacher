import genanki
import requests
import json

class FlashcardCreator:
    def __init__(self, deck_name, deck_id):
        self.deck = genanki.Deck(deck_id, deck_name)
        self.quiz_model = self.create_quiz_model()
        self.qa_model = self.create_qa_model()
        self.cloze_model = self.create_cloze_model()
        self.definition_model = self.create_definition_model()
        self.anki_connect_url = "http://localhost:8765"

    def create_quiz_model(self):
        return genanki.Model(
            1607392319,
            'Quiz Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ]
        )

    def create_qa_model(self):
        return genanki.Model(
            1607392320,
            'QA Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ]
        )

    def create_cloze_model(self):
        return genanki.Model(
            1607392321,
            'Cloze Model',
            fields=[
                {'name': 'Text'},
                {'name': 'Cloze'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{cloze:Text}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Text}}',
                },
            ],
            model_type=genanki.Model.CLOZE
        )

    def create_definition_model(self):
        return genanki.Model(
            1607392322,
            'Definition Model',
            fields=[
                {'name': 'Term'},
                {'name': 'Definition'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Term}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
                },
            ]
        )

    def create_flashcard(self, type, *args):
        if type == "quiz":
            return self.create_quiz_flashcard(*args)
        elif type == "qa":
            return self.create_qa_flashcard(*args)
        elif type == "cloze":
            return self.create_cloze_flashcard(*args)
        elif type == "definition":
            return self.create_definition_flashcard(*args)
        else:
            raise ValueError("Unsupported flashcard type")

    def create_quiz_flashcard(self, question, options, correct_option):
        options_html = "".join([f"<li style='margin: 10px 0; text-align: center;'>{option}</li>" for option in options])
        question_html = f"""
            <div style="text-align: center;">
                <h2>{question}</h2>
            </div>
            <hr>
            <ul style="list-style-type: none;">
                {options_html}
            </ul>
        """
        answer_html = f"<div style='text-align: center;'><h2>{correct_option}</h2></div>"
        return genanki.Note(
            model=self.quiz_model,
            fields=[question_html, answer_html],
            tags=["Quiz"]
        )

    # Define create_qa_flashcard, create_cloze_flashcard, and create_definition_flashcard similarly

    def create_qa_flashcard(self, question, answer):
        # Dummy implementation, adjust as needed
        return self._create_simple_flashcard(question, answer, self.qa_model)

    def create_cloze_flashcard(self, text, cloze):
        # Dummy implementation, adjust as needed
        return self._create_simple_flashcard(cloze, text, self.cloze_model)

    def create_definition_flashcard(self, term, definition):
        # Dummy implementation, adjust as needed
        return self._create_simple_flashcard(term, definition, self.definition_model)

    def _create_simple_flashcard(self, field1, field2, model):
        return genanki.Note(
            model=model,
            fields=[field1, field2],
            tags=["Generated"]
        )

    def add_flashcard(self, flashcard):
        self.deck.add_note(flashcard)

    def export_deck(self, file_name):
        package = genanki.Package(self.deck)
        package.write_to_file(file_name)
        print(f"Deck exported successfully to {file_name}!")

    def invoke_anki_connect(self, action, **params):
        payload = {"action": action, "version": 6, "params": params}
        response = requests.post(self.anki_connect_url, data=json.dumps(payload))
        return response.json()


# Usage example
flashcard_creator = FlashcardCreator(deck_name='CNN Flashcards', deck_id=123456789)

# Flashcard info
question = "In a convolutional neural network (CNN), what is the purpose of the pooling layer?"
options = [
    "A) To reduce overfitting by introducing dropout",
    "B) To increase the number of feature maps",
    "C) To reduce the spatial dimensions of the input volume",
    "D) To increase the non-linearity of the model"
]
correct_option = "Correct! In a convolutional neural network (CNN), the pooling layer is used to reduce the spatial dimensions (width and height) of the input volume, while retaining important information. This helps in reducing the computational complexity of the network and controlling overfitting by reducing the number of parameters. Common pooling operations include max pooling and average pooling, where the maximum or average value in each pooling window is taken, respectively."

# Creating the flashcard
quiz_flashcard = flashcard_creator.create_quiz_flashcard(question, options, correct_option)

# Adding the flashcard to the deck
flashcard_creator.add_flashcard(quiz_flashcard)

# Exporting the deck to a file
flashcard_creator.export_deck('cnn_flashcards.apkg')
