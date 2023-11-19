#import library python
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64

#Setup page 
st.set_page_config(page_title='Project Dashboard', page_icon='📈' ,layout='wide')
st.header('Project Dashboard')

st.markdown('##')

#Load Data
df = pd.read_csv('pages/Datasets/Data.csv')
#image = Image.open('pages/data/intro.gif')
#cost_2020_df = pd.read_csv('pages/Datasets/Cost_2020.csv')
#cost_2021_df = pd.read_csv('pages/Datasets/Cost_2021.csv')
cost_2022_df = pd.read_csv('pages/Datasets/Cost_2022.csv')
cost_2023_df = pd.read_csv('pages/Datasets/Cost_2023.csv')
cost_df = pd.concat([cost_2022_df, cost_2023_df])
cost_df['Amount'] =cost_df['Amount'].astype(float)

revenue_2022_df = pd.read_csv('pages/Datasets/Revenue_2022.csv')
revenue_2023_df = pd.read_csv('pages/Datasets/Revenue_2023.csv')
revenue_df = pd.concat([revenue_2022_df, revenue_2023_df])
revenue_df['Amount'] =revenue_df['Amount'].astype(float)


cash_in_df = pd.read_csv('pages/Datasets/cash_in.csv')
cash_out_df = pd.read_csv('pages/Datasets/cash_out.csv')


#site_list = df['المشروع'].unique()
cost_type =cost_df['نوع المصرف '].unique()



st.sidebar.image('pages/data/logo.png', caption='Online Analytics')
st.sidebar.header('Filter')
add_selectbox = st.sidebar.selectbox(
    "**What project do you want to choose?**",
    ['',*df['المشروع']]
)
#
site_selected = df[df['المشروع'] == add_selectbox]
cost_df_selected = cost_df[cost_df['اسم المشروع معدل'] == add_selectbox]
cost_df_selected['Amount'] = cost_df_selected['Amount'].astype(float)
revenue_df_selected = revenue_df[revenue_df['اسم المشروع معدل'] == add_selectbox]
revenue_df_selected['Amount'] = revenue_df_selected['Amount'].astype(float)


cash_in_df_selected = cash_in_df[cash_in_df['Cost Center'] == add_selectbox]
cash_in_df_selected['Amount'] = cash_in_df_selected['Amount'].astype(float)
cash_out_df_selected = cash_out_df[cash_out_df['Cost Center'] == add_selectbox]
cash_out_df_selected['Amount'] = cash_out_df_selected['Amount'].astype(float)


cash_combined = pd.concat([cash_in_df_selected, cash_out_df_selected], keys=['Cash In', 'Cash Out'])
cash_combined['Date'] = pd.to_datetime(cash_combined['Date'])
cash_combined_grouped = cash_combined.groupby(['Date', cash_combined.index.get_level_values(0)])['Amount'].sum().groupby(level=1).cumsum().reset_index()


profit_combined = pd.concat([cost_df_selected, revenue_df_selected], keys=['Expenses', 'Revenue'])
profit_combined['Date'] = pd.to_datetime(profit_combined['Date'])
profit_combined_grouped = profit_combined.groupby(['Date', profit_combined.index.get_level_values(0)])['Amount'].sum().groupby(level=1).cumsum().reset_index()

if add_selectbox =='':
    #st.image(image, caption = 'Wellcome to our Analysis ')
    st.subheader('Please select the project you want analyze ');
    #st.write(df)
else:
    #st.write(site_selected) #.transpose()
    st.write(':office: Project Name : ', add_selectbox)
    st.write(':house: Project Site : ', site_selected.iloc[0,4])
    st.write(':date: Start Date : ', site_selected.iloc[0,1])
    st.write(':date: End Date : ', site_selected.iloc[0,2])    
    
#st.markdown('##')
    st.markdown("<hr>", unsafe_allow_html=True)  
     
    fig = px.line(profit_combined_grouped, x='Date', y='Amount', color='level_1', title='Profit')
    st.plotly_chart(fig) 

    def profit():
        #with st.expander('Show the Data'):
         #   showdata = st.multiselect('Filter: ',site_selected.columns,default=[])
          #  st.write(site_selected[showdata])  
        #Compute Analysis
        total_expenses = (cost_df_selected['Amount']).sum().astype(float)
        total_revenue = (revenue_df_selected['Amount']).sum().astype(float)
        profit = float(total_revenue) - float(total_expenses)
        margin = float(profit) / float(total_revenue)
        margin_percentage = "{:.00%}".format(margin)
        
        expenses, revenue, total3, col4 = st.columns(4, gap='large') 
        with expenses:
            st.info('Total Expenses')
            st.metric(label='', value=f'{total_expenses:,.0f}')
        with revenue:
            st.info('Total Revenue')
            st.metric(label='', value=f'{total_revenue:,.0f}')
        with total3:
            st.info('Profit / Loss')
            st.metric(label='', value=f'{profit:,.0f}', delta=f'{margin_percentage}')
        with col4:
            ''
    profit()    
    st.markdown("<hr>", unsafe_allow_html=True)  

    fig = px.line(cash_combined_grouped, x='Date', y='Amount', color='level_1', title='Cash In Vs Cash Out')
    st.plotly_chart(fig)

    def cash_flow():
        total_cash_in = cash_in_df_selected['Amount'].sum()
        total_cash_out = (cash_out_df_selected['Amount']).sum()#.astype(float)
        net_cash_flow = float(total_cash_in) - float(total_cash_out)
        net_cash_flow_percentage = float(net_cash_flow) / float(total_cash_in)
        net_cash_flow_percentage_ = "{:.0%}".format(net_cash_flow_percentage)
        
        total1, total2, total3, plot = st.columns(4, gap='large') 
        with total1:
            st.info('Total Cash In')
            st.metric(label='', value=f'{total_cash_in:,.0f}')   
        with total2:
            st.info('Total Cash Out')
            #st.subheader(f'{total_cash_out:,.0f}')        
            st.metric(label='', value=f'{total_cash_out:,.0f}')
        with total3:
            st.info('Net Cash Flow')
            #st.subheader(f'{net_cash_flow:,.0f}')        
            st.metric(label='', value=f'{net_cash_flow:,.0f}', delta=f'{net_cash_flow_percentage_}') 
        with plot:
            ''
    cash_flow()


    st.markdown("<hr>", unsafe_allow_html=True)  

    #add_multiselect = st.sidebar.multiselect(
    #    "**What project do you want to choose?**",
    #    options = df['المشروع'].unique(),
    #    default = df['المشروع'].unique(),)

    #st.markdown('##')

    col1, col2 = st.columns(2)
    with col1:
        st.write('**Cost Analysis :**')
        site_selected_cost = cost_df[cost_df['اسم المشروع'] == add_selectbox]
        site_selected_cost_pt = site_selected_cost.groupby('نوع المصرف ')['Amount'].sum()
        
        st.write(site_selected_cost_pt)

        site_selected_cost_pt_csv = site_selected_cost_pt.to_csv(index=True, encoding='utf-8-sig')
        file_name1 = 'Cost Analysis_' + add_selectbox +'.csv'
        st.download_button('Download Data', data = site_selected_cost_pt_csv , file_name = file_name1)
        
        # Function to generate download link
    def get_download_link_csv(data, file_name):
        b64 = base64.b64encode(data.encode('utf-8-sig')).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download Data</a>'
        return href

    # Display the download link
    st.markdown(get_download_link_csv(site_selected_cost_pt_csv, file_name1), unsafe_allow_html=True)
        

        
        
        


    st.markdown("<hr>", unsafe_allow_html=True)  

    #cost_type_selectbox = st.selectbox(
        #"**What type of cost do you want to choose?**",
        #cost_type)
    #site_selected_cost = cost_df[cost_df['نوع المصرف '] == cost_type_selectbox]
    #site_selected_cost_type_pt = site_selected_cost.groupby([ cost_type_selectbox, 'اسم الحساب '])['Amount'].sum()
    #st.write(site_selected_cost_type_pt)

    st.markdown('##')




















