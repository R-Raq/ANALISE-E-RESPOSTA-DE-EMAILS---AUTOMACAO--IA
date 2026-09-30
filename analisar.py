from typing import Literal

from ollama import chat
from pydantic import BaseModel, Field


class AnaliseEmail(BaseModel):
    categoria: Literal[
        "financeiro",
        "suporte",
        "comercial",
        "reclamação",
        "spam",
        "outro"
    ]

    prioridade: Literal[
        "baixa",
        "media",
        "alta",
        "urgente"
    ]

    resumo: str

    precisa_humano: bool

    resposta_sugerida: str

email = print("Digite o e-mail:")
print("Finalize digitando FIM em uma nova linha.\n")


linhas = []


while True:

    linha = input()

    if linha == "FIM":
        break

    linhas.append(linha)


email = "\n".join(linhas)


prompt_sistema = """
Você é um sistema de triagem de emails corporativos, sua tarefa é analisar mensagens recebidas.
Classifique o e-mail e produza uma resposta sugerida.
A resposta sugerida deve ser educada, curta e profissional, nunca invente informações que não estejam disponíveis
no e-mail.
Quando o problema exigir consulta a sistemas internos, ou uma intervenção humana,
marque precisa_humano como true.
"""

resposta = chat(
    model="qwen3:8b",

    messages=[
        {
            "role": "system",
            "content": prompt_sistema
        },

        {
            "role": "user",
            "content": f"""
Analise este e-mail:

<email>
{email}
</email>
"""
        }
    ],

    format=AnaliseEmail.model_json_schema(),

    options={
        "temperature": 0
    }
)

analise = AnaliseEmail.model_validate_json(
    resposta.message.content
)


print("\n--- ANÁLISE DO E-MAIL ---")

print(f"Categoria: {analise.categoria}")
print(f"Prioridade: {analise.prioridade}")

print("\nResumo:")
print(analise.resumo)

print("\nPrecisa de atendimento humano?")
print("Sim" if analise.precisa_humano else "Não")

print("\nResposta sugerida:")
print(analise.resposta_sugerida)