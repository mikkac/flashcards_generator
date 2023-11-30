""" Import/export page definition """
import json

import streamlit as st

from flashcards_generator.flashcard import Flashcards


def show_import_export_page():
    """
    Defines a Streamlit page for importing and exporting flashcards.

    This function creates an interface where users can upload a JSON file
    to import flashcards, and download a JSON file containing the current
    flashcards stored in the session state. It handles file upload, file validation,
    and displays success or error messages accordingly.
    """

    # Displaying a header for the import section
    st.header("Import file with flashcards")

    # File uploader widget allowing the user to upload a JSON file
    flashcards_file = st.file_uploader("Select a file", type="json")

    # Handling the uploaded file
    if flashcards_file is not None:
        try:
            # Attempt to import flashcards from the uploaded file
            st.session_state.flashcards = Flashcards.import_from_json(flashcards_file)
            print(st.session_state.flashcards.as_json())  # Debug print statement
            st.success(f"Imported {len(st.session_state.flashcards)} flashcards!")
        except json.JSONDecodeError:
            # Handling invalid JSON files
            st.error("Invalid JSON file. Please upload a valid JSON file.")

    # Divider to separate import and export sections
    st.divider()

    # Displaying a header for the export section
    st.header("Export generated flashcards")

    # Download button to export the flashcards as a JSON file
    st.download_button(
        "Download flashcards",
        data=json.dumps(st.session_state.flashcards.as_json(), indent=4),
        file_name="flashcards_export.json",
        mime="application/json",
    )
