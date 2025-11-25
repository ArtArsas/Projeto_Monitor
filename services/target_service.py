import os 

FILE_CONFIG = "config/target_config.txt"
FILE_CONFIG_RISCO = "config/words_config.txt"

DEFAULT_TARGETS = [
    "CHROME",
    "GOOGLE CHROME",
    "FIREFOX",
    "EDGE",
    "DISCORD",
    "TELEGRAM",
    "WHATSAPP",
    "YOUTUBE",
    "FACEBOOK",
    "MINECRAFT",
    "ROBLOX",
    "FORTNITE",
    "BLOCO DE NOTAS",
    "BANCO",
    "PAGAMENTO",
    "PALWORLD",
    "PAL"
]

DEFAULT_RISK_WORDS = [
    "SUICIDIO",
    "SENHA",
    "DROGAS",
    "BULLYING"
]

#CARREGAR ARQUIVO DE TARGETS
def carregar_file_config():
    uploaded_target = []
    try:
        with open(FILE_CONFIG) as f:
            for linha in f:
                alvo_limpo = linha.strip().upper()
                if alvo_limpo:
                    uploaded_target.append(alvo_limpo)

        if not uploaded_target:
            print(f"AVISO: Arquivo de target vazio. Usando alvos padrão.")
            return DEFAULT_TARGETS
        
        print(f"✅ Configuração de Alvos carregada com sucesso: {len(uploaded_target)} programas monitorados.")
        return uploaded_target # Retorno de sucesso
    
    except FileNotFoundError:
        print(f"Arquivo de configuração '{FILE_CONFIG}' não encontrado. Usando valor padrão.")
        return DEFAULT_TARGETS
    except Exception as e:
        print(f"Erro ao carregar o arquivo de configuração: {e}. Usando valor padrão.")
        return DEFAULT_TARGETS
    
#CARREGAR ARQUIVO DE TARGETS
def carregar_words_config():
    uploaded_risco = []

    try:
        with open(FILE_CONFIG_RISCO, 'r') as f:
            for linha in f:
                palavra = linha.strip().upper()
                if palavra:
                    uploaded_risco.append(palavra)

        if not uploaded_risco:
            print(f"AVISO: Arquivo de risco vazio. Usando palavras padrão.")
            return DEFAULT_RISK_WORDS
        
        print(f"✅ Configuração de Risco carregada com sucesso: {len(uploaded_risco)} termos de alerta.")
        return uploaded_risco
        
    except FileNotFoundError:
        print(f"AVISO: Arquivo de risco '{FILE_CONFIG_RISCO}' não encontrado. Usando padrão.")
        return DEFAULT_RISK_WORDS
    
    except Exception as e:  
        print(f"ERRO ao carregar palavras de risco: {e}. Usando padrão.")
        return DEFAULT_RISK_WORDS
    
# TESTAR SE ARQUIVO DE KEYWORDS FOI CARREGADO
#TESTE = carregar_words_config()
#print(f"Status: {len(TESTE)} palavras carregadas.")
#print(f"Lista: {TESTE}")

def verificar_buffer(buffer_texto_maisuculo, palavras_de_risco):

    for palavra in palavras_de_risco:
        if palavra in buffer_texto_maisuculo:
            return palavra
        
    return None