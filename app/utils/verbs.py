import matplotlib.pyplot as plt
import plotly.graph_objects as go


def get_verb_lollipop(df):
    """
    Generate a lollipop plot to visualize interaction counts for each verb.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing interaction data.

    Returns:
    - plt.Figure: The generated lollipop plot.
    """
    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    ax.set_title(
        'Interactions',
        fontdict={'size': 22}
    )
    ax.set_xlabel(
        'Count',
        fontdict={
            'size': 15
        }
    )
    ax.set_yticks(range(len(df[['verb.id']].value_counts())))
    ax.set_yticklabels(
        df['verb.id'].drop_duplicates().tolist(),
        fontdict={
            'horizontalalignment': 'right',
            'size': 15
        }
    )
    ax.hlines(
        y=range(len(df[['verb.id']].value_counts())),
        xmin=0,
        xmax=df[['verb.id']].value_counts().to_frame()[['count']].max(),
        color='darkgray',
        alpha=0.7,
        linewidth=1,
        linestyles='dashdot'
    )
    ax.scatter(
        y=range(len(df[['verb.id']].value_counts())),
        x=df[['verb.id']].value_counts().to_frame()[['count']],
        s=75,
        color='firebrick',
        alpha=0.7
    )
    return fig


def get_verb_radar_verb(df):
    df_radar = (df
                .groupby(['Course', 'verb.id'])['verb.id']
                .count()
                .unstack(fill_value=0)
                .stack()
                .reset_index()
                .rename(columns={0: 'count'}))

    fig = go.Figure()

    for course in df_radar['Course'].drop_duplicates().tolist():
        fig.add_trace(go.Scatterpolar(
            r=df_radar[df_radar['Course'] == course]['count'].tolist(),
            theta=df_radar['verb.id'].drop_duplicates().tolist(),
            fill='toself',
            name=course
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        showlegend=True
    )

    return fig


def get_verb_radar_course(df):
    """
    Generate a radar plot to visualize the distribution of verb interactions across different courses.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing interaction data.

    Returns:
    - go.Figure: The generated radar plot.
    """
    df_radar = (df
                .groupby(['verb.id', 'Course'])['Course']
                .count()
                .unstack(fill_value=0)
                .stack()
                .reset_index()
                .rename(columns={0: 'count'}))

    fig = go.Figure()

    for verb in df_radar['verb.id'].drop_duplicates().tolist():
        fig.add_trace(go.Scatterpolar(
            r=df_radar[df_radar['verb.id'] == verb]['count'].tolist(),
            theta=df_radar['Course'].drop_duplicates().tolist(),
            fill='toself',
            name=verb
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        showlegend=True
    )

    return fig
