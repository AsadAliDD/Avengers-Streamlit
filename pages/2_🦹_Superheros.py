import streamlit as st
import glob
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Superheros",
                page_icon="🦹 vs 👾", layout="wide", 
                initial_sidebar_state="expanded")
st.sidebar.title("🦹 Avengers vs Invaders 👾")
st.title("🦹 Avengers Assemble")



@st.cache_data
def get_superheroes():
    superheroes_path='./solutions/task2/*.txt'
    superhero_files=glob.glob(superheroes_path)
    superhero_lov=[]
    for file_path in superhero_files:
        superhero_lov.append(file_path.split('/')[-1].split('.txt')[0])
    return superhero_lov



@st.cache_data
def read_superhero_data(superhero):
    if(superhero is None):
        return 
    file_path=f'./solutions/task2/{superhero}.txt'
    df=pd.read_csv(file_path,delimiter='\t')
    return df

@st.cache_data
def gen_mock_data(df):
    name=df.columns[0]
    df=df.melt(id_vars=[name]).rename(columns={'variable':'enemy_type','value':'role',name:'headquarters'}).dropna()
    df['hero']=name
    df['enemies_defeated']=np.random.randint(0,200, size=len(df))
    return df


def gen_plot(df,hq,invader):

    title='Enemies Defeated'
    if(hq is not None or invader is not None):
        df=df[(df['headquarters']==hq) & (df['enemy_type']==invader)]
        title=f'Enemies Defeated at {hq}'
    fig = px.bar(df,x='enemy_type',y='enemies_defeated',
           color='headquarters',barmode='group',facet_col='role')
    fig.update_layout(title=title)
    st.plotly_chart(fig)

def main():
    superhero_lov = get_superheroes()
    superhero=st.selectbox("Select Avenger",superhero_lov,index=None)
    if superhero:

        st.text(f"Selected Superhero: {superhero}")
        superhero_data=read_superhero_data(superhero)
        st.table(superhero_data)
        superhero_data_mock=gen_mock_data(superhero_data)

        hq=st.sidebar.selectbox("Select Headquarters",superhero_data_mock['headquarters'].unique(),index=None)
        invader=st.sidebar.selectbox("Select Enemy",superhero_data_mock['enemy_type'].unique(),index=None)
        gen_plot(superhero_data_mock,hq,invader)
main()