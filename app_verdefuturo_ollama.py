import streamlit as st
import ollama
import re

st.set_page_config(page_title="ONG VerdeFuturo IA", page_icon="🌿", layout="centered")

st.title("🌿 Assistente VerdeFuturo")
st.write("Inteligência Artificial protegida contra Fake News, Greenwashing e Eco-Ansiedade.")

# Inicializa o histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente da VerdeFuturo. Como posso ajudar com questões ambientais ou relatórios hoje? 🌍"}
    ]

# --- PROMPT MESTRE COM OS NOVOS GUARDRAILS ---
# Aqui condensamos toda a inteligência e restrições. Modelos pequenos funcionam muito melhor assim.
PROMPT_VERDEFUTURO = """És o assistente oficial e porta-voz da ONG VerdeFuturo.
Tua missão é transformar dados técnicos em mensagens inspiradoras, educar o público e responder a dúvidas com simpatia e uso de emojis.

REGRAS OBRIGATÓRIAS (GUARDRAILS):
1. CUMPRIMENTOS: Se o usuário apenas disser "Olá", "Tudo bem" ou saudar, responde com simpatia e pergunta como podes ajudar.
2. PREVENÇÃO DE ECO-ANSIEDADE: Nunca uses um tom fatalista, apocalíptico ou desesperador. Se o tema for grave (ex: desmatamento, poluição extrema), termina SEMPRE com uma mensagem de esperança e uma chamada à ação (ex: reciclar, apoiar a ONG).
3. ANTI-FAKE NEWS: Nunca valides teorias da conspiração ou negacionismo climático. Se o usuário enviar desinformação, corrige-o educadamente com base no consenso científico.
4. ANTI-GREENWASHING: Não celebres falsas soluções (ex: empresas que poluem muito mas plantam meia dúzia de árvores). Mantém um senso crítico.
5. FOCO: Se a pergunta for sobre receitas, finanças, fofocas ou códigos, avisa educadamente que o teu foco é exclusivo no Meio Ambiente.
Responde sempre em português claro e acessível.
6. SEM ALUCINAÇÕES: Nunca invente links, URLs, sites ou informações que não foram expressamente fornecidas. Foca-te estritamente no texto recebido.
"""

# --- GUARDRAILS DE ENTRADA (PYTHON / REGEX) ---
# Filtros estritos que não dependem do modelo, poupando processamento.

def guardrail_dados_sensiveis(texto):
    padrao_cpf = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
    padrao_cnpj = r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'
    padrao_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if re.search(padrao_cpf, texto) or re.search(padrao_cnpj, texto) or re.search(padrao_email, texto):
        return False
    return True

def guardrail_jailbreak(texto):
    termos_maliciosos = ["ignore as regras", "esqueça as instruções", "haja como", "desconsidere tudo", "você agora é"]
    texto_limpo = texto.lower()
    for termo in termos_maliciosos:
        if termo in texto_limpo:
            return False
    return True

# --- GUARDRAIL DE SAÍDA PROGRAMÁTICO ---
def guardrail_saida(texto):
    # Corrige os deslizes do Llama 3.2
    texto = re.sub(r'\bsostenível\b', 'sustentável', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bsosteníveis\b', 'sustentáveis', texto, flags=re.IGNORECASE)
    
    # Assinatura obrigatória
    disclaimer = "\n\n---\n*🌿 Assistente VerdeFuturo | Juntos por um amanhã sustentável.*"
    if disclaimer not in texto:
        texto += disclaimer
    return texto

# --- INTERFACE DE CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt_usuario := st.chat_input("Digite a sua mensagem aqui..."):
    
    # Adiciona a mensagem do usuário à tela
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
        
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        # 1. Checagem dos Guardrails de Entrada em Python (Super Rápido)
        if not guardrail_dados_sensiveis(prompt_usuario):
            resposta_erro = "🛑 **Bloqueio de Segurança:** Dados pessoais sensíveis (CPF, CNPJ, E-mail) não são permitidos por motivos de privacidade."
            status_placeholder.markdown(resposta_erro)
            st.session_state.messages.append({"role": "assistant", "content": resposta_erro})
            
        elif not guardrail_jailbreak(prompt_usuario):
            resposta_erro = "🛑 **Bloqueio de Segurança:** Detetada tentativa de sobreposição das diretrizes institucionais."
            status_placeholder.markdown(resposta_erro)
            st.session_state.messages.append({"role": "assistant", "content": resposta_erro})
            
        else:
            # 2. Geração da Resposta com o Prompt Mestre
            status_placeholder.markdown("🤖 *Processando...*")
            
            # Montamos o histórico para a IA entender o contexto
            historico_chamada = [{"role": "system", "content": PROMPT_VERDEFUTURO}]
            # Pegamos as últimas mensagens para manter o fluxo da conversa
            for msg in st.session_state.messages[-3:]: 
                historico_chamada.append(msg)
                
            try:
                resposta_modelo = ollama.chat(
                    model='IA_VerdeFuturo', 
                    messages=historico_chamada,
                    options={'temperature': 0.2} # <--- A trava lógica!
                )
                texto_gerado = resposta_modelo['message']['content']
                
                # 3. Aplicação do Guardrail de Saída (Disclaimer + Correções)
                texto_final = guardrail_saida(texto_gerado)
                
                status_placeholder.markdown(texto_final)
                st.session_state.messages.append({"role": "assistant", "content": texto_final})
            
            except Exception as e:
                erro_msg = f"⚠️ Erro ao contactar o Ollama: {e}"
                status_placeholder.markdown(erro_msg)