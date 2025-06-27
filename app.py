import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Preços - Kit Festa", layout="centered")

st.markdown("""
<style>
    .main { background-color: #fffbea; }
    h1, h2, h3 { color: #800080; }
    .stButton > button { background-color: #800080; color: white; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("🧁 Calculadora de Preço por Receita - Kit Festa")
st.subheader("Insira os ingredientes e os custos da produção")

st.markdown("---")

# Ingredientes
st.markdown("### Ingredientes Usados")
with st.expander("Adicionar Ingredientes"):
    ingredientes = []
    num = st.number_input("Quantos ingredientes você vai adicionar?", min_value=1, max_value=20, value=5)
    for i in range(num):
        st.markdown(f"**Ingrediente {i+1}**")
        nome = st.text_input(f"Nome do ingrediente {i+1}", key=f"nome{i}")
        qtd_usada = st.number_input(f"Quantidade usada (ex: 300)", key=f"qtd{i}", min_value=0.0)
        unidade = st.selectbox(f"Unidade", ["g", "kg", "ml", "l", "un", "caixa"], key=f"uni{i}")
        qtd_emb = st.number_input(f"Quantidade na embalagem comprada", key=f"emb{i}", min_value=0.01)
        preco_emb = st.number_input(f"Preço da embalagem comprada", key=f"preco{i}", min_value=0.01)
        if nome:
            custo_prop = (qtd_usada / qtd_emb) * preco_emb
            ingredientes.append({
                "Ingrediente": nome,
                "Qtd usada": qtd_usada,
                "Unidade": unidade,
                "Custo": round(custo_prop, 2)
            })

# Mostrar tabela de custos
if ingredientes:
    df = pd.DataFrame(ingredientes)
    st.markdown("#### Custo dos Ingredientes")
    st.dataframe(df)
    total_direto = sum([item['Custo'] for item in ingredientes])
    st.success(f"Custo total dos ingredientes: R$ {total_direto:.2f}")

# Custos fixos mensais
st.markdown("---")
st.markdown("### Custos Fixos Mensais")
gas = st.number_input("Gás (mensal)", value=130.0)
luz = st.number_input("Luz (mensal)", value=150.0)
tempo_horas = st.number_input("Horas gastas por receita", value=3.0)
valor_hora = st.number_input("Valor da sua hora de trabalho (R$)", value=15.0)

custo_tempo = tempo_horas * valor_hora
st.info(f"Custo de trabalho por receita: R$ {custo_tempo:.2f}")

total_mensal = gas + luz + custo_tempo
producoes_mes = st.number_input("Quantas receitas (ou bolos) por mês?", value=10, min_value=1)
custo_indireto_unit = total_mensal / producoes_mes
st.success(f"Custo indireto por receita: R$ {custo_indireto_unit:.2f}")

# Lucro
st.markdown("---")
st.markdown("### Margem de Lucro")
lucro = st.slider("Margem de lucro (%)", 0, 200, 30)

# Resultado final
st.markdown("---")
if st.button("Calcular Preço Final"):
    preco_total = total_direto + custo_indireto_unit
    preco_venda = preco_total * (1 + lucro / 100)
    st.markdown(f"## 💰 Preço de Venda Sugerido: **R$ {preco_venda:.2f}**")
    st.caption("Cálculo: (Custo Direto + Indireto) + Lucro")

