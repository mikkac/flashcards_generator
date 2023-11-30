from dotenv import load_dotenv, find_dotenv
import streamlit as st

from flashcard import Flashcards

# Importing page modules
from import_export_page import show_import_export_page
from show_generator_page import show_generator_page


def main():
    """
    Main function to run the Streamlit app for flashcard generation and management.

    This function initializes the app, setting up the page configuration and session state.
    It provides navigation between the flashcard generator and import/export pages.
    """

    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    # Set Streamlit page configuration
    st.set_page_config(page_title="FG", layout="centered", initial_sidebar_state="auto")

    # Initialize flashcards in session state if not already present
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = Flashcards([])

    # Initialize expand_all toggle state in session state
    if "expand_all" not in st.session_state:
        st.session_state.expand_all = False

    # Define navigation options
    generator_choice = "🤖 Generator"
    import_export_choice = "📂 Import/Export"

    # Sidebar for navigation
    with st.sidebar:
        # Display application logo
        st.image(
            "https://github.com/mikkac/flashcards_generator/blob/main/resources/logo.png?raw=true"
        )
        # Radio buttons for page selection
        choice = st.radio("Select Page", (generator_choice, import_export_choice))

    # Conditional rendering of pages based on user choice
    if choice == generator_choice:
        show_generator_page()
    elif choice == import_export_choice:
        show_import_export_page()


if __name__ == "__main__":
    main()
