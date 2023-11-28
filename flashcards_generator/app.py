import streamlit as st

from flashcard import Flashcards

# pages
from import_export_page import show_import_export_page
from show_generator_page import show_generator_page


def main():
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = Flashcards([])

    if "expand_all" not in st.session_state:
        st.session_state.expand_all = False

    generator_choice = "🤖 Generator"
    import_export_choice = "📂 Import/Export"

    with st.sidebar:
        st.image(
            "https://github.com/mikkac/flashcards_generator/blob/main/resources/logo.png?raw=true"
        )
        choice = st.radio("Select Page", (generator_choice, import_export_choice))
    if choice == generator_choice:
        show_generator_page()
    elif choice == import_export_choice:
        show_import_export_page()


if __name__ == "__main__":
    main()
