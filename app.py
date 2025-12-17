# Interface web
import streamlit as st

# Leitura e manipulação de CSV
import pandas as pd

# Para criar o ficheiro Excel em memória
from io import BytesIO


# Configuração básica da página
st.set_page_config(page_title="CSV → Excel", page_icon="📄")

st.title("CSV → Excel")
st.write("Carrega um ficheiro CSV e faz download do Excel convertido.")


# Upload do ficheiro CSV
csv_file = st.file_uploader("Carregar CSV", type=["csv"])


if csv_file is not None:
    try:
        # Lê o CSV assumindo:
        # - separador por vírgulas
        # - primeira linha é lixo (título)
        # - segunda linha contém os cabeçalhos
        # - ignora linhas vazias
        df = pd.read_csv(
            csv_file,
            sep=",",
            skiprows=1,          # ignora "01-SAPATAS,,,"
            encoding="latin-1",  # comum em ficheiros PT
            skip_blank_lines=True
        )

        # Remove linhas completamente vazias (segurança extra)
        df = df.dropna(how="all")

        # Cria o ficheiro Excel em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        output.seek(0)

        # Mensagem de sucesso
        st.success("Conversão concluída com sucesso")

        # Botão para descarregar o Excel
        st.download_button(
            label="Descarregar Excel",
            data=output,
            file_name="convertido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # Pré-visualização dos dados
        st.subheader("Pré-visualização")
        st.dataframe(df.head(20))

    except Exception as e:
        # Erro genérico (mostrado ao utilizador)
        st.error("Erro ao converter o ficheiro CSV.")
        st.exception(e)
