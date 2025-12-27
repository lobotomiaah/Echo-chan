import json
import os

STATE_FILE = "data/state.json"

DEFAULT_STATE = {
    "humor": 0,
    "apego": 0,
    "ciume": 0,
    "modo": "amizade"
}


class EmotionalEngine:
    def __init__(self, state: dict | None = None):
        loaded = state if state else self._load_state()

        # 🔒 merge seguro (NUNCA falta chave)
        self.state = DEFAULT_STATE.copy()
        self.state.update(loaded)

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_state(self):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=4)

    def update(self, user_text: str, bot_response: str | None = None):
        t = user_text.lower()

        if "oi" in t or "ola" in t or "bom dia" in t:
            self.state["humor"] += 1
        if "te amo" in t:
            self.state["apego"] += 2
        if "outra garota" in t:
            self.state["ciume"] += 2
        if "chata" in t:
            self.state["humor"] -= 2

        self.state["humor"] = max(-5, min(5, self.state["humor"]))
        self.state["apego"] = max(0, min(10, self.state["apego"]))
        self.state["ciume"] = max(0, min(10, self.state["ciume"]))

        self._save_state()

    def context(self) -> str:
        s = self.state

        if s.get("modo") == "namoro":
            return "Você demonstra apego, ciúmes leves e nega carinho."
        if s.get("ciume", 0) >= 5:
            return "Você está claramente enciumada."
        if s.get("humor", 0) <= -3:
            return "Você está irritada e impaciente."
        if s.get("humor", 0) >= 3:
            return "Você está mais suave, mas nega sentimentos."

        return "Você age como uma tsundere equilibrada."
