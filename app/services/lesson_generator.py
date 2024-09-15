from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

class LessonGenerator:
    def __init__(self, openai_api_key=None):
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set. Please provide it or set the OPENAI_API_KEY environment variable.")
        self.llm = OpenAI(temperature=0.7, api_key=api_key)


    def generate_lesson(self, language, proficiency_level, lesson_type):
        prompt = PromptTemplate(
            input_variables=["language", "proficiency", "lesson_type"],
            template="Generate a {lesson_type} lesson for {language} at {proficiency} level. Include vocabulary, grammar, and a short quiz."
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        lesson = chain.run(language=language, proficiency=proficiency_level, lesson_type=lesson_type)
        return lesson

    def generate_quiz(self, language, proficiency_level, topic):
        prompt = PromptTemplate(
            input_variables=["language", "proficiency", "topic"],
            template="Create a quiz for {language} at {proficiency} level on the topic of {topic}. Include 5 multiple-choice questions."
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        quiz = chain.run(language=language, proficiency=proficiency_level, topic=topic)
        return quiz