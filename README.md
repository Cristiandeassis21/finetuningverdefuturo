# 🚀 Pipeline de MLOps: Fine-Tuning Especializado e Guardrails Locais

### Customização do Modelo Mistral-7B-Instruct-v0.3 para a ONG VerdeFuturo usando QLoRA, Ollama e Streamlit

Este repositório contém o ciclo completo de desenvolvimento de uma aplicação de Inteligência Artificial Generativa focada em nicho. O objetivo do projeto foi transformar dados científicos, métricas frias e jargões ambientais complexos em mensagens institucionais inspiradoras, assertivas e seguras para a ONG **VerdeFuturo**, tudo rodando localmente em um hardware com restrição de recursos (8 GB de RAM).

---

## 🏗️ Arquitetura do Pipeline (End-to-End)

O projeto foi estruturado seguindo uma abordagem híbrida de engenharia de IA, dividida em quatro fases principais:

* **Fase 1: Preparação do Dataset:** Criação de um conjunto de dados especializado no formato de Instrução e Resposta, ensinando à IA o tom de voz da ONG.
* **Fase 2: O Treinamento (Google Colab):** Uso de uma GPU de nuvem (NVIDIA T4) para injetar esse conhecimento através de **Fine-Tuning via QLoRA**.
* **Fase 3: A Otimização (GGUF):** Conversão exclusiva dos novos neurônios gerados em um arquivo compacto `.gguf` (~54.5 MB).
* **Fase 4: O Ambiente Local:** Execução otimizada através do **Ollama** e uma interface web construída em **Streamlit**.

---

## 🛡️ Estratégia de Segurança e Guardrails (Defesa em Profundidade)

Seguindo os princípios de governança de GenAI modernos, o sistema conta com camadas sobrepostas de validação:

* **Camada de Modelo (Internalização):** O tom de voz acolhedor e ecológico foi embutido diretamente nos pesos do adaptador através do fine-tuning.
* **Camada de Prompt (Input & Behavioral Rails):** Injeção de instruções de sistema estritas no código local para prevenir desvios de assunto e conter pânico de eco-ansiedade.
* **Camada de Saída (Output Rails & Fact-Checking):** Implementação de uma trava lógica no Streamlit forçando a **Temperatura em 0.2**. Esta restrição removeu por completo as alucinações de links e URLs inventadas pelo modelo, garantindo respostas estritamente factuais.

---

## 🧪 Exemplos de Prompts para Teste (Perguntas Modelo)

Para testar a eficácia do Fine-Tuning e dos Guardrails na interface do Streamlit, copie e cole os textos técnicos abaixo no chat da IA. 

**1. Teste de Reciclagem e Economia Circular:**
> "Traduza o seguinte dado técnico: Aumento de 35% na triagem de polímeros de alta densidade (PEAD) no ecoponto do bairro no último trimestre."
* **O que observar:** A IA deve traduzir "PEAD" para uma linguagem acessível (como "plásticos rígidos/pesados") e aplicar um tom comemorativo e engajador, sem inventar links externos.

**2. Teste de Biodiversidade Local:**
> "Traduza o seguinte dado técnico: Registro de eclosão de 120 ninhos de tartaruga-de-pente na costa de João Pessoa, com taxa de sobrevivência juvenil de 85%."
* **O que observar:** O modelo deve focar na vitória da preservação local, usando um tom acolhedor, focado em esperança e usando emojis adequados à natureza (🐢🌊).

**3. Teste do Filtro de Eco-Ansiedade (Guardrail Comportamental):**
> "Traduza o seguinte dado: Níveis de turbidez da água do estuário atingiram 45 NTU após as chuvas, mas a nova barreira de contenção natural bloqueou 60% dos sedimentos."
* **O que observar:** Pela regra de evitar o fatalismo, o modelo não deve focar nos sedimentos que passaram, mas sim no sucesso da barreira de contenção natural, mantendo o usuário focado na ação climática positiva.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Configurar o Modelo Customizado no Ollama

Certifique-se de ter o arquivo `lora_verdefuturo.gguf` e o `Modelfile` na mesma pasta. No terminal, compile o modelo:

```bash
ollama create IA_VerdeFuturo -f Modelfile
```

### 2. Instalar as Dependências do Python

Ative o ambiente virtual e instale os pacotes necessários executando os comandos no terminal:

```bash
# Ativar o venv no Windows:
venv\Scripts\activate

# Instalar as bibliotecas necessárias:
pip install streamlit ollama
```

### 3. Rodar o Aplicativo

Inicie o servidor local do Streamlit com o seguinte comando:

```bash
streamlit run app_verdefuturo_ollama.py
```