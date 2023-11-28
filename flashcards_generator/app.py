import streamlit as st

from constants import languages, language_to_flag
from flashcard import Flashcard, Flashcards

if "flashcards" not in st.session_state:
    st.session_state.flashcards = Flashcards.import_from_json(
        "example_data/flashcards.json"
    )

if "expand_all" not in st.session_state:
    st.session_state.expand_all = False


def create_flashcard(
    expression: str, input_language: str, output_language: str
) -> Flashcard:
    return Flashcard(
        input_expression=expression,
        input_language=input_language,
        output_expression=None,
        output_language=output_language,
        example_usage=None,
    )


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
        flashcard.input_expression == expression
        for flashcard in st.session_state.flashcards.data
    ):
        new_flashcard = create_flashcard(
            expression,
            st.session_state.input_language,
            st.session_state.output_language,
        )
        st.session_state.flashcards.data.append(new_flashcard)


def show_expand_button():
    if st.button("Expand/Collapse All"):
        st.session_state.expand_all = not st.session_state.expand_all


def show_flashcards():
    col1, col2 = st.columns(2)
    for idx, flashcard in enumerate(st.session_state.flashcards.data):
        create_toggle(
            col1 if idx % 2 == 0 else col2,
            f"{language_to_flag[flashcard.input_language]} {flashcard.input_expression}",
            f"{language_to_flag[flashcard.output_language]} {flashcard.output_expression}",
            f"{flashcard.example_usage}",
            f"toggle_{idx}",
        )


def show_generator_page():
    st.title("Flashcards generator")
    show_generator()

    st.divider()
    show_expand_button()
    show_flashcards()


def show_import_export_page():
    st.title("Import/Export")
    st.header("Import file with flashcards")
    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

    st.divider()

    st.header("Export generated flashcards")
    if st.button("Download File"):
        st.write("File download button clicked!")


def main():
    generator_choice = "🤖 Generator"
    import_export_choice = "📂 Import/Export"

    choice = st.sidebar.radio("Select Page", (generator_choice, import_export_choice))
    # Display the selected page based on the choice
    if choice == generator_choice:
        show_generator_page()
    elif choice == import_export_choice:
        show_import_export_page()


if __name__ == "__main__":
    main()
