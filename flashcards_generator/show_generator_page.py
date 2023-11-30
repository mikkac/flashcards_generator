""" Flashcards generator page definition """
import os

import streamlit as st

from flashcards_generator.constants import language_to_flag, languages
from flashcards_generator.flashcard import Flashcard, FlashcardGeneratorOpenAI


def create_flashcard(
    expression: str, input_language: str, output_language: str
) -> Flashcard:
    """
    Creates a Flashcard instance with given expression and languages.

    Args:
        expression (str): The expression to be included in the flashcard.
        input_language (str): The language of the input expression.
        output_language (str): The target language for translation.

    Returns:
        Flashcard: A new Flashcard instance.
    """
    return Flashcard(
        input_expression=expression,
        input_language=input_language,
        output_expression=None,
        output_language=output_language,
        example_usage=None,
    )


def create_toggle(col, original: str, translation: str, example: str):
    """
    Creates a toggle (expandable section) in the Streamlit app.

    Args:
        col: The Streamlit column where the toggle will be placed.
        original (str): The original expression to be displayed.
        translation (str): The translated expression.
        example (str): An example usage of the expression.
        id (str): A unique identifier for the toggle.
    """
    with col:
        with st.expander(original, expanded=st.session_state.expand_all):
            st.write(f"**{translation}**\n\n{example}")


def show_generator(generator: FlashcardGeneratorOpenAI):
    """
    Displays the flashcard generator interface in the Streamlit app.

    Args:
        generator (FlashcardGeneratorOpenAI): The flashcard generator object.
    """
    col1, col2 = st.columns(2)
    with col1:
        input_language = st.selectbox(
            "Select an input language:", languages, index=languages.index("English")
        )
    with col2:
        output_language = st.selectbox(
            "Select an output language:", languages, index=languages.index("Polish")
        )

    if "input_language" not in st.session_state:
        st.session_state.input_language = input_language
    st.session_state.input_language = input_language

    if "output_language" not in st.session_state:
        st.session_state.output_language = output_language
    st.session_state.output_language = output_language

    expression = st.text_input(
        "Expression",
        placeholder="Enter an expression and press Enter to generate a flashcard",
    )

    if expression and not any(
        flashcard.input_expression == expression
        for flashcard in st.session_state.flashcards.data
    ):
        new_flashcard = generator.generate_flashcard(
            expression, input_language, output_language
        )
        st.session_state.flashcards.data.append(new_flashcard)


def show_expand_button():
    """
    Displays a button to expand or collapse all flashcards in the Streamlit app.
    """
    if st.button("Expand/Collapse All"):
        st.session_state.expand_all = not st.session_state.expand_all


def show_flashcards():
    """
    Displays the generated flashcards in the Streamlit app.
    """
    if len(st.session_state.flashcards) == 0:
        st.info("Generate a flashcard or import a file with previously generated ones")
    else:
        col1, col2 = st.columns(2)
        for idx, flashcard in enumerate(st.session_state.flashcards.data):
            create_toggle(
                col1 if idx % 2 == 0 else col2,
                f"{language_to_flag[flashcard.input_language]} {flashcard.input_expression}",
                f"{language_to_flag[flashcard.output_language]} {flashcard.output_expression}",
                f"{flashcard.example_usage}",
            )


def show_generator_page():
    """
    Sets up the main page of the Streamlit app for the flashcard generator.
    """
    generator = FlashcardGeneratorOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    st.title("Flashcards generator")
    show_generator(generator)

    st.divider()
    show_expand_button()
    show_flashcards()
