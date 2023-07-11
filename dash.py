"""
This is a dashboard to visualize the data from the MetaPals game.

"""

import requests
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import urllib.parse
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pymongo import MongoClient
import streamlit as st
import altair as alt
import polars as pl
import sys
sys.path.append('/Users/joaovictorfarrulladarze/Desktop/Metapals/Workspace/Dashboard/python_files')
from python_files.clustering import df, event_counts, event_counts_pd, event_names, polar, pie


# from st_pages import Page, add_page_title, show_pages



# ### MongoDB Conection
#
# client = MongoClient('mongodb://localhost:27017/')
#
# db = client['event_database']
# collection = db['events']
#
#
# ### Load data
# @st.cache_data
# def load_data(_collection):
#     # Define the events of interest
#     events_of_interest = ['Picking Up Dark Matter', 'Sleeping', 'Patting',
#                           'Claim Daily Rewards', 'Waking Up', 'Feeding', 'Visit Sanctuary',
#                           'Shop Transaction', 'Calling Pet', 'Swap Wearable',
#                           'Equip Wearable', 'Detach Wearable']
#
#     # Fetch the data from MongoDB
#     query = {"event": {"$in": events_of_interest}}
#
#     # Convert to Polars DataFrame
#     data = pl.DataFrame(list(collection.find(query).limit(1000)))
#
#     # Extract properties into new columns
#     data = data.lazy().select(
#         *[data[col].apply(pl.col("properties").get(pl.lit(col))).alias(col) for col in data.columns])
#     data = data.drop("properties")
#     data = data.fetch()
#
#     return data


#   data = pd.DataFrame(list(collection.find(query)))

#   # Extract properties into new columns
#   data = pd.concat([data.drop('properties', axis=1),
#                   data['properties'].apply(pd.Series)], axis=1)
#   return data


# data_load_state = st.text('Loading data...')
# data = load_data(collection)
# data_load_state.success("Done! (using st.cache_data)")

# """ Clustering """
# # Count the number of events per user
# event_counts = data.groupby('distinct_id')['event'].value_counts().unstack().fillna(0)
#
# X = event_counts
# scaler = MinMaxScaler()
# X_scaled = scaler.fit_transform(X)
#
# # Perform clustering using K-means
# kmeans = KMeans(
#     n_clusters=3,
#     init="k-means++",
#     n_init=10,
#     tol=1e-04,
#     random_state=42
# )
# kmeans.fit(X_scaled)
#
# clusters = pd.DataFrame(X_scaled)
# clusters['label'] = kmeans.labels_
# polar = clusters.groupby("label").mean().reset_index()
# polar = pd.melt(polar, id_vars=["label"])
#
# # Name the cluster variables
# event_names = event_counts.columns.to_list()
# polar["variable"] = polar["variable"].map(lambda x: event_names[x])
#
# # Visualize the clusters
# fig, ax = plt.subplots(figsize=(14, 8))
# sns.barplot(data=polar, x="variable", y="value", hue="label", ax=ax)
# plt.xticks(rotation=45)
# plt.title("Cluster Centers - Polar Plot")
#
# cluster_chart = alt.Chart(polar).mark_bar().encode(
#     x=alt.X('variable:N', title='Variable'),
#     y=alt.Y('value:Q', title='Value'),
#     color='label:N',
#     tooltip=['variable', 'value', 'label']
# ).properties(
#     width=700,
#     height=400,
#     title='Cluster Centers - Polar Plot'
# ).configure_axis(
#     labelAngle=45
# ).interactive()
#
# # Calculate the cluster distribution
# pie = clusters.groupby('label').size().reset_index()
# pie.columns = ['label', 'value']
# print(pie)
#
# # Create the pie chart using Altair
# chart = alt.Chart(pie).mark_arc().encode(
#     # alt.X('value:Q', stack='normalize', title='Percentage'),
#     theta='value',
#     color='label:N',
#     tooltip=['label', 'value', 'percentage:Q']
# ).properties(
#     width=500,
#     height=400,
#     title='Cluster Distribution'
# ).interactive()
#
# # General Info
# events_num = data.shape[0]

""" Streamlit App """

# Declaring the pages in your app:

# show_pages(
#     [
#         Page("example_app/streamlit_app.py", "Home", "🏠"),
#         # Can use :<icon-name>: or the actual icon
#         Page("example_app/example_one.py", "Example One", ":books:"),
#         # The pages appear in the order you pass them
#         Page("example_app/example_four.py", "Example Four", "📖"),
#         Page("example_app/example_two.py", "Example Two", "✏️"),
#         # Will use the default icon and name based on the filename if you don't
#         # pass them
#         Page("example_app/example_three.py"),
#         Page("example_app/example_five.py", "Example Five", "🧰"),
#     ]
# )

# add_page_title()  # Optional method to add title and icon to current page

st.title("MetaPals Dashboard")
st.markdown("Hello, **MetaPals Team**!, this is the place where you can see complex data :sunglasses:")

st.sidebar.success("Select a page to start")

col1, col2, col3 = st.columns(3)
col1.metric("Number of Events", 10, delta=None)
col2.metric("Unique users", df['distinct_id'].n_unique(), delta=None)
col3.metric("Patting events", 20, delta=None)
# st.dataframe(data)
# Statistics table - too heavy
# st.table(data)

# Display the plot using Streamlit
# st.subheader("Clustering")
# st.text("Here we use all the core metapals interactions to build the cluster analysis. Data starts on the Feb 10th")
# st.pyplot(fig)
# st.altair_chart(cluster_chart)
#
# # Display the pie chart using Streamlit
# st.subheader("Cluster distribution")
# st.text("As follows we have the proportion of every cluster on the numbers of players in each")
# col4, col5 = st.columns(2)
# col4.altair_chart(chart)

st.markdown("This graph shows in which hours in a day users tend to be more active in the game.")


