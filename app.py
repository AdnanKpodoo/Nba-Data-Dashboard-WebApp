import streamlit as st

import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px




st.set_page_config(page_title= "NBA Dashboard",
                   page_icon=":bar_chart",
                   layout="wide"
                   )

# Load the datasets
@st.cache_data
def load_data():
    return pd.read_csv('players.csv')

@st.cache_data
def load_data2():
    return pd.read_csv('player_regions.csv')

df = load_data()
df2 = load_data2()


# Merge the two datasets based on a common column, e.g., 'playerid'
merged_df = pd.merge(df, df2, on='school')

#merged_df = merged_df.dropna()
#st.write(merged_df.head(10))


st.title('NBA Analysis Draft Dashboard')
st.subheader("Analysis Introduction")
st.write(
'Hello my name is Adnan Kpodo and I am an aspirirng Data Analyst who created this web app to showcase my findings in regards to the NBA draft pick. The question I wil be answeing is what region produces the most round 1 picks.(This is still a work in progress :)'
         )



st.subheader("Dataset Values")
st.write("This dataset is the final result after the data transformation and cleaining process, it contains everything needed for me to make my insights.")
st.write(merged_df.head(10))



merged_df = pd.get_dummies(merged_df, columns=['draft_round'], drop_first=True)
merged_df.dropna()
merged_df.isnull().sum()

merger = merged_df[(merged_df['draft_year'] >= 2019)]
#st.write(merger.head())

# Calculate the count of draft_round_1.0 by Region_Continent
count_data = merger.groupby('Region_Continent')['draft_round_1.0'].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    # Pie chart
    fig_pie = px.pie(count_data,
                     names='Region_Continent',
                     values='draft_round_1.0',
                     title='Percentage of Round 1 Picks by Region (2019-2022)',
                     labels={'Region_Continent': 'Region Continent', 'draft_round_1.0': 'Count'},
                     hole=0.4)

    # Update layout for better readability
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(title_font_size=18, showlegend=True, template='plotly_dark')

    # Display the interactive pie chart in Streamlit
    st.plotly_chart(fig_pie)

with col2:

    # Plotly bar plot
    fig_bar = px.bar(count_data, x='Region_Continent', y='draft_round_1.0',
                     title='Draft Round 1 Count by Region (2019-2022)',
                     labels={'Region_Continent': 'Region Continent', 'Round 1': 'Count'},
                     text='draft_round_1.0')

    # Update layout for better readability
    fig_bar.update_layout(xaxis_title='Region Continent', yaxis_title='Count',
                          xaxis_tickangle=-45, title_font_size=20, template='plotly_dark')

    # Display the interactive plot in Streamlit
    st.plotly_chart(fig_bar)

# Optionally, display the Seaborn plot as well
st.subheader("Seaborn Count Plot")

plt.figure(figsize=(14, 7))
plt.title('Draft Round 1 & 2 Picks From 2019-2022')
plt.xlabel('Region Continent')
plt.ylabel('Count')

ax = sns.countplot(data=merger, x='Region_Continent', hue='draft_round_1.0')

# Display count values on each bar
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                textcoords='offset points')

# Show the Seaborn plot
st.pyplot(plt)