

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Аналітика продажів E-commerce", layout="wide")

st.title("Аналітика продажів E-commerce")

csv_url = st.text_input("Вставте посилання на CSV з GitHub (raw):", 
                        "https://raw.githubusercontent.com/ТВОЙ_ЮЗЕРНЕЙМ/ТВОЙ_РЕПО/main/test_sales.csv")

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df['дата'] = pd.to_datetime(df['дата'])
    df['місяць'] = df['дата'].dt.to_period('M')
    return df

try:
    df = load_data(csv_url)
    st.success("Дані успішно завантажено!")
except:
    st.error("Не вдалося завантажити CSV. Перевірте посилання.")
    st.stop()

st.dataframe(df)

st.subheader("Pareto-аналіз продажів товарів (80/20)")
df_products = df.groupby('товар')['кількість'].sum().sort_values(ascending=False)
df_products_cumsum = df_products.cumsum() / df_products.sum()
pareto_80 = df_products_cumsum[df_products_cumsum <= 0.8]
st.write("Товари, що дають ~80% продажів:")
st.write(pareto_80)

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.barplot(x=df_products.index, y=df_products.values, ax=ax1)
ax1.set_title("Продажі товарів")
ax1.set_ylabel("Кількість")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Продажі по регіонах")
df_region = df.groupby('регіон')['кількість'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(x=df_region.index, y=df_region.values, palette="viridis", ax=ax2)
ax2.set_ylabel("Кількість")
st.pyplot(fig2)

st.subheader("Продажі по місяцях")
df_month = df.groupby('місяць')['кількість'].sum()
fig3, ax3 = plt.subplots(figsize=(10,5))
df_month.plot(kind='bar', color='skyblue', ax=ax3)
ax3.set_ylabel("Кількість")
ax3.set_xlabel("Місяць")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader("Середній чек")
if 'ціна' in df.columns:
    df['сумма'] = df['кількість'] * df['ціна']
    avg_check = df['сумма'].sum() / df['кількість'].sum()
    st.write(f"Середній чек: {avg_check:.2f} грн")
else:
    st.write("Колонка 'ціна' відсутня, середній чек не розрахований.")

st.subheader("Сезонність продажів")
df_monthly_sales = df.groupby('місяць')['кількість'].sum()
fig4, ax4 = plt.subplots(figsize=(10,5))
df_monthly_sales.plot(marker='o', ax=ax4)
ax4.set_ylabel("Кількість")
ax4.set_xlabel("Місяць")
st.pyplot(fig4)
