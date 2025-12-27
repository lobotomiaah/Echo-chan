class AntiGenericFilter:
    def clean(self, text: str) -> str:
        generic_responses = [
            "Não sei",
            "Talvez",
            "Não tenho certeza",
        ]

        for phrase in generic_responses:
            if phrase.lower() in text.lower():
                return "Hmpf… pergunta direito então."

        return text
def limpar_resposta(texto: str) -> str:
    lixo = [
        "como um modelo de linguagem",
        "não tenho sentimentos",
        "sou uma ia",
        "não posso"
    ]

    for l in lixo:
        texto = texto.replace(l, "")

    return texto.strip()
