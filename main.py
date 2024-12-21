import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Function to scrape prices
def scrape_prices(url):
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Wait for elements to load
    wait = WebDriverWait(driver, 3)
    elementos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "olx-ad-card__price")))

    # List to store prices
    precos = []

    # Extract prices
    for i, elemento in enumerate(elementos):
        preco = elemento.text.strip()
        if preco:
            precos.append(preco)

    # Convert prices to float
    precos_float = []
    for preco in precos:
        try:
            preco_clean = preco.replace("R$", "").replace(".", "").replace(",", ".")
            if "mil" in preco_clean:
                preco_clean = preco_clean.replace("mil", "").strip()
                preco_float = float(preco_clean) * 1000
            else:
                preco_float = float(preco_clean)
            precos_float.append(preco_float)
        except ValueError:
            continue  # Skip invalid prices

    # Close the browser
    driver.quit()

    return precos_float

# Streamlit UI
st.title("Preços do Olx")

# Input para o URL
url = st.text_input("Insira o url do Olx e pressione enter:")

if url:
    with st.spinner("Carregando..."):
        prices = scrape_prices(url)
        
        if prices:
            st.success("Preços carregados com sucesso!")
            st.write(f"Foram encontrados {len(prices)} preços.")
            
            #Exibe os preços em um dataframe e um gráfico de linha
            df = pd.DataFrame(prices, columns=["Preço (R$)"])
            st.line_chart(df)
            st.dataframe(df)
                      
            # Opção de baixar como arquivo CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Baixar como  CSV",
                data=csv_data,
                file_name="precos.csv",
                mime="text/csv"
            )
        else:
            st.warning("Nenhum preço encontrado. Verifique o URL inserido.")