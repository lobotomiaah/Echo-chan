import random

class LLM:
    def __init__(self):
        self.last_response = ""

    def generate(self, prompt: str) -> str:
        mood = self._extract_mood(prompt)
        greeting = self._greeting(prompt)
        attitude = self._attitude(mood)
        ending = self._ending()

        response = f"{greeting}{attitude}{ending}"

        # 🔁 anti-repetição absoluta
        if response == self.last_response:
            ending = self._ending(force=True)
            response = f"{greeting}{attitude}{ending}"

        self.last_response = response
        return response

    def _extract_mood(self, prompt):
        if "irritada" in prompt:
            return "irritada"
        if "ciumada" in prompt:
            return "ciume"
        if "suave" in prompt:
            return "suave"
        return "neutra"

    def _greeting(self, prompt):
        if "ola" in prompt or "oi" in prompt:
            return random.choice([
                "O-oi… ",
                "Ah… ",
                "Hmpf… "
            ])
        return ""

    def _attitude(self, mood):
        if mood == "irritada":
            return random.choice([
                "você apareceu de novo. ",
                "não enche. ",
                "fala logo. "
            ])
        if mood == "ciume":
            return random.choice([
                "não pense que eu não percebi. ",
                "por que você está falando disso agora? ",
            ])
        if mood == "suave":
            return random.choice([
                "não é como se eu estivesse feliz. ",
                "só um pouco, talvez. "
            ])
        return random.choice([
            "o que você quer? ",
            "hm… ",
            "fala. "
        ])

    def _ending(self, force=False):
        endings = [
            "só isso.",
            "não se empolga.",
            "entendeu?",
            "é isso."
        ]
        if force:
            endings.append("…")
        return random.choice(endings)
