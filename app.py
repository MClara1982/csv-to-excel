# Importa o Streamlit, que serve para criar a interface web (UI)
import streamlit as st

# Importa o Pandas, usado para ler o CSV e trabalhar com dados em tabelas
import pandas as pd

# Importa BytesIO para guardar o ficheiro Excel em memória
# (sem criar ficheiros temporários no disco)
from io import BytesIO


# Configuração básica da página (título no browser e ícone)
st.set_page_config(page_title="CSV → Excel", page_icon="📄")

# Título principal da aplicação
st.title("CSV-to-Excel")

# Texto explicativo simples para o utilizador
st.write("Carrega um ficheiro CSV e faz download do Excel convertido.")


# Cria um botão de upload de ficheiros
# Aceita apenas ficheiros com extensão .csv
csv_file = st.file_uploader("Carregar CSV", type=["csv"])


# Verifica se o utilizador já carregou um ficheiro
if csv_file is not None:
    try:
        # Lê o ficheiro CSV carregado e converte-o num DataFrame (tabela)
        df = pd.read_csv(csv_file)

        # Cria um buffer em memória para guardar o ficheiro Excel
        output = BytesIO()

        # Cria o ficheiro Excel usando o motor openpyxl
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Escreve os dados do DataFrame para o Excel
            df.to_excel(writer, index=False)

        # Volta o cursor do buffer para o início
        output.seek(0)

        # Mostra uma mensagem de sucesso na interface
        st.success("Conversão concluída")

        # Cria um botão para o utilizador descarregar o ficheiro Excel
        st.download_button(
            label="Descarregar Excel",
            data=output,
            file_name="convertido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        # Caso ocorra algum erro durante a leitura ou conversão
        st.error("Erro ao converter o ficheiro CSV.")
