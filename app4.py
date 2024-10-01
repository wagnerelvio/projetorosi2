import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

#file_path = 'D:\OneDrive\ead-ia\programação\houses_to_rent_v2.csv'
#df = pd.read_csv(file_path)

# URL dos dados hospedados no GitHub (substitua com o seu link)
DATA_URL = 'https://raw.githubusercontent.com/wagnerelvio/projetorosi2/refs/heads/main/houses_to_rent_v2.csv'

# Função para carregar os dados com cache
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

# Carregar os dados
data = load_data()




# Configurações iniciais do dashboard
st.title('Dashboard de Análise de Aluguéis de Imóveis')
st.markdown('Este dashboard permite analisar os dados de aluguel de imóveis por cidade, considerando características como número de quartos, banheiros, aceitação de animais e se o imóvel é mobiliado.')

# Seleciona  as colunas numéricas para calcular a correlação
numerical_cols = ['area', 'rooms', 'bathroom', 'parking spaces', 'hoa (R$)', 'rent amount (R$)']
data_numerical = data[numerical_cols]

# Matriz de correlação
correlation_matrix = data_numerical.corr()

# Criação das abas
tab1, tab2, tab3, tab4 = st.tabs(["Dados Gerais", "Dados Filtrados (Sem Outliers)", "Gráfico de Correlação", 'Filtros'])

# Aba 1 - Dados Gerais
with tab1:
    st.header("Distribuição Geral do Preço Total por Cidade")
    st.markdown('Apresentação geral de preços dos imóveis.')
    fig_box_general = px.box(data, x='city', y='total (R$)', title='Distribuição do Preço Total por Cidade')
    st.plotly_chart(fig_box_general)
   
    st.markdown('Distribuição geral de quartos por cidades')
    fig_box_rooms = px.box(data, y='rooms', color='city', title='Distribuição de Quartos por Cidade')
    st.plotly_chart(fig_box_rooms)

    st.markdown('Distribuição geral de vagas de estacionamento por cidades')
    fig_box_parking = px.box(data, y='parking spaces', color='city', title='Distribuição de Vagas de Estacionamento por Cidade')
    st.plotly_chart(fig_box_parking)

    st.markdown('Aceitação de animais')
    animal_counts = data['animal'].value_counts().reset_index()
    animal_counts.columns = ['animal', 'count']
    fig_pie_animal = px.pie(animal_counts, names='animal', values='count', title='Distribuição de Aceitação de Animais')
    st.plotly_chart(fig_pie_animal)

# Aba 2 - Dados Filtrados (Sem Outliers)
df_filtered = data[data['total (R$)'] <= 10000]  # Filtrando os outliers
with tab2:
    st.header("Distribuição do Preço Total por Cidade (Sem Outliers)")
    fig_box_filtered2 = px.box(df_filtered, x='city', y='total (R$)', title='Distribuição do Preço Total por Cidade (Sem Outliers)')
    st.plotly_chart(fig_box_filtered2)


# Aba 3 - Gráfico de Correlação
with tab3:
    st.header("Gráfico de Correlação")
    
    # Plotar o heatmap de correlação usando Seaborn
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


# Aba 4 - Filtros
with tab4:
    st.header("Filtros")

    # Filtros interativos
    city = st.multiselect('Selecione a cidade', data['city'].unique())
    rooms = st.slider('Número de Quartos', int(data['rooms'].min()), int(data['rooms'].max()), (int(data['rooms'].min()), int(data['rooms'].max())))
    bathroom = st.slider('Número de Banheiros', int(data['bathroom'].min()), int(data['bathroom'].max()), (int(data['bathroom'].min()), int(data['bathroom'].max())))
    parking_spaces = st.slider('Vagas de estacionamento', int(data['parking spaces'].min()), int(data['parking spaces'].max()), (int(data['parking spaces'].min()), int(data['bathroom'].max())))
    animal = st.selectbox('Aceita Animais?', ['acept', 'not acept'], format_func=lambda x: 'Aceita' if x == 'acept' else 'Não Aceita')
    furniture = st.selectbox('Mobiliado?', ['furnished', 'not furnished'], format_func=lambda x: 'Mobiliado' if x == 'furnished' else 'Não Mobiliado')

    # Filtrar os dados com base nas seleções
    filtered_df = data[
        (data['city'].isin(city)) &
        (data['rooms'] >= rooms[0]) &
        (data['rooms'] <= rooms[1]) &
        (data['bathroom'] >= bathroom[0]) &
        (data['bathroom'] <= bathroom[1]) &
        (data['animal'] == animal) &
        (data['furniture'] == furniture)
    ]

    # Estatísticas
    min_price = filtered_df['total (R$)'].min() if not filtered_df.empty else 0
    max_price = filtered_df['total (R$)'].max() if not filtered_df.empty else 0

    # Exibir estatísticas
    st.subheader('Estatísticas Filtradas')
    st.write(f'Preço mínimo: R${min_price}')
    st.write(f'Preço máximo: R${max_price}')

    # Gráficos interativos
    if not filtered_df.empty:
        # Gráfico de barras do preço total por cidade
        fig1 = px.box(filtered_df, x='city', y='total (R$)', color='city', title='Preço Total por Cidade')
        st.plotly_chart(fig1)

        # Gráfico de dispersão entre área e preço
        fig2 = px.scatter(filtered_df, x='area', y='total (R$)', color='city', size='rooms', hover_data=['bathroom', 'parking spaces'])
        st.plotly_chart(fig2)

         # Gráfico de dispersão entre área e preço
        fig3 = px.scatter(filtered_df, x='parking spaces', y='total (R$)', color='city', size='rooms', hover_data=['bathroom', 'parking spaces'])
        st.plotly_chart(fig3)
    else:
        st.write("Nenhum dado disponível para os filtros selecionados.")
