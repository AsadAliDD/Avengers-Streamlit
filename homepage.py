import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="Avengers vs Invaders",
                page_icon="🦹 vs 👾", layout="wide", 
                initial_sidebar_state="expanded")
st.sidebar.title("🦹 Avengers vs Invaders 👾")
st.title("🦹 Avengers vs Invaders 👾")
GRAPHS = st.sidebar.toggle("Show Graphs", True)




@st.cache_data
def read_data():
    country=pd.read_table('./solutions/task1.txt')
    country_hq_iso=pd.read_csv('./solutions/country_hq_iso.csv')
    country_code=list(country['Country_Code'].unique())
    role=list(country['Role'].unique())
    invaders=list(country['Invader_Species'].unique())
    country['Name']=country['Email'].str.split('@').str[0]
    return country,country_code,role,invaders,country_hq_iso


def filter_data(country,country_code,role,invaders):
    if(country_code is None or role is None or invaders is None):
        return country
    print (f"country_code: {country_code} role: {role} invaders: {invaders}")
    data=country[(country['Country_Code']==country_code) 
                          & (country['Role']==role) 
                          & (country['Invader_Species']==invaders)]
    try:
        st.sidebar.text(f'Email: {data["Email"].iloc[0]}')
    except Exception as e:
        st.text("No Hero Found")
        print (f"Exception: {e}")
    return data

@st.cache_data
def gen_maps_data(country_hq_iso):
    df=pd.DataFrame()
    for enemy_type in ['Aliens','Predators','D&D Monsters']:
        temp=country_hq_iso.groupby([enemy_type,enemy_type+'_alpha_3'])['Country Name'].nunique().reset_index()
        temp=temp.rename(columns={enemy_type:'HQ',enemy_type+'_alpha_3':'hq_alpha_3','Country Name':'count'})
        temp['Enemy Type']=enemy_type
        df=pd.concat([df,temp])
    return df


def gen_maps(df):

    # Full World Map
    fig = px.scatter_geo(df, locations="alpha_3",hover_name='Country Name',color='Country Name',projection="orthographic",template='plotly_dark')
    fig.update_layout(title='Countries under Avengers Protection')
    st.plotly_chart(fig)



    
    df=gen_maps_data(df)
    fig = px.scatter_geo(df, locations="hq_alpha_3",color='HQ',hover_name='HQ',template='plotly_dark', projection="natural earth1",size='count',facet_col='Enemy Type')
    fig.update_layout(title='How many countries are under the protection of each HQ?')
    fig.update_geos(showcountries=True, subunitcolor="Blue")
    st.plotly_chart(fig)


def gen_graphs(country,country_hq_iso):
   
    gen_maps(country_hq_iso)
    temp=country.groupby('Name')['Country_Code'].nunique().reset_index()
    fig = px.treemap(temp,path=[px.Constant('Avengers'),'Name'],values='Country_Code')
    fig.update_layout(title='How Many Countries are under the Protetction of each Avenger?')
    st.plotly_chart(fig)

    temp=country.groupby(['Name','Role'])['Invader_Species'].nunique().reset_index()
    fig = px.sunburst(temp,path=['Role','Name'],values='Invader_Species')
    fig.update_layout(title='How Many Enemies are an Avenger tackling under Specific Role?')
    st.plotly_chart(fig)


    temp=country.groupby(['Role','Invader_Species'])['Name'].nunique().reset_index()
    fig = px.line_polar(temp, r='Name', theta='Role', color='Invader_Species', line_close=True, 
                    title='How many heroes are in specific roles for each invader Species?',template='plotly_dark')
    st.plotly_chart(fig)





    


country,lov_country_code,lov_role,lov_invaders,country_hq_iso = read_data()
if(GRAPHS): 
    gen_graphs(country,country_hq_iso)


st.sidebar.title("Find Your Hero")
country_code = st.sidebar.selectbox("Select Country Code",lov_country_code,index=None)
role = st.sidebar.selectbox("Select Country Code",lov_role,index=None)
invaders = st.sidebar.selectbox("Select Invader",lov_invaders,index=None)
data=filter_data(country,country_code,role,invaders)
st.dataframe(data)