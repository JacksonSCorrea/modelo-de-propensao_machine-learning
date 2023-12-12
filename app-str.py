# Importação das bibliotecas

import pandas as pd
import numpy as np
import streamlit as st
import pickle
from sklearn.preprocessing import OneHotEncoder
import http.client
import json
import requests
import json


# warnings.filterwarnings("ignore")



# =====================================================================================
def main():

    # Configurações gerais
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_page_config()                                      # Tamanho padrão de página
    # st.set_page_config(layout="wide")                           # Tamanho 'large' de página

    # =============================================================================================
    # CABEÇALHO
    # =============================================================================================
    
    # Título
    st.title('OptiBank - módulo propensão')
    st.subheader("Saiba quais clientes da sua base de dados podem aderir a um serviço financeiro do seu banco!")

    # Linha separadora
    st.markdown("<hr>", unsafe_allow_html=True) 



    # =============================================================================================
    # AUTOR E VERSÃO
    # =============================================================================================

    col1, col2= st.columns([1,1])
    with col1:

        st.write("""Desenvolvido por Jackson Corrêa <br> v01 - dezembro/2023<br>
        <a href='https://www.linkedin.com/in/jackson-corrêa' target='_blank'>Acesse meu LinkedIn</a>  <br>
                <a href='https://www.github.com/JacksonSCorrea' target='_blank'>Acesse meu GitHub</a>""" , 
                unsafe_allow_html=True)

    # =============================================================================================
    # Amostras para download
    # =============================================================================================

    with col2:
        st.write("""Download das amostras para teste<br>
            <a href='https://github.com/JacksonSCorrea/modelo-de-propensao_machine-learning/blob/main/amostra1.csv' target='_blank'>Amostra 1 - 5 observações</a>   <br>
            <a href='https://github.com/JacksonSCorrea/modelo-de-propensao_machine-learning/blob/main/amostra2.csv' target='_blank'>Amostra 2 - 100 observações</a> <br>
            <a href='https://github.com/JacksonSCorrea/modelo-de-propensao_machine-learning/blob/main/amostra3.csv' target='_blank'>Amostra 3 - 300 observações</a>
                """ , 
                    unsafe_allow_html=True)

     # Linha separadora
    st.markdown("<hr>", unsafe_allow_html=True)


    # =============================================================================================
    # INFORMAÇÕES DO PROJETO
    # =============================================================================================

    col1, col2= st.columns([1,1])

    with col1:
        st.write('''**Modelo RandomForestClassifier:**
                 
    Recall: 0.67  
    AUC-ROC: 0.76  
    Gini: 0.52
    KS: 0.44 ''')

    with col2:
        st.write('**Arquitetura da aplicação:**')
        st.image('arquitetura_aplicacao.png', use_column_width='auto')
                      

    # Linha separadora
    st.markdown("<hr>", unsafe_allow_html=True) 

    
    # =============================================================================================
    # ENDPOINT DA API
    # =============================================================================================
    
    # URL para requisão da API
    # url = "https://o4z6kok940.execute-api.us-east-2.amazonaws.com/Prod/classify_digit/"
    url = "o4z6kok940.execute-api.us-east-2.amazonaws.com"
    path = "/Prod/classify_digit/"



    # =============================================================================================
    # EXTRAINDO OS ARTEFATOS
    # =============================================================================================

    # Lista de variáveis
    with open ('features.pkl', 'rb') as f:
        lista_variaveis = pickle.load(f)

    # Lista de variáveis selecionadas
    with open ('features_fs.pkl', 'rb') as f:
        lista_variaveis_fs = pickle.load(f)

    # Lista de valores para imputação de miss
    with open ('inputs_miss.pkl', 'rb') as f:
        inputs_miss = pickle.load(f)

    # Lista de variáveis do onehotencoder
    with open ('list_onehotencoder.pkl', 'rb') as f:
        lista_encoder = pickle.load(f)

    # Encoder
    with open ('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)



    # =============================================================================================
    # METODO DE IMPUT POR CLIENTE
    # =============================================================================================

    # Variáveis para dataprep
    #  'poutcome',        ok
    #  'loan',            ok
    #  'marital',         ok
    #  'age',             ok
    #  'housing',         ok
    #  'job',             ok 
    #  'pdays',           ok
    #  'euribor3m',       ok
    #  'campaign',        ok
    #  'education'        ok

    # Variáveis de treinamento do modelo
    #  'age',                                ok
    #  'campaign',                           ok
    #  'pdays',                              ok
    #  'euribor3m',                          ok
    #  'job_technician_dummy',               ok
    #  'marital_married_dummy',              ok
    #  'marital_single_dummy',               ok
    #  'education_high.school_dummy',        ok
    #  'education_university.degree_dummy',  ok
    #  'housing_yes_dummy',                  ok
    #  'loan_yes_dummy',                     ok


    st.subheader('Consulta individual')

    # Definição das colunas do layout
    col1, col2= st.columns([1,1])


    # Coluna 1
    with col1:

        age = st.number_input('Age' , value=45)

        marital = st.selectbox('Marital Status', ['married', 'single', 'divorced', 'unknown'])

        job = st.selectbox('Job', ['housemaid', 'services', 'admin.', 'blue-collar', 'retired',
                                   'management', 'unemployed', 'technician', 'self-employed',
                                   'unknown', 'entrepreneur', 'student'])
        
        education = st.selectbox('Education', ['basic.4y', 'high.school', 'basic.6y', 'basic.9y',
                                               'professional.course', 'unknown', 'university.degree',
                                               'illiterate'])

        housing = st.selectbox('Housing', ['no', 'yes', 'unknown'])


    # Coluna 2
    with col2:

        loan = st.selectbox('Loan', ['no', 'yes', 'unknown'])
        campaign = st.number_input('Campaign' , step=1)
        pdays = st.number_input('Previous Days' , step=1)
        euribor = st.number_input('euribor3M' , value=5.59)

    # Botão de consulta individual
    consulta1=st.button('Consultar')

    if consulta1 == True:

        # criando dicionário de valores
        entradas = {'housing': [housing] ,
                'age': [age],
                'euribor3m': [euribor],
                'loan': [loan],
                'job': [job],
                'marital': [marital],
                'pdays': [pdays],
                'education': [education],
                'poutcome': ['success'],
                'campaign': [campaign]}


        # Observação: o encoder exportado convertia também a feature 'poutcome'
        # Porém essa feature não é utilizada no treinamento do modelo
        # Mas para não comprometer o funcionamento do encoder, essa feature
        # será mantida na lista de conversão do encoder como um valor fixo
        # oputcome = 'success'


        # Montando uma tabela analítica
        abt_new=pd.DataFrame(entradas)
    
        # Aplicando o OneHotEncoder (Lembrar de aplicar o sufixo '_dummy')
        encoded_data = encoder.transform(abt_new[lista_encoder])
        encoded_cols = encoder.get_feature_names_out(lista_encoder)
        encoded_df = pd.DataFrame(encoded_data, columns=encoded_cols+'_dummy', index=abt_new.index)
        abt_new = pd.concat([abt_new.drop(lista_encoder, axis=1), encoded_df], axis=1)

        # Aplicando o filtro da Feature Selection
        abt_new = abt_new[lista_variaveis_fs]

        # Montando os parâmetros (string com os valores da primeira linha do dataframe)
        parametros = ','.join(map(str, abt_new.iloc[0]))

        # Ajustando a formatação do body (tem que ser uma string com aspas duplas) 
        body = [{"params" : f"{parametros}"}]

        # Convertendo a lista de dicionários para um JSON válido
        body = json.dumps(body)

        # Inicializando a conexão
        conn = http.client.HTTPSConnection(url)

        # Definindo o cabeçalho da requisição
        headers = {"Content-type": "application/json"}


        try:
            # Enviando a requisição
            conn.request("POST", path, body=body, headers=headers)

            # Obtendo a resposta
            resposta = conn.getresponse()


            if resposta.status == 200:
                st.info("Requisição bem-sucedida!")
                # Lendo e imprimindo a resposta
                data = resposta.read().decode('utf-8')
                results = json.loads(data)
                classe = results['predicoes'][0]        # Extraindo a classe
                score_0 = results['prob_classe_0'][0]   # Propabilidade de nao adesão
                score_1 = results['prob_classe_1'][0]   # Probabilidadede adesão

                # Exibindo os resultados
                if classe == 0: # Se for provável a não adesão
                    st.error(f"""
                            O cliente não está propenso à aderir ao produto!

                            Probabilidade de não adesão: {100* round(float(score_0) , 2)}
                            """)

                else:   # Se for provável a adesão
                    st.success(f"""
                            O cliente está propenso à aderir ao produto!

                            Probabilidade de adesão: {100* round(float(score_1) , 2)}
                            """)

                # print("Status:", resposta.status)
                # print("Response:", data.decode('utf-8'))

            else:
                st.warning("Erro na requisição. Código de status:", resposta.status)


        finally:
            # Fechando a conexão
            conn.close()



    # Linha separadora
    st.markdown("<hr>", unsafe_allow_html=True)


    # =============================================================================================
    # METODO DE IMPORTAÇÃO DOS DADOS
    # =============================================================================================


    st.subheader('Escoragem de tabela')
    # st.subheader('Scoragem de base de dados')
    upload_file = st.file_uploader('Carregar do computador', type=['csv']) 

    if upload_file is not None:
        # Convertendo em dataframe
        df = pd.read_csv(upload_file)
        # Dropando a target
        df.drop('y' , axis=1 , inplace=True)

        # Criandoum backup
        df_bkp = df.copy()

        # Exibindo
        st.text('Tabela original:')
        st.dataframe(df)

        # backup da coluna de id
        bkp_id = df['ID'].values

    # Botaão de escoragem da tabela
    consulta2 = st.button('Escorar tabela')


    if consulta2 == True:

        with st.spinner(text="Por favor, aguarde..."):

            # Ajustando os dados da tabela
            df=df[lista_variaveis]

            # Imputando miss
            df.fillna(value=inputs_miss)


            # Aplicando OneHotEncoder
            encoded_data = encoder.transform(df[lista_encoder])
            encoded_cols = encoder.get_feature_names_out(lista_encoder)
            encoded_df = pd.DataFrame(encoded_data, columns=encoded_cols+'_dummy', index=df.index)
            df = pd.concat([df.drop(lista_encoder, axis=1), encoded_df], axis=1)

            # Aplicando o filtro da Feature Selection
            df = df[lista_variaveis_fs]

            # Montando os parâmetros (string com os valores da primeira linha do dataframe)
            # Quantidade de linhas da tabela
            qtd = df.shape[0]

            # Lista vazia do body
            body=[]

            # Iterando
            for i in range (0, qtd):
                parametros = ','.join(map(str, df.iloc[i,:]))
                body.append({"params" : f"{parametros}"})


            # Convertendo a lista de dicionários para um JSON válido
            body = json.dumps(body)

            # Inicializando a conexão
            conn = http.client.HTTPSConnection(url)

            # Definindo o cabeçalho da requisição
            headers = {"Content-type": "application/json"}


            try:
                # Enviando a requisição
                conn.request("POST", path, body=body, headers=headers)

                # Obtendo a resposta
                resposta = conn.getresponse()

                if resposta.status == 200:
                    st.info("Requisição bem-sucedida!")
                    # Lendo e imprimindo a resposta
                    data = resposta.read().decode('utf-8')
                    results = json.loads(data)
                    classe = results['predicoes']        # Extraindo a classe
                    score_0 = results['prob_classe_0']   # Propabilidade de nao adesão
                    score_1 = results['prob_classe_1']   # Probabilidadede adesão

                else:
                    st.warning("Erro na requisição. Código de status:", resposta.status)

            finally:
                # Fechando a conexão
                conn.close()

            # Montando o dataframe final
            df2=df.copy()
            df2['ID'] = bkp_id
            df2['classe'] = classe
            df2['vai aderir?'] = df2['classe'].apply(lambda x: 'Sim' if int(x)==1 else 'Não')
            df2.drop('classe' , axis=1 , inplace=True)
            df2['prob. adesão'] = score_1
            df2 = df2[['ID','vai aderir?' , 'prob. adesão']]


            # Left join nas tabelas
            df3 = pd.merge(df2 , df_bkp , on='ID' , how='left')

            # Exibindo
            st.text('Tabela escorada:')
            st.dataframe(df3)

            # Linha separadora
            st.markdown("<hr>", unsafe_allow_html=True)


            # =============================================================================================
            # API chatGPT (dentro do comando do botão de escoragem de tabela)
            # =============================================================================================


            # API_KEY = st.text_input("Digite sua API Key da OpenAI", type='password')

            API_KEY = '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'

            headers = {"Authorization" : f"Bearer {API_KEY}" , "Content-Type": "application/json"}

            link="https://api.openai.com/v1/chat/completions"

            id_modelo = "gpt-3.5-turbo"

            body_mensagem = {
                "model":id_modelo,
                "messages":[{"role":"user" , "content" : f"Extraia insight da tabela. Trata-se de uma base de dados com informações de clientes propensos ou não a aderir a um produto bancário: {df3}. Além disso, dê dicas de como vender mais estes produtos para estes clientes. Mostre asprincipais distribuições das variáveis dentee os clientes propensos e não propensos. Prar os propensos, mostre as estratégias para vender o produto. Seu texto deve ter no máximo 80 caracteres por linha."}]                 
                            }

            body_mensagem = json.dumps(body_mensagem)

            # O parâmetro verify=False desativa a verificação de certificados SSl no VSCode, mas pode ser inseguro
            requisicao = requests.post(link, headers=headers , data=body_mensagem , verify=False)

            # print(requisicao.text)

            resposta = requisicao.json()

            mensagem = resposta["choices"][0]["message"]["content"]

            # Botão
            st.write(mensagem)




if __name__ == "__main__":
    main()