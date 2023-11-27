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