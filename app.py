import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Da Maju Confeitaria", layout="centered")

# Estilo visual
st.markdown("""
<style>
    .stApp { background-color: #fffafc; }
    h1, h2, h3 { color: #800080; }
    .stButton>button { background-color: #800080; color: white; border-radius: 10px; padding: 0.5em 1.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("Calculadora Da Maju Confeitaria")

# INGREDIENTES
with st.expander("Ingredientes"):
    num_ing = st.number_input("Quantos ingredientes?", min_value=1, max_value=20, value=5)
    ingredientes = []
    for i in range(num_ing):
        cols = st.columns([3, 1, 1, 1, 1])
        nome = cols[0].text_input(f"Nome do ingrediente {i+1}", key=f"nome{i}")
        qtd_usada = cols[1].number_input("Quantidade usada", min_value=0.0, key=f"qtd{i}")
        unidade = cols[2].selectbox("Unidade", ["g", "kg", "ml", "l", "un", "caixa"], key=f"uni{i}")
        qtd_emb = cols[3].number_input("Qtd por embalagem", min_value=0.01, key=f"emb{i}")
        preco_emb = cols[4].number_input("Preço da embalagem (R$)", min_value=0.01, key=f"preco{i}")

        if nome:
            custo = (qtd_usada / qtd_emb) * preco_emb
            ingredientes.append({
                "Ingrediente": nome,
                "Quantidade usada": f"{qtd_usada} {unidade}",
                "Custo (R$)": round(custo, 2)
            })

    if ingredientes:
        df_ingredientes = pd.DataFrame(ingredientes)
        st.table(df_ingredientes)
        custo_ingredientes = df_ingredientes["Custo (R$)"].sum()
        st.success(f"Custo total dos ingredientes: R$ {custo_ingredientes:.2f}")

# CUSTOS FIXOS E VARIÁVEIS
with st.expander("Custos Fixos e Variáveis"):
    st.write("Inclua custos como luz, gás, água, internet, aluguel etc.")
    num_custos = st.number_input("Quantos custos deseja adicionar?", min_value=1, max_value=15, value=3)
    custos = {}
    for i in range(num_custos):
        nome = st.text_input(f"Nome do custo {i+1}", key=f"nome_custo{i}")
        valor = st.number_input(f"Valor mensal do custo {i+1} (R$)", min_value=0.0, key=f"valor_custo{i}")
        if nome:
            custos[nome] = valor
    total_custos = sum(custos.values())
    st.success(f"Total dos custos mensais: R$ {total_custos:.2f}")

# TEMPO DE PRODUÇÃO / HORA TRABALHADA
with st.expander("Tempo de Produção"):
    tempo_horas = st.number_input("Horas de trabalho por unidade produzida", min_value=0.0, value=3.0)
    valor_hora = st.number_input("Valor da hora de trabalho (R$)", min_value=0.0, value=10.0)
    custo_tempo = tempo_horas * valor_hora
    st.info(f"Custo do tempo de produção: R$ {custo_tempo:.2f}")

# PRODUÇÃO MENSAL E CUSTO INDIRETO
with st.expander("Produção Mensal"):
    producao_mensal = st.number_input("Quantidade produzida por mês", min_value=1, value=10)
    custo_indireto_unitario = (total_custos + custo_tempo) / producao_mensal
    st.info(f"Custo indireto por unidade: R$ {custo_indireto_unitario:.2f}")

# LUCRO E RESULTADO FINAL
with st.expander("Lucro e Preço Final"):
    margem_lucro = st.slider("Margem de lucro (%)", 0, 200, 30)
    custo_total_unitario = custo_ingredientes + custo_indireto_unitario
    preco_venda = custo_total_unitario * (1 + margem_lucro / 100)
    st.success(f"Preço sugerido de venda: R$ {preco_venda:.2f}")

# OBSERVAÇÃO FINAL
st.caption("Todos os campos são personalizáveis. O valor da hora trabalhada é apenas um exemplo e pode ser ajustado conforme a realidade do seu negócio.")
