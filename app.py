import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Da Maju Confeitaria", layout="centered")

# Cores e estilo
st.markdown("""
<style>
    .stApp { background-color: #fffafc; }
    h1, h2, h3 { color: #800080; }
    .stButton>button { background-color: #800080; color: white; border-radius: 10px; padding: 0.5em 1.5em; font-weight: bold; }
    .divider { border-top: 2px solid #800080; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

st.title("Calculadora Da Maju Confeitaria")
st.write("Organize sua precificação com clareza e eficiência.")

# Ingredientes
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.header("Ingredientes")
num = st.number_input("Quantos ingredientes?", min_value=1, max_value=20, value=5)
ing_list = []
columns_ing = st.columns([3, 1, 1, 1, 1])
for col, label in zip(columns_ing, ["Nome", "Qtd usada", "Unidade", "Qtd emb.", "R$ Embalagem"]):
    col.markdown(f"*{label}*")

for i in range(num):
    cols = st.columns([3, 1, 1, 1, 1])
    nome = cols[0].text_input(f"Ingrediente {i+1}", key=f"nome{i}")
    qtd_usada = cols[1].number_input("", key=f"qtd{i}", min_value=0.0)
    unidade = cols[2].selectbox("", ["g", "kg", "ml", "l", "un", "caixa"], key=f"uni{i}")
    qtd_emb = cols[3].number_input("", key=f"emb{i}", min_value=0.01)
    prec_emb = cols[4].number_input("", key=f"pre{i}", min_value=0.01)
    if nome:
        custo = (qtd_usada / qtd_emb) * prec_emb
        ing_list.append({
            "Ingrediente": nome,
            "Qtd usada": f"{qtd_usada} {unidade}",
            "Custo (R$)": round(custo, 2)
        })

if ing_list:
    df_ing = pd.DataFrame(ing_list)
    st.table(df_ing)
    total_direto = df_ing["Custo (R$)"].sum()
    st.success(f"Custo total dos ingredientes: R$ {total_direto:.2f}")

# Custos fixos mensais
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.header("Custos Fixos Mensais")
custos = {}
num_costs = st.number_input("Quantos custos fixos deseja incluir?", min_value=1, max_value=10, value=3)
for j in range(num_costs):
    name = st.text_input(f"Nome do custo {j+1}", value=["Gás","Luz","Tempo trabalhado (em horas)"][j] if j<3 else "", key=f"name{j}")
    val = st.number_input(f"Valor R$ {name or j+1}", min_value=0.0, key=f"cost{j}")
    if name:
        custos[name] = val

# Valor da hora de trabalho
if "Tempo trabalhado" in "".join(custos.keys()) or any("tempo" in k.lower() for k in custos.keys()):
    st.markdown("\n*Obs.:* Valor da hora de trabalho é apenas um exemplo. Altere conforme desejar.")

total_mensal = sum(custos.values())
producoes = st.number_input("Produções por mês", min_value=1, value=10)
indireto = total_mensal / producoes
st.info(f"Custo indireto por unidade: R$ {indireto:.2f}")

# Lucro e preço final
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.header("Preço de Venda")
lucro = st.slider("Margem de Lucro (%)", 0, 200, 30)
if st.button("Calcular"):
    preco_total = total_direto + indireto
    final = preco_total * (1 + lucro/100)
    st.markdown(f"### Preço sugerido: R$ {final:.2f}")
    st.caption("Cálculo: Custo Direto + Indireto + Lucro")

# Observação
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.caption("Custo indireto por unidade = soma dos custos fixos dividido pelo total de produções mensais.")
