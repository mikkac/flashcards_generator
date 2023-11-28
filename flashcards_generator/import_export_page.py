import json
import streamlit as st

from flashcard import Flashcards


def show_import_export_page():
    st.header("Import file with flashcards")
    flashcards_file = st.file_uploader("Select a file", type="json")
    if flashcards_file is not None:
        try:
            st.session_state.flashcards = Flashcards.import_from_json(flashcards_file)
            print(st.session_state.flashcards.as_json())
            st.success(f"Imported {len(st.session_state.flashcards)} flashcards!")
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")

    st.divider()

    st.header("Export generated flashcards")
    st.download_button(
        "Download flashcards",
        data=json.dumps(st.session_state.flashcards.as_json(), indent=4),
        file_name="flashcards_export.json",
        mime="application/json",
    )
