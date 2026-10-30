from fastapi import FastAPI

app = FastAPI(
    title="GAT - Gerenciador de Atividades e Tempo",
    description="Diário de atividades e análise do tempo.",
    version="0.1.0",
)


@app.get("/")
def inicio():
    return {
        "aplicativo": "GAT",
        "descricao": "Diário de Atividades e Análise do Tempo",
        "versao": "0.1.0",
        "status": "em desenvolvimento",
    }


@app.get("/health")
def verificar_saude():
    return {
        "status": "ok",
        "servico": "GAT API",
    }