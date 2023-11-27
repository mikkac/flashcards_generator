import streamlit as st

from constants import flashcards_data, languages, language_to_flag

if "flashcards" not in st.session_state:
    st.session_state.flashcards = flashcards_data

if "expand_all" not in st.session_state:
    st.session_state.expand_all = False


def create_flashcard(
    expression: str, input_language: str, output_language: str
) -> dict:
    return {
        "input_expression": expression,
        "input_language": input_language,
        "output_language": output_language,
    }


def create_toggle(col, input: str, output: str, example: str, id: str):
    with col:
        with st.expander(input, expanded=st.session_state.expand_all):
            st.write(f"**{output}**\n\n{example}")


def show_generator():
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
        flashcard["input_expression"] == expression
        for flashcard in st.session_state.flashcards
    ):
        new_flashcard = create_flashcard(
            expression, st.session_state.input_language, st.session_state.output_language
        )
        st.session_state.flashcards.append(new_flashcard)


# Display generated flashcards



def show_flashcards():
    col1, col2 = st.columns(2)
    for idx, flashcard in enumerate(st.session_state.flashcards):
        create_toggle(
            col1 if idx % 2 == 0 else col2,
            f"{language_to_flag[flashcard['input_language']]} {flashcard.get('input_expression', None)}",
            f"{language_to_flag[flashcard['output_language']]} {flashcard.get('output_expression', None)}",
            f"{flashcard.get('example_usage', None)}",
            f"toggle_{idx}",
        )


def main():
    st.title("Flashcards generator")
    show_generator()

    st.divider()

    st.subheader("Available flashcards")
    if st.button("Expand/Collapse All"):
        st.session_state.expand_all = not st.session_state.expand_all
    show_flashcards()

if __name__ == "__main__":
    main()