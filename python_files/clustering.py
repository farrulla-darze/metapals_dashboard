
import polars as pl
import pandas as pd
import numpy as np
from pymongo import MongoClient 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import sqlite3


# Access the sqlite database
conn = sqlite3.connect('/Users/joaovictorfarrulladarze/Desktop/Metapals/Workspace/Dashboard/databases/event_database.db')
c = conn.cursor()

# Fetch data from collection using query and make it a pl.DataFrame
c.execute('''SELECT * FROM event_counts''')

# get the name of the columns in the table
column_names = list(map(lambda x: x[0], c.description))

# make a dataframe from the query result
event_counts = pl.DataFrame(c.fetchall(), column_names)

# Transform the pl.DataFrame to a pandas.DataFrame in order to work with seaborn and sci-kit learn
event_counts_pd = event_counts.to_pandas()


# Select all columns but index and distinct_id
X = event_counts_pd.iloc[:, 2:]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

inertia = []
for i in range(1, 11):
    kmeans = KMeans(
        n_clusters=i,
        init="k-means++",
        n_init=10,
        tol=1e-04,
        random_state=42
    )
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(np.arange(1, 11), inertia)
plt.title("Inertia vs Cluster Number")
plt.xlabel("Cluster Number")
plt.ylabel("Inertia")
plt.show()


# Perform clustering using K-means
kmeans = KMeans(
    n_clusters=3,
    init="k-means++",
    n_init=10,
    tol=1e-04, 
    random_state=42
)
kmeans.fit(X_scaled)

clusters = pd.DataFrame(X_scaled)
clusters['label'] = kmeans.labels_
polar = clusters.groupby("label").mean().reset_index()
polar = pd.melt(polar, id_vars=["label"])

# Name the cluster variables
event_names = event_counts.to_pandas().columns[1:].to_list()
polar["variable"] = polar["variable"].map(lambda x: event_names[x])


# Visualize the clusters
plt.figure(figsize=(14, 8))
sns.barplot(data=polar, x="variable", y="value", hue="label")
plt.xticks(rotation=45)
plt.title("Cluster Centers - Polar Plot")
plt.show()

# Visualize the clusters distribution
pie = clusters.groupby('label').size().reset_index()
pie.columns = ['label', 'value']

sns.set(style="whitegrid")
plt.pie(pie['value'], labels=pie['label'], colors=['blue', 'red', 'green'], autopct='%1.1f%%')
plt.axis('equal')
plt.title("Cluster Distribution")
plt.show()


#%%
