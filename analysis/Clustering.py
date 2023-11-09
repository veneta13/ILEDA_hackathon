import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def cluster(df, number_of_clusters = 3):
  model = KMeans(n_clusters = number_of_clusters)
  clusters = model.fit_predict(df)

  n_components = 3
  pca = PCA(n_components=n_components)
  df_pca = pca.fit_transform(df)
  feature_importance = pd.DataFrame(abs(pca.components_), columns=df.columns)

  first_axis = [(df.columns[idx], pca.components_[0][idx]) for idx in np.argsort(pca.components_[0])[-3:]]
  second_axis = [(df.columns[idx], pca.components_[1][idx]) for idx in np.argsort(pca.components_[1])[-3:]]
  third_axis = [(df.columns[idx], pca.components_[2][idx]) for idx in np.argsort(pca.components_[2])[-3:]]

  all_axis = [first_axis, second_axis, third_axis]

  fig = px.scatter_3d(df_pca, x=0, y=1, z=2, color=clusters, opacity=0.7,
                    title='K-means Clustering with PCA 3D Visualization',
                    labels={'0': 'X', '1': 'Y', '2': 'Z'},
                    color_continuous_scale='viridis')
  fig.show()

  axis_importance = pd.DataFrame({'first': [first_axis[0][1], second_axis[0][1], third_axis[0][1]],
                                  'second': [first_axis[1][1], second_axis[1][1], third_axis[1][1]],
                                  'third': [first_axis[2][1], second_axis[2][1], third_axis[2][1]]})
  bar_width = 0.2
  bar_positions = range(3)

  plt.bar([pos + bar_width for pos in bar_positions], axis_importance['first'], width=bar_width)
  plt.bar(bar_positions, axis_importance['second'], width=bar_width)
  plt.bar([pos - bar_width for pos in bar_positions], axis_importance['third'], width=bar_width)
  for pos in bar_positions:
    plt.text(pos + bar_width, 0 + first_axis[pos][1]/10, all_axis[pos][0][0], ha='center', va='bottom', rotation=90)
    plt.text(pos, 0 + second_axis[pos][1]/10, all_axis[pos][1][0], ha='center', va='bottom', rotation=90)
    plt.text(pos - bar_width, 0 + third_axis[pos][1]/10, all_axis[pos][2][0], ha='center', va='bottom', rotation=90)

  plt.xticks(bar_positions, ['X', 'Y', 'Z'])
  plt.xlabel('Axis')
  plt.ylabel('Value')
  plt.title('Most Importnat Features')
  plt.legend()
