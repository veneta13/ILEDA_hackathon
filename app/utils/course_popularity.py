import pandas as pd
import matplotlib.pyplot as plt

def course_popularity(df):
    """
    Analyzes course popularity based on user interactions and visualizes the results through three plots.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the dataset.

    Returns:
    - fig1 (plt.Figure): Pie chart depicting the distribution of user interactions across courses.
    - fig2 (plt.Figure): Boxplot illustrating the variation in user interactions by course.
    - fig3 (plt.Figure): Scatter plot showing the relationship between the median interaction count per person
                        and the number of students enrolled in each course.
    """
    color_df = pd.DataFrame({
        'Institution': df['Institution'].unique(),
        'color': ['red', 'blue', 'green', 'yellow']
    })
    color_df = color_df.merge(df[['Course', 'Institution']].drop_duplicates(), how='left')

    colors = [color_df[color_df['Course'] == course].iloc[0][['color']].iloc[0] for course in
              list(df['Course'].value_counts().to_frame().index)]

    fig1, ax = plt.subplots()
    fig1.set_figwidth(10)
    fig1.set_figheight(10)
    plt.title("Number of user interactions by course")
    ax.pie(
        list(df['Course'].value_counts()),
        labels=df['Course'].value_counts().to_frame().index.tolist(),
        autopct='%.0f%%',
        colors=colors
    )
    plt.plot()

    df_actor_count = df[['Course', 'actor.id']].groupby(['Course']).nunique()
    actor_interactions = [
        [
            df[df['Course'] == course_name].groupby(['actor.id']).size().to_frame('size')['size']
            for course_name in df['Course'].unique()
        ],
        [
            course_name
            for course_name in df['Course'].unique()
        ],
    ]

    colors = [color_df[color_df['Course'] == course].iloc[0][['color']].iloc[0] for course in actor_interactions[1]]

    fig2, ax = plt.subplots()
    fig2.set_figwidth(10)
    fig2.set_figheight(10)
    plt.title("Number of user interactions by course")
    boxpl = ax.boxplot(
        actor_interactions[0],
        notch=True,
        patch_artist=True,
        labels=actor_interactions[1],
    )
    for patch, color in zip(boxpl['boxes'], colors):
        patch.set_facecolor(color)
    plt.xticks(rotation=90)

    df_median_interaction = df.groupby(['Course', 'actor.id']).size().groupby(level=0).median().to_frame(
        'median').reset_index()

    df_median_count = df_median_interaction.merge(df_actor_count.reset_index().drop_duplicates(), how='left')
    df_median_count = df_median_count.merge(df[['Course', 'Teaching']].drop_duplicates(), how='right')

    colors = [
        color_df[color_df['Course'] == course].iloc[0][['color']].iloc[0]
        for course
        in list(df_median_count['Course'].value_counts().to_frame().index)
    ]

    markers = [
        (
            '*'
            if df_median_count[df_median_count['Course'] == course].iloc[0]['Teaching'] == 'Flipped classroom'
            else 'o'
        )
        for course
        in list(df_median_count['Course'].value_counts().to_frame().index)
    ]

    fig3, ax = plt.subplots()
    fig3.set_figwidth(10)
    fig3.set_figheight(10)
    for xp, yp, color, marker in zip(
            df_median_count['median'],
            df_median_count['actor.id'],
            colors,
            markers
    ):
        ax.scatter(
            x=xp,
            y=yp,
            c=color,
            marker=marker,
            s=100
        )
    plt.xlabel('Interaction count per person (median)', fontsize=15)
    plt.ylabel('Number of students enrolled in course', fontsize=15)

    return fig1, fig2, fig3
