import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def load_courses(directory):
    """
    Load course data from CSV files in a specified directory.

    Parameters:
    - directory (str): The directory containing CSV files.

    Returns:
    - dict: A dictionary where keys are course names and values are corresponding DataFrames.
    """
    files = [os.path.join(directory, file_name) for file_name in os.listdir(directory)]
    courses = {}

    for file_name in files:
        # Extracting the course name from the file name (excluding the ".csv" extension)
        course_name = os.path.splitext(os.path.basename(file_name))[0]
        if course_name == '.ipynb_checkpoints':
            continue

        # Reading the CSV file with the full path
        course_data = pd.read_csv(file_name)
        columns_to_drop = [col for col in course_data if
                           'min_score' in col or 'max_score' in col or 'institution' in col]
        course_data = course_data.drop(columns_to_drop, axis=1)

        # Adding the course data to the dictionary
        courses[course_name] = course_data

    return courses


def cluster(course_name, number_of_clusters=3):
    """
    Perform K-means clustering on course data and generate 3D visualization with PCA.

    Parameters:
    - course_name (str): Name of the course to be clustered.
    - number_of_clusters (int): Number of clusters for K-means. Default is 3.

    Returns:
    - tuple: Two figures - 3D scatter plot and bar plot of the most important features.
    """
    courses = load_courses('data/clustering_data')  # Tук пътя трябва да оправим
    course_name = course_name.replace(' ', '_')
    df = courses[course_name]

    n_components = 3
    pca = PCA(n_components=n_components)
    df_pca = pca.fit_transform(df)

    model = KMeans(n_clusters=number_of_clusters)
    clusters = model.fit_predict(df_pca)
    components = pd.DataFrame(pca.components_, columns=df.columns)

    first_axis = [
        (list(components.iloc[0].sort_values(ascending=False)[:3].index)[idx].replace('_', ' '),
         list(components.iloc[0].sort_values(ascending=False)[:3])[idx]) for idx in range(3)]
    second_axis = [
        (list(components.iloc[1].sort_values(ascending=False)[:3].index)[idx].replace('_', ' '),
         list(components.iloc[1].sort_values(ascending=False)[:3])[idx]) for idx in range(3)]
    third_axis = [
        (list(components.iloc[2].sort_values(ascending=False)[:3].index)[idx].replace('_', ' '),
         list(components.iloc[2].sort_values(ascending=False)[:3])[idx]) for idx in range(3)]

    all_axis = [first_axis, second_axis, third_axis]

    fig1 = px.scatter_3d(
        df_pca,
        x=0,
        y=1,
        z=2,
        color=clusters,
        opacity=0.7,
        title='K-means Clustering with PCA (3D Visualization)',
        labels={'0': 'X', '1': 'Y', '2': 'Z'},
        color_continuous_scale='viridis'
    )

    axis_importance = pd.DataFrame({
        'first': [first_axis[0][1], second_axis[0][1], third_axis[0][1]],
        'second': [first_axis[1][1], second_axis[1][1], third_axis[1][1]],
        'third': [first_axis[2][1], second_axis[2][1], third_axis[2][1]]
    })
    fig2, ax = plt.subplots()

    bar_width = 0.2
    bar_positions = range(3)

    ax.bar(
        [pos + bar_width for pos in bar_positions],
        axis_importance['first'],
        width=bar_width,
        color='#fde725'
    )
    ax.bar(
        bar_positions,
        axis_importance['second'],
        width=bar_width,
        color='#21918c'
    )
    ax.bar(
        [pos - bar_width for pos in bar_positions],
        axis_importance['third'],
        width=bar_width,
        color='#A40154'
    )

    for pos in bar_positions:
        plt.text(
            pos + bar_width,
            0 + first_axis[pos][1] / 10,
            all_axis[pos][0][0],
            ha='center',
            va='bottom',
            rotation=90
        )
        plt.text(
            pos,
            0 + second_axis[pos][1] / 10,
            all_axis[pos][1][0],
            ha='center',
            va='bottom',
            rotation=90
        )
        plt.text(
            pos - bar_width,
            0 + third_axis[pos][1] / 10,
            all_axis[pos][2][0],
            ha='center',
            va='bottom',
            rotation=90
        )

    plt.xticks(bar_positions, ['X', 'Y', 'Z'])
    plt.xlabel('Axis')
    plt.ylabel('Value')
    plt.title('Most Important Features')

    return fig1, fig2
