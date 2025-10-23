
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_url = "https://raw.githubusercontent.com/ТВОЙ_ЮЗЕРНЕЙМ/ТВОЙ_РЕПО/main/sales.csv"
df = pd.read_csv(csv_url)

print(df.head())

df_products = df.groupby('товар')['кількість'].sum().sort_values(ascending=False)
df_products_cumsum = df_products.cumsum() / df_products.sum()
pareto_80 = df_products_cumsum[df_products_cumsum <= 0.8]
print("\nТовари, що дають 80% продажів:\n", pareto_80)

plt.figure(figsize=(10,6))
sns.barplot(x=df_products.index, y=df_products.values)
plt.xticks(rotation=45)
plt.title("Pareto-аналіз продажів товарів")
plt.ylabel("Кількість проданих одиниць")
plt.tight_layout()
plt.show()

df_region = df.groupby('регіон')['кількість'].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
sns.barplot(x=df_region.index, y=df_region.values, palette="viridis")
plt.title("Продажі по регіонах")
plt.ylabel("Кількість проданих одиниць")
plt.show()

df['дата'] = pd.to_datetime(df['дата'])
df['місяць'] = df['дата'].dt.to_period('M')
df_month = df.groupby('місяць')['кількість'].sum()
plt.figure(figsize=(10,5))
df_month.plot(kind='bar', color='skyblue')
plt.title("Продажі по місяцях")
plt.ylabel("Кількість проданих одиниць")
plt.xticks(rotation=45)
plt.show()


if 'ціна' in df.columns:
    df['сумма'] = df['кількість'] * df['ціна']
    avg_check = df['сумма'].sum() / df['кількість'].sum()
    print(f"\nСередній чек: {avg_check:.2f} грн")
else:
    print("\nКолонка 'ціна' відсутня, середній чек не розрахований.")

df_monthly_sales = df.groupby('місяць')['кількість'].sum()
plt.figure(figsize=(10,5))
df_monthly_sales.plot(marker='o')
plt.title("Сезонність продажів")
plt.ylabel("Кількість проданих одиниць")
plt.xticks(rotation=45)
plt.show()
