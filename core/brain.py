from core.memory import Memory
from core.emotions import EmotionalEngine
from core.llm import LLM
from core.filters import AntiGenericFilter

class Brain:
    def __init__(self):
        self.memory = Memory()

        self.emotions = EmotionalEngine(
            self.memory.data.get("emotions", {})
        )

        self.llm = LLM()
        self.filter = AntiGenericFilter()

    def responder(self, user_text: str) -> str:
        mood_context = self.emotions.context()
        memory_context = self.memory.context()

        prompt = f"""
{mood_context}
{memory_context}

Usuário: {user_text}
IA:
"""

        raw_response = self.llm.generate(prompt)
        response = self.filter.clean(raw_response)

        self.emotions.update(user_text, response)
        self.memory.save()

        return response
