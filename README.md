# 🩺 Automação CFM | Web Scraper de Médicos (Pernambuco)

> Um robô extrator resiliente, construído em Python, para mineração ativa de registros profissionais no portal do CFM.

O **Projeto Automação CFM** é um Web Scraper especializado desenvolvido para navegar de forma autônoma e silenciosa na base de dados pública do **Conselho Federal de Medicina (CFM)**. Utilizando automação inteligente de navegadores (Bypass via Undetected ChromeDriver), ele rastreia milhares de páginas extraindo o status de atuação, nome, CRM e RQEAs (especialidades) de profissionais regulamentados ativamente, especificamente mapeados no estado de Pernambuco.

---

## 🔥 Principais Funcionalidades

- **Interação "Human-Like":** Desvia ativamente de sistemas de proteção ou bloqueios da Cloudflare do site da CFM operando sobre a biblioteca `undetected_chromedriver`.
- **Extração Analítica Robusta:** Coleta, higieniza e categoriza (Nome, CRM, Especialidades) os dados de mais de *2.500 páginas de registros* na sequência.
- **Tolerância a Falhas e Resiliência (Anti-Crash):** Diferente de scripts básicos, ele conta com lógicas avançadas de auto-validação. Caso detecte repetições de página devido a instabilidades da internet ou erros no DOM, ele pausa, volta o navegador ou reinicia as conexões sozinho na mesma página onde falhou.
- **Gerenciador de Driver Automático:** Utiliza `webdriver_manager` para sempre baixar localmente a versão correta do Chrome equivalente ao seu sistema (Zero configurações manuais no PATH).

---

## 🛠 Tecnologias Utilizadas

Este projeto foi construído utilizando as melhores ferramentas para automação de Browser e Engenharia de Dados Leve:

*   **[Python 3.x](https://www.python.org/)** - Linguagem base do projeto.
*   **[Selenium WebDriver](https://www.selenium.dev/)** - Responsável pela simulação estrutural de ponta a ponta dos cliques e preenchimentos orgânicos dos `<select>` do site.
*   **[Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)** - Modificação oficial do driver para mascarar as intenções de robô.
*   **[Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager)** - Instalador dinâmico de binários dos navegadores.

---

## 💻 Instalação e Execução

### Pré-requisitos
Certifique-se de que o **Python 3.8+** esteja instalado em sua máquina e o navegador nativo `Google Chrome` esteja atualizado.

### Configuração Inicial

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/juanalenca/Projeto-Automacao-Medicos.git
   cd Projeto-Automacao-Medicos
   ```

2. **Instale as as dependências através do requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o Robô:**
   ```bash
   python main.py
   ```
   *Após rodar, o robô automaticamente extrairá a interface, clicará nos escopos de Pernambuco, aplicará as formatações e começará a jogar rodada por rodada os relatórios extraídos localmente dentro do arquivo final `dados/dados_medicos.txt`!*

---

> [!WARNING]
> *Este projeto possui fins estritamente analíticos ou para automação pessoal da coleta de chaves públicas indexadas na web, operando como prova de conceito para projetos engajados no respeito das barreiras locais.*
