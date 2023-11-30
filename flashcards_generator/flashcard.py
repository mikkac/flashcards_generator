import json
from dataclasses import asdict, dataclass

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser


@dataclass
class Flashcard:
    """
    Represents a flashcard containing language translation information.

    Attributes:
        input_expression (str): The expression in the input language.
        input_language (str): The language of the input expression.
        output_expression (str): The translated expression in the output language.
        output_language (str): The language of the output expression.
        example_usage (str): An example usage of the input expression in a sentence.
    """

    input_expression: str
    input_language: str
    output_expression: str
    output_language: str
    example_usage: str

    @classmethod
    def from_dict(cls, data: dict) -> "Flashcard":
        """
        Creates a Flashcard instance from a dictionary of attributes.

        Args:
            data (dict): A dictionary containing flashcard attributes.

        Returns:
            Flashcard: An instance of Flashcard.
        """
        return cls(
            input_expression=data.get("input_expression", None),
            input_language=data.get("input_language", None),
            output_expression=data.get("output_expression", None),
            output_language=data.get("output_language", None),
            example_usage=data.get("example_usage", None),
        )


@dataclass
class Flashcards:
    """
    Represents a collection of Flashcard instances.

    Attributes:
        data (list[Flashcard]): A list of Flashcard instances.
    """

    data: list[Flashcard]

    def as_json(self) -> dict:
        """
        Converts the collection of Flashcard instances to a JSON format.

        Returns:
            dict: A dictionary representing the flashcards in JSON format.
        """
        return {"flashcards": [asdict(card) for card in self.data]}

    @classmethod
    def import_from_json(cls, data: dict) -> "Flashcards":
        """
        Creates a Flashcards instance from a JSON file.

        Args:
            data (file): A JSON file containing flashcard data.

        Returns:
            Flashcards: An instance of Flashcards containing the imported data.
        """
        data = json.load(data)
        flashcard_objects = [Flashcard(**card) for card in data["flashcards"]]
        return cls(data=flashcard_objects)

    def __len__(self) -> int:
        """
        Returns the number of Flashcard instances in the collection.

        Returns:
            int: The number of Flashcard instances.
        """
        return len(self.data)


class FlashcardGeneratorOpenAI:
    """
    A class to generate language learning flashcards using OpenAI's language model.

    Attributes:
        chat (ChatOpenAI): An instance of ChatOpenAI for generating flashcards.
        response_schemas (list): A list of ResponseSchema objects for structuring the response.
        output_parser (StructuredOutputParser): Parser to structure the output from the language model.
        flashcard_generator_template (str): A template for generating flashcard data.
        prompt (ChatPromptTemplate): A prompt template for the language model.
    """

    def __init__(self, api_key: str, llm_model: str = "gpt-3.5-turbo") -> None:
        """
        Initializes the FlashcardGeneratorOpenAI class with the specified API key and language model.

        Args:
            api_key (str): The API key for OpenAI.
            llm_model (str): The name of the language model to use.
        """
        self.chat = ChatOpenAI(temperature=0.0, model=llm_model, api_key=api_key)

        self.input_expression_schema = ResponseSchema(
            name="input_expression",
            type="str",
            description="Original expression entered by the user, refined to create translated_expression.",
        )
        self.input_language_schema = ResponseSchema(
            name="input_language",
            type="str",
            description="Language of the input expression.",
        )
        self.output_expression_schema = ResponseSchema(
            name="output_expression",
            type="str",
            description="Translation of refined expression entered by the user.",
        )
        self.output_language_schema = ResponseSchema(
            name="output_language",
            type="str",
            description="Language of the output expression.",
        )
        self.example_usage_schema = ResponseSchema(
            name="example_usage",
            type="str",
            description="Example usage of input expression, used to give the user some example context where it could be used. Limited to one sentence.",
        )

        self.response_schemas = [
            self.input_expression_schema,
            self.input_language_schema,
            self.output_expression_schema,
            self.output_language_schema,
            self.example_usage_schema,
        ]

        self.output_parser = StructuredOutputParser.from_response_schemas(
            self.response_schemas
        )
        self.format_instructions = self.output_parser.get_format_instructions()

        self.flashcard_generator_template = """\
        For the following expression, extract the following information:

        input_expression: Original expression entered by the user, but refined to create translated_expression (for flashcard for language learning). If the expression is too long (more than 10 words), it should be shortened while keeping the sense.

        input_language: Language of the input expression

        output_expression: Refined input expression translated to {output_language} language. Provide 2 alternatives, separated with 'slash' sign (and space before & after the sign).

        example_usage: Example usage of input expression, used to give the user some example context where it could be used. Limited to one sentence.

        input_expression: {input_expression}
        input_language: {input_language}

        {format_instructions}
        """

        self.prompt = ChatPromptTemplate.from_template(
            template=self.flashcard_generator_template
        )

    def generate_flashcard(
        self, input_expression: str, input_language: str, output_language: str
    ) -> Flashcard:
        messages = self.prompt.format_messages(
            input_expression=input_expression,
            input_language=input_language,
            output_language=output_language,
            format_instructions=self.format_instructions,
        )
        response = self.chat(messages)
        flashcard_dict = self.output_parser.parse(response.content)
        return Flashcard.from_dict(flashcard_dict)


if __name__ == "__main__": # For debugging purposes only
    from dotenv import load_dotenv, find_dotenv
    import os

    _ = load_dotenv(find_dotenv())  # Read local .env file

    generator = FlashcardGeneratorOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    input_expressions = [
        "cruel",
        "let someone off the hook",
        "it absorbed me",
        "get my thoughts in order",
        "crude",
        "pore over",
    ]
    input_language = "English"
    output_language = "Polish"

    flashcards = Flashcards()

    for input_expression in input_expressions:
        flashcard = generator.generate_flashcard(
            input_expression, input_language, output_language
        )
        print(flashcard)
        flashcards.flashcards.append(asdict(flashcard))

    flashcards.export_to_json("flashcards.json")
