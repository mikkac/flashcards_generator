import streamlit as st

flashcards_data = [
    {
        "input_expression": "cruel",
        "input_language": "English",
        "output_expression": "okrutny / brutalny",
        "output_language": "Polish",
        "example_usage": "The dictator's cruel treatment of his people sparked international outrage.",
    },
    {
        "input_expression": "let someone off the hook",
        "input_language": "English",
        "output_expression": "uwolni\u0107 kogo\u015b od odpowiedzialno\u015bci / odpu\u015bci\u0107 komu\u015b",
        "output_language": "Polish",
        "example_usage": "I decided to let my friend off the hook and not hold him responsible for the mistake.",
    },
    {
        "input_expression": "it absorbed me",
        "input_language": "English",
        "output_expression": "to mnie wch\u0142on\u0119\u0142o / to mnie poch\u0142on\u0119\u0142o",
        "output_language": "Polish",
        "example_usage": "The book was so captivating that it absorbed me completely.",
    },
    {
        "input_expression": "get my thoughts in order",
        "input_language": "English",
        "output_expression": "uporz\u0105dkowa\u0107 moje my\u015bli/skolekcjonowa\u0107 moje my\u015bli",
        "output_language": "Polish",
        "example_usage": "I need some time alone to get my thoughts in order before making a decision.",
    },
    {
        "input_expression": "crude",
        "input_language": "English",
        "output_expression": "prostacki / prymitywny",
        "output_language": "Polish",
        "example_usage": "His jokes were crude and offensive.",
    },
    {
        "input_expression": "pore over",
        "input_language": "English",
        "output_expression": "prze\u015bwietli\u0107/szpera\u0107",
        "output_language": "Polish",
        "example_usage": "She spent hours poring over the documents to find the missing information.",
    },
]

languages = [
    "English",
    "Spanish",
    "Polish",
    "Chinese",
    "Hindi",
    "Arabic",
    "Portuguese",
    "Bengali",
    "Russian",
    "Japanese",
]

language_to_flag = {
    "English": "🇬🇧",  # Flag of the United Kingdom
    "Spanish": "🇪🇸",  # Flag of Spain
    "Polish": "🇵🇱",  # Flag of Poland
    "Chinese": "🇨🇳",  # Flag of China
    "Hindi": "🇮🇳",  # Flag of India
    "Arabic": "🇸🇦",  # Flag of Saudi Arabia (Arabic is widely spoken in many countries)
    "Portuguese": "🇵🇹",  # Flag of Portugal
    "Japanese": "🇯,🇵"  # Flag of Japan
}


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