import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

#DataFrame Creation
myDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Skramar$13071999",
    database = "phonepe"
)
myCursor = myDB.cursor()
###############################################################################
#aggregated_insurance
myCursor.execute("select * from aggregated_insurance")
aggregated_insurance_table = myCursor.fetchall()
aggregated_insurance = pd.DataFrame(aggregated_insurance_table , columns = ['States' , 'Years' , 'Quarter' , 'Transaction_name' , 'Transaction_count' , 'Transaction_amount'])

#aggregated_transaction
myCursor.execute("select * from aggregated_transaction")
aggregated_transaction_table = myCursor.fetchall()
aggregated_transaction = pd.DataFrame(aggregated_transaction_table , columns = ['States' , 'Years' , 'Quarter' , 'Transaction_name' , 'Transaction_count' , 'Transaction_amount'])

#aggregated_user
myCursor.execute("select * from aggregated_user")
aggregated_user_table = myCursor.fetchall()
aggregated_user = pd.DataFrame(aggregated_user_table , columns = ['States' , 'Years' , 'Quarter' , 'Brand' , 'Transaction_count' , 'Percentage'])

####################################################################################
#map_insurance_country
myCursor.execute("select * from map_insurance_country")
map_insurance_country_table = myCursor.fetchall()
map_insurance_country = pd.DataFrame(map_insurance_country_table , columns = ['Latitude' , 'Longitude' , 'Metric' , 'District'])

#map_insurance_hover
myCursor.execute("select * from map_insurance_hover")
map_insurance_hover_table = myCursor.fetchall()
map_insurance_hover = pd.DataFrame(map_insurance_hover_table , columns = ['States' , 'Years' , 'Quarter' , 'District' , 'Transaction_count' , 'Transaction_amount'])

#map_transaction
myCursor.execute("select * from map_transaction")
map_transaction_table = myCursor.fetchall()
map_transaction = pd.DataFrame(map_transaction_table , columns = ['States' , 'Years' , 'Quarter' , 'District' , 'Transaction_count' , 'Transaction_amount'])

#map_user
myCursor.execute("select * from map_user")
map_user_table = myCursor.fetchall()
map_user = pd.DataFrame(map_user_table , columns = ['States' , 'Years' , 'Quarter' , 'District' , 'RegisteredUsers' , 'AppOpens'])

####################################################################################
#top_insurance
myCursor.execute("select * from top_insurance")
top_insurance_table = myCursor.fetchall()
top_insurance = pd.DataFrame(top_insurance_table , columns = ['States' , 'Years' , 'Quarter' , 'Pincodes' , 'Transaction_count' , 'Transaction_amount'])

#top_transaction
myCursor.execute("select * from top_transaction")
top_transaction_table = myCursor.fetchall()
top_transaction = pd.DataFrame(top_transaction_table , columns = ['States' , 'Years' , 'Quarter' , 'Pincodes' , 'Transaction_count' , 'Transaction_amount'])

#top_user
myCursor.execute("select * from top_user")
top_user_table = myCursor.fetchall()
top_user = pd.DataFrame(top_user_table , columns = ['States' , 'Years' , 'Quarter' , 'Pincodes' , 'RegisteredUsers'])


def Transaction_amount_count_Y(df, year):
    AI_tacy = df[df["Years"] == year] 
    AI_tacy.reset_index(drop=True, inplace=True)
    AI_tacyg = AI_tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    AI_tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        amount_fig = px.bar(AI_tacyg, x="States", y="Transaction_amount", title=f"{AI_tacy['Years'].unique()} YEAR TRANSACTION_AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset_r, height=500, width=550)
        st.plotly_chart(amount_fig)
    with col2:
        count_fig = px.bar(AI_tacyg, x="States", y="Transaction_count", title=f"{AI_tacy['Years'].unique()} YEAR TRANSACTION_COUNT", color_discrete_sequence=px.colors.sequential.amp_r, height=450, width=500)
        st.plotly_chart(count_fig)
    
    col1, col2 = st.columns(2)
    # Load geojson data
    with open("states_india.geojson", "r") as f:
        data = json.load(f)

    # Ensure that state names in geojson data match those in the DataFrame
    AI_tacyg["States"] = AI_tacyg["States"].str.title()
    with col1:
        Indian_map1 = px.choropleth(AI_tacyg, 
                                    geojson=data, 
                                    locations='States', 
                                    featureidkey="properties.st_nm", 
                                    color="Transaction_amount", 
                                    color_continuous_scale="turbo", 
                                    range_color=(AI_tacyg["Transaction_amount"].min(), AI_tacyg["Transaction_amount"].max()), 
                                    hover_name="States", 
                                    title=f"{AI_tacy['Years'].unique()} YEAR TRANSACTION AMOUNT", 
                                    fitbounds="locations", 
                                    height=500, 
                                    width=550)
        Indian_map1.update_geos(visible=False)
        st.plotly_chart(Indian_map1)

    with col2:
        Indian_map2 = px.choropleth(AI_tacyg, 
                                    geojson=data, 
                                    locations='States', 
                                    featureidkey="properties.st_nm", 
                                    color="Transaction_count", 
                                    color_continuous_scale="turbo", 
                                    range_color=(AI_tacyg["Transaction_count"].min(), AI_tacyg["Transaction_count"].max()), 
                                    hover_name="States", 
                                    title=f"{AI_tacy['Years'].unique()} YEAR TRANSACTION COUNT", 
                                    fitbounds="locations", 
                                    height=500, 
                                    width=550)
        Indian_map2.update_geos(visible=False)
        st.plotly_chart(Indian_map2)
    return AI_tacy
    

def Transaction_amount_count_Q(df , quarter):
    AI_tacy = df[df["Quarter"] == quarter]
    AI_tacy.reset_index(drop = True , inplace = True)

    AI_tacyg = AI_tacy.groupby("States")[["Transaction_count" , "Transaction_amount"]].sum()
    AI_tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        amt_fig = px.bar(AI_tacyg , x = "States" , y = "Transaction_amount", title = f"{AI_tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT" , color_discrete_sequence = px.colors.sequential.Agsunset_r , height=500, width=550)
        st.plotly_chart(amt_fig)
    with col2:
        cnt_fig = px.bar(AI_tacyg , x = "States" , y = "Transaction_count", title = f"{AI_tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT" , color_discrete_sequence = px.colors.sequential.amp_r , height=450, width=500)
        st.plotly_chart(cnt_fig)

    col1, col2 = st.columns(2)
    # Load geojson data
    with open("states_india.geojson", "r") as f:
        data = json.load(f)

    # Ensure that state names in geojson data match those in the DataFrame
    AI_tacyg["States"] = AI_tacyg["States"].str.title()

    with col1:
        Indian_map1 = px.choropleth(AI_tacyg , 
                                    geojson = data , 
                                    locations = 'States' , 
                                    featureidkey = "properties.st_nm" ,
                                    color = "Transaction_amount" , 
                                    color_continuous_scale = "turbo" , 
                                    range_color = (AI_tacyg["Transaction_amount"].min() , AI_tacyg["Transaction_amount"].max()) , 
                                    hover_name = "States" , 
                                    title = f"{AI_tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT" , 
                                    fitbounds = "locations" , 
                                    height = 500 , 
                                    width = 550)
        Indian_map1.update_geos(visible = False)
        st.plotly_chart(Indian_map1)

    with col2:
        Indian_map2 = px.choropleth(AI_tacyg , 
                                    geojson = data , 
                                    locations = 'States' , 
                                    featureidkey = "properties.st_nm" , 
                                    color = "Transaction_count" , 
                                    color_continuous_scale = "turbo" , 
                                    range_color = (AI_tacyg["Transaction_count"].min() ,  AI_tacyg["Transaction_count"].max()) , 
                                    hover_name = "States" , 
                                    title = f"{AI_tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT" , 
                                    fitbounds = "locations" , 
                                    height = 500 , 
                                    width = 550)
        Indian_map2.update_geos(visible = False)
        st.plotly_chart(Indian_map2)
    return AI_tacy


def Aggregated_Transaction_Name(df , state):

    AT_tacy = df[df["States"] == state]
    AT_tacy.reset_index(drop = True , inplace = True)

    AT_tacyg = AT_tacy.groupby("Transaction_name")[["Transaction_count" , "Transaction_amount"]].sum()
    AT_tacyg.reset_index(inplace = True)

    col1 , col2 = st.columns(2)
    with col1:
        pie1 = px.pie(data_frame = AT_tacyg , names = "Transaction_name" , values = "Transaction_amount" , width = 500 , title = f"{state} TRANSACTION AMOUNT" , hole = 0.5 )
        st.plotly_chart(pie1)

    with col2:
        pie2 = px.pie(data_frame = AT_tacyg , names = "Transaction_name" , values = "Transaction_count" , width = 500 , title = f"{state} TRANSACTION COUNT" , hole = 0.5 )
        st.plotly_chart(pie2)

def Aggregated_User_Plot_Year(df , year):
    AU_aguy = df[df["Years"] == year]
    AU_aguy.reset_index(drop = True , inplace = True)

    AU_aguyg = pd.DataFrame(AU_aguy.groupby("Brand")["Transaction_count"].sum())
    AU_aguyg.reset_index(inplace = True)

    Bar1 = px.bar(AU_aguyg , x = "Brand" , y = "Transaction_count" , title = F"{year} BRANDS AND TRANSACTION COUNT" , width = 900 , color_discrete_sequence = px.colors.sequential.algae_r , hover_name = "Brand")
    st.plotly_chart(Bar1)
    return AU_aguy



def Agg_User_Plot_Quarter(df , quarter):
    AU_aguq = df[df["Quarter"] == quarter]
    AU_aguq.reset_index(drop = True , inplace = True)

    AU_aguqg = pd.DataFrame(AU_aguq.groupby("Brand")["Transaction_count"].sum())
    AU_aguqg.reset_index(inplace = True)

    Bar2 = px.bar(AU_aguqg , x = "Brand" , y = "Transaction_count" , title = f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT" , width = 900 , color_discrete_sequence = px.colors.sequential.Jet_r , hover_name = "Brand")
    st.plotly_chart(Bar2)
    return AU_aguq

def Agg_User_Plot_State(df , state):
    AU_aguqs = df[df["States"] == state]
    AU_aguqs.reset_index(drop = True , inplace = True)
    state_plot = px.line_3d(AU_aguqs , x="Brand" , y  = "Transaction_count" , z = "Percentage" , title="BRANDS , TRANSACTION COUNT , PERCENTAGE" , width = 1000 , hover_name = "States" , markers=True , color_discrete_sequence = px.colors.sequential.Magenta_r)
    st.plotly_chart(state_plot)



def Map_ins_dist(df, state):
    MI_tacy = df[df["States"] == state]
    MI_tacy.reset_index(drop=True, inplace=True)

    MI_tacyg = MI_tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    MI_tacyg.reset_index(inplace=True)

    # Create the subplots with secondary y-axes
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"secondary_y": True}, {"secondary_y": True}]],
        subplot_titles=(
            f"{state} TRANSACTION AMOUNT", 
            f"{state} TRANSACTION COUNT"
        )
    )

    # First bar chart for Transaction Amount
    bar1 = go.Bar(
        x=MI_tacyg["District"],
        y=MI_tacyg["Transaction_amount"],
        name='Transaction Amount (Bar)',
        marker=dict(color='green')
    )
    # First line chart for Transaction Amount
    line1 = go.Scatter(
        x=MI_tacyg["District"],
        y=MI_tacyg["Transaction_amount"],
        mode='lines+markers',
        name='Transaction Amount (Line)',
        line=dict(color='green')
    )

    # Second bar chart for Transaction Count
    bar2 = go.Bar(
        x=MI_tacyg["District"],
        y=MI_tacyg["Transaction_count"],
        name='Transaction Count (Bar)',
        marker=dict(color='red')
    )
    # Second line chart for Transaction Count
    line2 = go.Scatter(
        x=MI_tacyg["District"],
        y=MI_tacyg["Transaction_count"],
        mode='lines+markers',
        name='Transaction Count (Line)',
        line=dict(color='red')
    )

    # Add the first bar and line chart traces to the first subplot
    fig.add_trace(bar1, row=1, col=1, secondary_y=False)
    fig.add_trace(line1, row=1, col=1)

    # Add the second bar and line chart traces to the second subplot
    fig.add_trace(bar2, row=1, col=2, secondary_y=False)
    fig.add_trace(line2, row=1, col=2)

    # Update layout
    fig.update_layout(
        title_text=f"{state} TRANSACTIONS",
        width=1200,
        height=600,
        showlegend=True
    )

    # Update x-axis titles
    fig.update_xaxes(title_text="District", row=1, col=1)
    fig.update_xaxes(title_text="District", row=1, col=2)

    fig.update_yaxes(title_text="Transaction Amount", secondary_y=False, row=1, col=1)
    fig.update_yaxes(title_text="Transaction Count", secondary_y=False, row=1, col=2)
    st.plotly_chart(fig)


def map_user_plot_year(df , year):
    MU_muy =df[df["Years"] == year]
    MU_muy.reset_index(drop = True , inplace = True)
    MU_muyg = MU_muy.groupby("States")[["RegisteredUsers" , "AppOpens"]].sum()
    MU_muyg.reset_index(inplace = True)
    Mi_fig = px.line(MU_muyg , x = "States" , y = ["RegisteredUsers" , "AppOpens"] , title = f"{year} REGISTERED USER AND APP OPENS" , width = 1000 , height = 900 , markers = True)
    st.plotly_chart(Mi_fig)
    return MU_muy


def map_user_quarter(df , quarter):
    MU_muq = df[df["Quarter"] == quarter]
    MU_muq.reset_index(drop = True , inplace = True)

    MU_muqg = MU_muq.groupby("States")[["RegisteredUsers" , "AppOpens"]].sum()
    MU_muqg.reset_index(inplace = True)

    map_fig2 = px.line(MU_muqg , x = "States" , y = ["RegisteredUsers" , "AppOpens"] , title = f"{df['Years'].min()} {quarter} QUARTER  REGESTERED USER APP OPENS" , width = 1000 , height = 900 , markers = True )
    st.plotly_chart(map_fig2)
    return MU_muq


def map_user_dist(df , state):
    MU_muqs = df[df["States"] == state]
    MU_muqs.reset_index(drop = True , inplace = True)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("REGISTERED USERS", "APP OPENS"))
    # Add the Registered Users bar chart
   
    fig.add_trace(
        go.Bar(x=MU_muqs["District"], y=MU_muqs["RegisteredUsers"], name="Registered Users"),
        row=1, col=1
    )

    # Add the App Opens bar chart
  
    fig.add_trace(
        go.Bar(x=MU_muqs["District"], y=MU_muqs["AppOpens"], name="App Opens"),
        row=1, col=2
    )

    # Update the layout
    fig.update_layout(height=800, title_text=f"Registered Users and App Opens")

    # Show the figure
    st.plotly_chart(fig)


def Top_ins_state(df, state):
    # Filter the data for the specified state
    TI_tiy = df[df["States"] == state]
    TI_tiy.reset_index(drop=True, inplace=True)
    
    # Create the subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("TRANSACTION AMOUNT", "TRANSACTION COUNT"))
    
    # Add the Transaction Amount bar chart
    fig.add_trace(
        go.Bar(x=TI_tiy["Quarter"], y=TI_tiy["Transaction_amount"], text=TI_tiy["Pincodes"], name="Transaction Amount"),
        row=1, col=1
    )
    
    # Add the Transaction Count bar chart
    fig.add_trace(
        go.Bar(x=TI_tiy["Quarter"], y=TI_tiy["Transaction_count"], text=TI_tiy["Pincodes"], name="Transaction Count"),
        row=1, col=2
    )
    
    # Update the layout
    fig.update_layout(height=600, width=1200, title_text=f"Transaction Amount and Count in {state}")
    
    # Show the figure
    st.plotly_chart(fig)



def Top_user_year(df , year):
    TU_Tuy = df[df["Years"] == year]
    TU_Tuy.reset_index(drop = True , inplace = True)

    TU_Tuyyg = pd.DataFrame(TU_Tuy.groupby(["States" , "Quarter"])["RegisteredUsers"].sum())
    TU_Tuyyg.reset_index(inplace = True)

    tu_fig = px.bar(TU_Tuyyg , x = "States" , y = "RegisteredUsers" , color = "Quarter" , width = 900 , height = 900 , color_discrete_sequence= px.colors.sequential.algae , hover_name = "States"  , title = f"{year} REGISTERED USERS")

    st.plotly_chart(tu_fig)
    return TU_Tuy



def  top_user_states(df , states):
    TU_Tuys = df[df["States"] == states]
    TU_Tuys.reset_index(drop = True , inplace = True)
    tu_fig2 = px.bar(TU_Tuys , x = "Quarter" , y = "RegisteredUsers" , title = f'{states} REGISTERED USERS ,  PINCODES , QUARTERS' , width = 900 , height = 900 , color = "RegisteredUsers" , hover_data = 'Pincodes' , color_continuous_scale = px.colors.sequential.Electric)
    st.plotly_chart(tu_fig2)


#DataFrame Creation
def top_chart_TA(table_name):
    myDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Skramar$13071999",
        database = "phonepe"
    )
    myCursor = myDB.cursor()

    myCursor.execute(f"select states , sum(Transaction_amount) as Transaction_amount from {table_name} group by states order by transaction_amount desc limit 10 ")

    col1 , col2 , col3 = st.columns(3)

    table1 = myCursor.fetchall()
    myDB.commit()
    df_table1 = pd.DataFrame(table1 , columns = ["States" , "Transaction_amount"])
    with col1:
        fig1 = px.line(df_table1 , x = "States" , y = "Transaction_amount" , title = "TOP 10 TRANSACTION AMOUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Emrld , height = 500  , width = 600 , markers=True)
        st.plotly_chart(fig1)

    myCursor.execute(f"select states , sum(Transaction_amount) as Transaction_amount from {table_name} group by states order by transaction_amount limit 10 ")

    table2 = myCursor.fetchall()
    myDB.commit()
    df_table2 = pd.DataFrame(table2 , columns = ["States" , "Transaction_amount"])

    with col2:
        fig2 = px.line(df_table2 , x = "States" , y = "Transaction_amount" , title = "LAST 10 TRANSACTION AMOUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Emrld , height = 500  , width = 600 , markers=True)
        st.plotly_chart(fig2)

    myCursor.execute(f"select states , avg(Transaction_amount) as Transaction_amount from {table_name} group by states order by transaction_amount")

    table3 = myCursor.fetchall()
    myDB.commit()
    df_table3 = pd.DataFrame(table3 , columns = ["States" , "Transaction_amount"])

    with col3:
        fig3 = px.line(df_table3 , x = "States" , y = "Transaction_amount" , title = "AVERAGE OF TRANSACTION AMOUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Magenta_r , height = 500  , width = 600  , markers=True)
        st.plotly_chart(fig3)

#DataFrame Creation
def top_chart_TC(table_name):
    myDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Skramar$13071999",
        database = "phonepe"
    )
    myCursor = myDB.cursor()

    col1 , col2 , col3 = st.columns(3)

    myCursor.execute(f"select states , sum(Transaction_count) as Transaction_count from {table_name} group by states order by transaction_count desc limit 10 ")

    table1 = myCursor.fetchall()
    myDB.commit()
    df_table1 = pd.DataFrame(table1 , columns = ["States" , "Transaction_count"])

    with col1:
        fig1 = px.line(df_table1 , x = "States" , y = "Transaction_count" , title = "TOP 10 TRANSACTION COUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Emrld , height = 500  , width = 600 , markers=True)
        st.plotly_chart(fig1)

    myCursor.execute(f"select states , sum(Transaction_count) as Transaction_count from {table_name} group by states order by transaction_count limit 10 ")

    table2 = myCursor.fetchall()
    myDB.commit()
    df_table2 = pd.DataFrame(table2 , columns = ["States" , "Transaction_count"])

    with col2:
        fig2 = px.line(df_table2 , x = "States" , y = "Transaction_count" , title = "LAST 10 TRANSACTION COUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Emrld , height = 500  , width = 600 , markers=True)
        st.plotly_chart(fig2)

    myCursor.execute(f"select states , avg(Transaction_count) as Transaction_count from {table_name} group by states order by transaction_count")

    table3 = myCursor.fetchall()
    myDB.commit()
    df_table3 = pd.DataFrame(table3 , columns = ["States" , "Transaction_count"])

    with col3:
        fig3 = px.line(df_table3 , x = "States" , y = "Transaction_count" , title = "AVERAGE OF TRANSACTION COUNT" , hover_name = "States" , color_discrete_sequence = px.colors.sequential.Magenta_r , height = 500  , width = 600  , markers=True)
        st.plotly_chart(fig3)



def top_chart_registered_users(table_name, state):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Skramar$13071999",
        database="phonepe"
    )
    myCursor = myDB.cursor()

    col1 , col2 , col3 = st.columns(3)

    # Top 10 registered users
    query1 = f"SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY RegisteredUsers DESC LIMIT 10"
    myCursor.execute(query1, (state,))
    table1 = myCursor.fetchall()
    df_table1 = pd.DataFrame(table1, columns=["Districts", "RegisteredUsers"])
    with col1:
        fig1 = px.line(df_table1, x="Districts", y="RegisteredUsers", title="TOP 10 REGISTERED USERS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig1)

    # Last 10 registered users
    query2 = f"SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY RegisteredUsers LIMIT 10"
    myCursor.execute(query2, (state,))
    table2 = myCursor.fetchall()
    df_table2 = pd.DataFrame(table2, columns=["Districts", "RegisteredUsers"])

    with col2:
        fig2 = px.line(df_table2, x="Districts", y="RegisteredUsers", title="LAST 10 REGISTERED USERS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig2)

    # Average registered users
    query3 = f"SELECT Districts, AVG(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY RegisteredUsers"
    myCursor.execute(query3, (state,))
    table3 = myCursor.fetchall()
    df_table3 = pd.DataFrame(table3, columns=["Districts", "RegisteredUsers"])

    with col3:
        fig3 = px.line(df_table3, x="Districts", y="RegisteredUsers", title="AVERAGE OF REGISTERED USERS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Magenta_r,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig3)

    myDB.commit()



def top_chart_App_Opens(table_name, state):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Skramar$13071999",
        database="phonepe"
    )
    myCursor = myDB.cursor()

    col1 , col2 , col3 = st.columns(3)

    # Top 10 registered users
    query1 = f"SELECT Districts, SUM(AppOpens) AS AppOpens FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY AppOpens DESC LIMIT 10"
    myCursor.execute(query1, (state,))
    table1 = myCursor.fetchall()
    df_table1 = pd.DataFrame(table1, columns=["Districts", "AppOpens"])
    
    with col1:
        fig1 = px.line(df_table1, x="Districts", y="AppOpens", title="TOP 10 APP OPENS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig1)

    # Last 10 registered users
    query2 = f"SELECT Districts, SUM(AppOpens) AS AppOpens FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY AppOpens LIMIT 10"
    myCursor.execute(query2, (state,))
    table2 = myCursor.fetchall()
    df_table2 = pd.DataFrame(table2, columns=["Districts", "AppOpens"])

    with col2:
        fig2 = px.line(df_table2, x="Districts", y="AppOpens", title="LAST 10 APP OPENS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig2)

    # Average registered users
    query3 = f"SELECT Districts, AVG(AppOpens) AS AppOpens FROM {table_name} WHERE states = %s GROUP BY Districts ORDER BY AppOpens"
    myCursor.execute(query3, (state,))
    table3 = myCursor.fetchall()
    df_table3 = pd.DataFrame(table3, columns=["Districts", "AppOpens"])

    with col3:
        fig3 = px.line(df_table3, x="Districts", y="AppOpens", title="AVERAGE OF APP OPENS",
                    hover_name="Districts", color_discrete_sequence=px.colors.sequential.Magenta_r,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig3)

    myDB.commit()


def top_chart_top_registered_users(table_name):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Skramar$13071999",
        database="phonepe"
    )
    myCursor = myDB.cursor()

    col1 , col2 , col3 = st.columns(3)

    # Top 10 registered users
    query1 = f"SELECT states, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY states ORDER BY RegisteredUsers DESC LIMIT 10;"
    myCursor.execute(query1)
    table1 = myCursor.fetchall()
    df_table1 = pd.DataFrame(table1, columns=["States", "RegisteredUsers"])
    with col1:
        fig1 = px.line(df_table1, x="States", y="RegisteredUsers", title="TOP 10 REGISTERED USERS",
                    hover_name="States", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig1)

    # Last 10 registered users
    query2 = f"SELECT states, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY states ORDER BY RegisteredUsers ASC LIMIT 10;"
    myCursor.execute(query2)
    table2 = myCursor.fetchall()
    df_table2 = pd.DataFrame(table2, columns=["States", "RegisteredUsers"])

    with col2:
        fig2 = px.line(df_table2, x="States", y="RegisteredUsers", title="LAST 10 REGISTERED USERS",
                    hover_name="States", color_discrete_sequence=px.colors.sequential.Emrld,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig2)

    # Average registered users
    query3 = f"SELECT states, AVG(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY states ORDER BY RegisteredUsers;"
    myCursor.execute(query3)
    table3 = myCursor.fetchall()
    df_table3 = pd.DataFrame(table3, columns=["States", "RegisteredUsers"])

    with col3:
        fig3 = px.line(df_table3, x="States", y="RegisteredUsers", title="AVERAGE OF REGISTERED USERS",
                    hover_name="States", color_discrete_sequence=px.colors.sequential.Magenta_r,
                    height=500, width=600, markers=True)
        st.plotly_chart(fig3)

    myDB.commit()



st.set_page_config(layout = "wide")
st.title("PhonePe Data Analysis And Visualization")

with st.container():
    select = option_menu("Main Menu" , ["Home" , "Data Analysis" , "Top Charts"])

if select == "Home" : 
    logo = Image.open(r'C:\Users\S.Kothandaramar\Desktop\PhonePe\PhonePe logo.png')
    # Company Information
    company_name = "PhonePe"
    description = """
    PhonePe is a digital payments platform that allows users to send and receive money, recharge mobile phones, pay utility bills, and make payments in offline stores. It is one of India's leading digital payment platforms, enabling seamless and secure financial transactions.
    """

    services = [
        "Money Transfers",
        "Mobile Recharges",
        "Utility Bill Payments",
        "Merchant Payments",
        "Insurance Services",
        "Investments",
    ]

    features = [
        "Secure Transactions",
        "Instant Payments",
        "User-friendly Interface",
        "Wide Range of Services",
        "24/7 Customer Support",
    ]

    # Display the company logo and name
    st.image(logo, width=900)
    st.title(company_name)

    # Display the description
    st.header("About PhonePe")
    st.write(description)

    # Display the services offered
    st.header("Services")
    for service in services:
        st.markdown(f"- {service}")

    # Display the features
    st.header("Features")
    for feature in features:
        st.markdown(f"- {feature}")

    # Contact Information
    st.header("Contact")
    st.write("For more information, visit our website or contact our support team.")

    st.write("Website: [PhonePe](https://www.phonepe.com)")


elif select == "Data Analysis" : 
    with st.expander(":Red[Select the type of Data]"):
        option = st.selectbox("Type Of Data",["Aggregated" , "Map" , "Top"] , index = None , placeholder = "Select the Data Type")

    if option == "Aggregated":
       
       col1 , col2 = st.columns(2)
       tab1 , tab2 , tab3 = st.tabs(["Aggregated Insurance " , "Aggregated Transaction" , "Aggregated User"])
       with col1:
        with tab1:
            years_ins = st.number_input('Choose a year', min_value=2020, max_value=2023, value=2020)
            Agg_ins_y = Transaction_amount_count_Y(aggregated_insurance , years_ins)

            Quarters = st.number_input('Choose a  Quarter', min_value=1, max_value=4, value=1)
            
            if years_ins == 2020 and Quarters == 1 : st.text("NO DATA FOUND FOR ANALYSIS")
            else : Transaction_amount_count_Q(Agg_ins_y , Quarters)

        with tab2:
            years_trans = st.number_input('Select a Year', min_value=2018, max_value=2023, value=2018)
            Agg_trans_y = Transaction_amount_count_Y(aggregated_transaction , years_trans)
            
            states_AT1 = st.selectbox("Select the State" , Agg_trans_y["States"].unique() , index = None , placeholder = "Select the State")
            if states_AT1 == None : st.text("Please select state to show analysis")
            else : Aggregated_Transaction_Name(Agg_trans_y , states_AT1)

            Quarters = st.number_input('Select a Quarter', min_value=1, max_value=4, value=1)
                       
            Agg_trans_Q = Transaction_amount_count_Q(Agg_trans_y, Quarters)
            Aggregated_Transaction_Name(Agg_trans_Q, states_AT1)

        with tab3:
            years_User = st.number_input('Choose a Year', min_value=2018, max_value=2023, value=2018)
            Agg_User_Y = Aggregated_User_Plot_Year(aggregated_user , years_User)

            Quarters = st.number_input('Choose a Quarter', min_value=1, max_value=4, value=1)
            Agg_User_Q = Agg_User_Plot_Quarter(Agg_User_Y, Quarters)

            states_AT3 = st.selectbox("Choose the State", Agg_trans_Q["States"].unique(), index=None, placeholder="Choose the State")
            if states_AT3 == None : st.text("Please select state to show analysis")
            else : Agg_User_Plot_State(Agg_User_Q , states_AT3)



    elif option == "Map":
        tab1 , tab2 , tab3 = st.tabs(["Map Insurance " , "Map Transaction" , "Map User"])

        with tab1:
           map_years_ins = st.number_input('Choose a year', min_value=2020, max_value=2023, value=2020)
           map_ins_h_y = Transaction_amount_count_Y(map_insurance_hover , map_years_ins)

           states_MI1 = st.selectbox("Select the State" , map_ins_h_y["States"].unique() , index = None , placeholder = "Select the State")
           if states_MI1 == None : st.text("Please select state to show analysis")
           else : Map_ins_dist(map_ins_h_y, states_MI1)

           Quarters = st.number_input('Choose a  Quarter', min_value=1, max_value=4, value=1)
           if map_years_ins == 2020 and Quarters == 1 : st.text("NO DATA FOUND FOR ANALYSIS")
           else : 
                map_ins_Q = Transaction_amount_count_Q(map_ins_h_y , Quarters)
                Map_ins_dist(map_ins_Q, states_MI1)

        with tab2:
           map_years_trans = st.number_input('Choose a year', min_value=2018, max_value=2023, value=2018)
           map_trans_y = Transaction_amount_count_Y(map_transaction , map_years_trans)

           states_MT1 = st.selectbox("Select the State" , map_trans_y["States"].unique() , index = None , placeholder = "Choose the State")
           if states_MT1 == None : st.text("Please select state to show analysis")
           else : Map_ins_dist(map_trans_y, states_MT1)

           Quarters = st.number_input('Select a  Quarter', min_value=1, max_value=4, value=1)
            
           map_trans_Q = Transaction_amount_count_Q(map_trans_y , Quarters)
           Map_ins_dist(map_trans_Q, states_MT1)


        with tab3:
           map_years_user = st.number_input('Select a year', min_value=2018, max_value=2023, value=2018)
           map_user_y = map_user_plot_year(map_user , map_years_user)

           Quarters = st.number_input('Quarters', min_value=1, max_value=4, value=1)
           map_user_q = map_user_quarter(map_user_y , Quarters)

           states_MU1 = st.selectbox("Choose the State" , map_user_q["States"].unique() , index = None , placeholder = "Choose the State")
           if states_MU1 == None : st.text("Please select state to show analysis")
           else :  map_user_dist(map_user_q, states_MU1)
        

    elif option == "Top":
        tab1 , tab2 , tab3 = st.tabs(["Top Insurance " , "Top Transaction" , "Top User"])

        with tab1:
           top_years_ins = st.number_input('Choose a year', min_value=2020, max_value=2023, value=2020)
           top_ins_y = Transaction_amount_count_Y(top_insurance , top_years_ins)

           states_TI1 = st.selectbox("Choose the State" , top_ins_y["States"].unique() , index = None , placeholder = "Choose the State")
           if states_TI1 == None : st.text("Please select state to show analysis")
           else : Top_ins_state(top_ins_y, states_TI1)

           Quarters = st.number_input('Quarters', min_value=1, max_value=4, value=1)
           if  top_years_ins == 2020 and Quarters == 1 : st.text("NO DATA FOUND FOR ANALYSIS")
           else : Transaction_amount_count_Q(top_ins_y , Quarters)

        with tab2:
            top_years_trans = st.number_input('Select a year', min_value=2018, max_value=2023, value=2018)
            top_trans_y = Transaction_amount_count_Y(top_transaction , top_years_trans)

            states_TI2 = st.selectbox("Choose the State" , top_trans_y["States"].unique() , index = None , placeholder = "Select the State")
            if states_TI2 == None : st.text("Please select state to show analysis")
            else : Top_ins_state(top_trans_y, states_TI2)

            Quarters = st.number_input('select a Quarters', min_value=1, max_value=4, value=1)
           
            Transaction_amount_count_Q(top_trans_y , Quarters)


        with tab3:
           top_years_user = st.number_input('Choose a year', min_value=2018, max_value=2023, value=2018)

           top_user_y =  Top_user_year(top_user , top_years_user)

           states_TI3 = st.selectbox("Select the State" , top_user_y["States"].unique() , index = None , placeholder = "Select the State")

           if states_TI3 == None : st.text("Please select state to show analysis")
           else : top_user_states(top_user_y , states_TI3)


elif select == "Top Charts":
    queries = st.selectbox("Select the Queries" , ["1. Transaction Amount and Count of Aggregated Insurance",

    "2. Transaction Amount and Count of Map Insurance",

    "3. Transaction Amount and Count of Top Insurance",

    "4. Transaction Amount and Count of Aggregated Transaction",

    "5. Transaction Amount and Count of Map Transaction" ,

    "6. Transaction Amount and Count of Top Transaction",

    "7. Transaction Count of Aggregated User",

    "8. Registered users of Map User",

    "9. App opens of Map User",

    "10. Registered users of Top User"] , index = None)

    if queries == "1. Transaction Amount and Count of Aggregated Insurance" :

        st.subheader("TRANSACTION AMOUNT")
        top_chart_TA("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("aggregated_insurance")
        

    elif queries == "2. Transaction Amount and Count of Map Insurance" :
        st.subheader("TRANSACTION AMOUNT")
        top_chart_TA("map_insurance_hover")
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("map_insurance_hoverj")                

    elif queries == "3. Transaction Amount and Count of Top Insurance" :
       st.subheader("TRANSACTION AMOUNT")
       top_chart_TA("top_insurance")
       st.subheader("TRANSACTION COUNT")
       top_chart_TC("top_insurance")

    elif queries == "4. Transaction Amount and Count of Aggregated Transaction" :
        st.subheader("TRANSACTION AMOUNT")
        top_chart_TA("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("aggregated_transaction")
       
    elif queries ==  "5. Transaction Amount and Count of Map Transaction" :
        st.subheader("TRANSACTION AMOUNT")
        top_chart_TA("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("map_transaction")
        
    elif queries == "6. Transaction Amount and Count of Top Transaction" :
        st.subheader("TRANSACTION AMOUNT")
        top_chart_TA("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("top_transaction")
       

    elif queries =="7. Transaction Count of Aggregated User" :
        st.subheader("TRANSACTION COUNT")
        top_chart_TC("aggregated_user")        

    elif queries == "8. Registered users of Map User" :
        st.subheader("REGISTERED USERS")
        states1 = st.selectbox("Select the state" , map_user["States"].unique() , index = None)
        if states1 == None: st.text("Select a state to show analysis")
        else:
            top_chart_registered_users("map_user" , states1)           

    elif queries == "9. App opens of Map User" :
        st.subheader("REGISTERED USERS")
        states2 = st.selectbox("Select the state" , map_user["States"].unique() , index = None)
        if states2 == None: st.text("Select a state to show analysis")
        else:
            top_chart_App_Opens("map_user" , states2)
        
            
    elif queries == "10. Registered users of Top User" :
        st.subheader("REGISTERED USERS")
        top_chart_top_registered_users("top_user")      