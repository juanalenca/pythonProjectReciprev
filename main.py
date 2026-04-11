import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple, Any

# Instalando o ChromeDriver Manager correspondente à sua versão atual
servico = Service(ChromeDriverManager().install())

# Diretórios Dinâmicos para Extensão e Dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE_DIR, 'dados')
os.makedirs(PASTA_DADOS, exist_ok=True)

ARQUIVO_DADOS = os.path.join(PASTA_DADOS, 'dados_medicos.txt')

# Busca a extensão do Chrome de forma inteligente no User da máquina
LOCAL_APP_DATA = os.getenv('LOCALAPPDATA', '')
EXTENSAO_PATH = os.path.join(
    LOCAL_APP_DATA, 'Google', 'Chrome', 'User Data', 'Default',
    'Extensions', 'hlifkpholllijblknnmbfagnkjneagid', '0.2.1_0'
)


def iniciar_navegador() -> uc.Chrome:
    """Inicia o navegador com Bypass em modo undetected e carrega extensões locais."""
    options = uc.ChromeOptions()
    
    if os.path.exists(EXTENSAO_PATH):
        options.add_argument(f'--load-extension={EXTENSAO_PATH}')
    else:
        print(f"⚠️ Extensão não encontrada em {EXTENSAO_PATH}. Iniciando sem ela.")

    return uc.Chrome(service=servico, options=options)


def acessar_e_configurar_pesquisa(navegador: uc.Chrome) -> uc.Chrome:
    """Acessa o portal e executa cliques automatizados nos selects de busca."""
    while True:
        try:
            navegador.get("https://portal.cfm.org.br/busca-medicos/?uf=PE")
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            # Situação -> ativo
            navegador.find_element(By.XPATH, '//*[@id="tipoSituacao"]').click()
            time.sleep(0.5)
            navegador.find_element(By.XPATH, '//*[@id="tipoSituacao"]/option[2]').click()
            time.sleep(1)
            
            # Situação -> regular
            navegador.find_element(By.XPATH, '//*[@id="situacao"]').click()
            time.sleep(0.6)
            navegador.find_element(By.XPATH, '//*[@id="situacao"]/option[4]').click()
            time.sleep(1)
            
            # UF -> PE
            navegador.find_element(By.XPATH, '//*[@id="uf"]').click()
            time.sleep(0.55)
            navegador.find_element(By.XPATH, '//*[@id="uf"]/option[17]').click()
            time.sleep(1)
            
            # Enviar e aguardando o carregamento da pesquisa
            navegador.find_element(By.XPATH, '//*[@id="buscaForm"]/div/div[4]/div[2]/button').click()
            time.sleep(35)
            
            # Verificar a presença da lista de médicos através do CRM
            verificacao_medicos = navegador.find_elements(By.XPATH, '//div[b[contains(text(), "CRM:")]]')
            if verificacao_medicos:
                break
            else:
                raise Exception("Elemento do CRM não encontrado\n")
                
        except Exception as e:
            print("Elemento do CRM não encontrado, fechando e reabrindo a página.")
            navegador.close()
            navegador = iniciar_navegador()
            time.sleep(1)
            
    return navegador


def extrair_dados(navegador: uc.Chrome) -> Tuple[List[Any], List[Any], List[Any]]:
    """Mapeia o DOM para extrair H4(nomes), CRMs e Especialidades(RQEAs)."""
    elementos_h4 = navegador.find_elements(By.TAG_NAME, 'h4')
    elementos_crm = navegador.find_elements(By.XPATH, '//div[b[contains(text(), "CRM:")]]')
    
    # Tratamento de XPATH longo para RQEA
    xpath_rqea = '//div[contains(@class, "col-md-12") and (br or span) and not(b[text()="Inscrições em outro estado:"])]'
    elementos_rqea = navegador.find_elements(By.XPATH, xpath_rqea)
    
    return elementos_h4, elementos_crm, elementos_rqea


def salvar_dados(elementos_h4: List[Any], elementos_crm: List[Any], elementos_rqea: List[Any], 
                 page_num: int, arquivo: str) -> None:
    """Estrutura os blocos tabulares de texto padronizados e arquiva no .txt."""
    with open(arquivo, 'a', encoding='utf-8') as file:
        file.write(f"\nDados da página {page_num}:\n")
        
        nome_col_width = 40
        crm_col_width = 20
        especialidade_col_width = 200
        
        file.write(f"{'Nome':<{nome_col_width}}{'CRM':<{crm_col_width}}{'Especialidade':<{especialidade_col_width}}\n")
        file.write(f"{'-' * nome_col_width}{'-' * crm_col_width}{'-' * especialidade_col_width}\n\n")
        
        print(f"\nSalvando dados da página {page_num}...")
        for h4, crm, rqea in zip(elementos_h4, elementos_crm, elementos_rqea):
            nome = h4.text[:nome_col_width-1]  # Limita string muito longa
            crm_text = crm.text.strip()[:crm_col_width-1]
            rqea_text = rqea.text.strip()[:especialidade_col_width-1]
            file.write(f"{nome:<{nome_col_width}}{crm_text:<{crm_col_width}}{rqea_text:<{especialidade_col_width}}\n\n\n")
            
        file.write("\n")
    print(f"Dados da página {page_num} salvos com sucesso.\n\n")


def ler_dados_primeira_pagina(arquivo: str) -> List[str]:
    """Lê a memória do TXT para resgatar status de CRM de validação das primeiras buscas."""
    dados_primeira_pagina = {'h4': [], 'crm': [], 'rqea': []}
    with open(arquivo, 'r', encoding='utf-8') as file:
        print(f"Lendo dados da primeira página do arquivo...\n")
        for linha in file:
            if linha.startswith('Nome'):
                continue
            if '-' * 40 in linha:
                break
                
            partes = linha.strip().split(None, 2)
            if len(partes) == 3:
                dados_primeira_pagina['h4'].append(partes[0])
                dados_primeira_pagina['crm'].append(partes[1])
                dados_primeira_pagina['rqea'].append(partes[2])
                
    print(f"Dados da primeira página lidos: {dados_primeira_pagina}\n\n\n")
    return dados_primeira_pagina['crm']


def comparar_dados(elementos_crm: List[Any], dados_primeira_pagina_crm: List[str]) -> bool:
    """Compara CRMs da tela atual com a matriz em cache para detectar se houveram falhas de repetição de página."""
    elementos_crm_texts = [crm.text.strip() for crm in elementos_crm]

    print(f"Dados atuais da página:\nCRM: {elementos_crm_texts}\n")
    print(f"Dados da primeira página:\nCRM: {dados_primeira_pagina_crm}\n")

    comparacao = set(elementos_crm_texts) == set(dados_primeira_pagina_crm)

    print(f"Comparação dos CRMs resultou em: {'IDÊNTICOS :(' if comparacao else 'DIFERENTES :)'}\n\n\n")
    return comparacao


def clicar_botao_paginacao(navegador: uc.Chrome, page_num: int) -> bool:
    """Espera e clica na próxima página numerada do site da CFM."""
    try:
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xpath_pag = f'//ul/li[@class="paginationjs-page J-paginationjs-page" and @data-num="{page_num}"]'
        
        elemento_paginacao = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath_pag))
        )
        time.sleep(2)
        elemento_paginacao.click()
        time.sleep(35)
        return True
    except Exception as e:
        print(f"Erro ao clicar no botão de paginação da página {page_num}: {e}")
        return False


def orquestrar_main() -> None:
    # Definindo o caminho absoluto do arquivo onde os dados serão salvos de forma dinâmica
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as file:
        file.write("") # Limpa cache do diretório de destino
        
    print(f"[*] Os Relatórios serão arquivados em: {ARQUIVO_DADOS}")

    # Iniciando o navegador e configurando a pesquisa
    navegador = iniciar_navegador()
    navegador = acessar_e_configurar_pesquisa(navegador)

    # Extraindo e salvando dados da primeira página
    elementos_h4_primeira, elementos_crm_primeira, elementos_rqea_primeira = extrair_dados(navegador)
    salvar_dados(elementos_h4_primeira, elementos_crm_primeira, elementos_rqea_primeira, 1, ARQUIVO_DADOS)

    # Lendo os dados da primeira página do arquivo
    dados_primeira_pagina_crm = [crm.text.strip() for crm in elementos_crm_primeira]

    # Varrer páginas até a quantia total mapeada
    page_num = 2
    TOTAL_PAGINAS_ALVO = 2504

    while page_num <= TOTAL_PAGINAS_ALVO:
        try:
            if not clicar_botao_paginacao(navegador, page_num):
                print(f"Atenção: Não encontrou o elemento de paginação para a página {page_num}!\n")
                break

            elementos_h4_atual, elementos_crm_atual, elementos_rqea_atual = extrair_dados(navegador)

            # Mitigação de repetição de página (falha site CFM/Conexão)
            while comparar_dados(elementos_crm_atual, dados_primeira_pagina_crm):
                print(f"CRMs da página {page_num} idênticos à base! Retornando o bot para corrigir.")
                print("-" * 100)

                if not clicar_botao_paginacao(navegador, page_num - 1):
                    break
                time.sleep(10)

                if not clicar_botao_paginacao(navegador, page_num):
                    break
                time.sleep(10)

                elementos_h4_atual, elementos_crm_atual, elementos_rqea_atual = extrair_dados(navegador)

            salvar_dados(elementos_h4_atual, elementos_crm_atual, elementos_rqea_atual, page_num, ARQUIVO_DADOS)
            page_num += 1

        except Exception as e:
            print(f"Erro Crítico de Driver ao tentar processar {page_num}: {e}")
            navegador.close()
            time.sleep(5)
            
            # Recuperação Resiliente de Desconexão / IP block
            navegador = iniciar_navegador()
            navegador = acessar_e_configurar_pesquisa(navegador)
            
            elementos_h4_primeira, elementos_crm_primeira, elementos_rqea_primeira = extrair_dados(navegador)
            salvar_dados(elementos_h4_primeira, elementos_crm_primeira, elementos_rqea_primeira, page_num, ARQUIVO_DADOS)
            dados_primeira_pagina_crm = [crm.text.strip() for crm in elementos_crm_primeira]

if __name__ == "__main__":
    orquestrar_main()
