#import library python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from streamlit_option_menu import option_menu
from PIL import Image
import base64


st.set_page_config(page_title='Dashboard', page_icon='💹', layout='wide')
st.subheader('Elsaeed Company - **P&L** :money_with_wings:')
st.markdown('##')

#Load Data
cost_2022_df = pd.read_csv('pages/Datasets/Cost_2022.csv')
cost_2023_df = pd.read_csv('pages/Datasets/Cost_2023.csv')
cost_df = pd.concat([cost_2022_df, cost_2023_df])
cost_df['Amount'] =cost_df['Amount'].astype(float)
cost_df['Date'] = pd.to_datetime(cost_df['Date'])
mixing_cost_df = cost_df[cost_df['Type'] == 'محطات خلط الخرسانه']
real_estat_cost_df = cost_df[cost_df['Type'] == 'الاستثمار العقارى']
contracting_cost_df = cost_df[cost_df['Type'] == 'المقاولات']
operation_cost_df = pd.concat([mixing_cost_df, real_estat_cost_df, contracting_cost_df])
operation_cost_without_interest_df = operation_cost_df[operation_cost_df['نوع المصرف '] != 'بنوك']

general_expenses = cost_df[cost_df['Type'] == 'الإدارة']
general_expenses_without_interest_df =general_expenses[general_expenses['نوع المصرف '] != 'بنوك']


revenue_2022_df = pd.read_csv('pages/Datasets/Revenue_2022.csv')
revenue_2023_df = pd.read_csv('pages/Datasets/Revenue_2023.csv')
revenue_df = pd.concat([revenue_2022_df, revenue_2023_df])
revenue_df['Amount'] =revenue_df['Amount'].astype(float)
revenue_df['Date'] = pd.to_datetime(revenue_df['Date'])
mixing_revenue_df = revenue_df[revenue_df['Type'] == 'محطات خلط الخرسانه']
real_estat_revenue_df = revenue_df[revenue_df['Type'] == 'الاستثمار العقارى']
contracting_revenue_df = revenue_df[revenue_df['Type'] == 'المقاولات']
operation_revenue_df = pd.concat([mixing_revenue_df, real_estat_revenue_df, contracting_revenue_df])


cash_in_df = pd.read_csv('pages/Datasets/Cash_in.csv')
cash_out_df = pd.read_csv('pages/Datasets/Cash_out.csv')

dates = pd.to_datetime(cost_df['Date'])
years = sorted(list(set(dates.dt.year)))
quarters  = sorted(list(set(dates.dt.quarter)))
quarter_names = ['Q1', 'Q2', 'Q3', 'Q4', ""]
quarters = [quarter_names[qtr - 1] for qtr in quarters]


years_sidebar = st.sidebar.selectbox(
    "**What is the year you want to analyze?**",
    ['',*years])
quarters_sidebar = st.sidebar.selectbox(
    "**What is the period you want to analyze?**",
    [*quarters])
    
# Determine the index of the selected quarter
selected_quarter_index = quarters.index(quarters_sidebar)
    

filtered_cost_df = operation_cost_without_interest_df[
    (operation_cost_without_interest_df['Date'].dt.year == years_sidebar) &
    (operation_cost_without_interest_df['Date'].dt.quarter <= (selected_quarter_index + 1))]

filtered_admin_expenses_df = general_expenses_without_interest_df[
    (general_expenses_without_interest_df['Date'].dt.year == years_sidebar) &
    (general_expenses_without_interest_df['Date'].dt.quarter <= (selected_quarter_index + 1))]

filtered_revenue_df = operation_revenue_df[
    (operation_revenue_df['Date'].dt.year == years_sidebar) &
    (operation_revenue_df['Date'].dt.quarter <= (selected_quarter_index + 1))]
    
filtered_revenue_df_previous_year =operation_revenue_df[
    (operation_revenue_df['Date'].dt.year == years_sidebar - 1) &
    (operation_revenue_df['Date'].dt.quarter <= (selected_quarter_index + 1))]     

type_operation_cost = filtered_cost_df.groupby('Type')['Amount'].sum()
type_operation_revenue = filtered_revenue_df.groupby('Type')['Amount'].sum()
profit_operation_grouped = pd.DataFrame(type_operation_revenue).merge(type_operation_cost, on='Type',
    how='left',suffixes=('_revenue', '_cost'))
profit_operation_grouped['Amount_gross'] = profit_operation_grouped['Amount_revenue'] - profit_operation_grouped['Amount_cost']
profit_operation_grouped.rename(columns = {'Amount_gross': 'Gross Profit', 'Amount_revenue' : 'Revenue', 'Amount_cost':'Cost'}, inplace=True)
profit_operation_grouped = profit_operation_grouped.sort_values(by= 'Gross Profit', ascending=False)

translation_dict = {
    'المقاولات': 'Contracting',
    'الاستثمار العقارى': 'Housing and development projects',
    'محطات خلط الخرسانه': 'Concrete Station',
}


profit_operation_grouped_transpose = profit_operation_grouped.transpose()


#st.dataframe(type_operation_cost)
st.markdown('#')
#st.dataframe(type_operation_revenue)
#st.dataframe(profit_operation)
#st.dataframe(profit_operation_grouped)
#st.write(profit_operation_grouped)
#st.dataframe(profit_operation_grouped_transpose)

list_operation_type = list(profit_operation_grouped.index)
type_df =pd.DataFrame(list_operation_type)
type_df.rename(columns ={0: 'type'}, inplace=True)
type_df['type_en'] = type_df['type'].map(translation_dict)
list_operation_type_en = list(type_df['type_en'])
#st.write(list_operation_type_en)
#st.write(list_operation_type)

#st.write(type_df)


fig = sp.make_subplots(rows=1, cols=3, subplot_titles=list_operation_type_en)
#for i, col in enumerate(profit_operation_grouped[profit_operation_grouped['Type']]):
for i, col in enumerate(list_operation_type):
    fig.add_trace(go.Bar(x=profit_operation_grouped_transpose.index, y=profit_operation_grouped_transpose[col], name=col), row=1, col=i + 1)   
    
fig.update_layout(height=450, width=1000, title_text=f'Gross Profit generates from primary activities ( ' + str(years_sidebar) + '-' + str(quarters_sidebar) + ' )' )

#fig.update_xaxes(title_text=list_operation_type_en[0], row=1, col=1)
#fig.update_xaxes(title_text=list_operation_type_en[1], row=1, col=2)
#fig.update_xaxes(title_text=list_operation_type_en[2], row=1, col=3)

st.plotly_chart(fig)

profit_combined = pd.concat([filtered_cost_df, filtered_revenue_df], keys=['Expenses', 'Revenue'])
#profit_combined['Date'] = pd.to_datetime(profit_combined['Date'])
profit_combined_grouped = profit_combined.groupby(['Type', profit_combined.index.get_level_values(0)])['Amount'].sum().groupby(level=1).cumsum().reset_index()
#st.dataframe(profit_combined_grouped)

debit_interest_df = filtered_cost_df[filtered_cost_df['نوع المصرف '] == 'بنوك']
debit_interest = debit_interest_df['Amount'].sum().astype(float)

admin_expenses = (filtered_admin_expenses_df['Amount']).sum().astype(float)
total_expenses = (filtered_cost_df['Amount']).sum().astype(float)
total_revenue = (filtered_revenue_df['Amount']).sum().astype(float)
total_revenue_previous_year = (filtered_revenue_df_previous_year['Amount']).sum().astype(float)
gross_profit = float(total_revenue) - float(total_expenses)
revenue_growth = ((total_revenue - total_revenue_previous_year )/total_revenue_previous_year)
revenue_growth_percentage =  "{:.00%}".format(revenue_growth)
margin = float(gross_profit) / float(total_revenue)
margin_percentage = "{:.00%}".format(margin)



def profit():
    revenue, expenses, total3, col4 = st.columns(4, gap='large')
    with revenue:
        st.info('Total Revenue')
        st.metric(label='', value=f'{total_revenue:,.0f}') 
    with expenses:
        st.info('Total Expenses')
        st.metric(label='', value=f'{total_expenses:,.0f}')
    with total3:
        st.info('Gross Profit')
        st.metric(label='', value=f'{gross_profit:,.0f}', delta=f'{margin_percentage}')
    with col4:
        st.info('Revenue Growth')
        st.metric(label='', value=revenue_growth_percentage)
profit() 

st.write(debit_interest)













def p_and_l_chart():
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "total", "relative", "relative", "total"],
        x = ["Operations Revenue", "Operations Cost", "Gross Profit", "Administrative Expenses", "Other expenses", "Profit before tax"],
        textposition = "outside",
        text = [total_revenue, -total_expenses, gross_profit, admin_expenses , "", "Total"],
        y = [total_revenue, (total_expenses * -1), gross_profit, (admin_expenses * -1), 0, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        texttemplate='%{text:.3s}'
    ))

    fig.update_layout(
            title = "Profit and loss statement " + str(years_sidebar) + " " + str(quarters_sidebar) ,
            showlegend = True
    )


    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)
p_and_l_chart()   
