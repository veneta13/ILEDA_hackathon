import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf


def get_actions(df, min_time=None, max_time=None):
    if min_time is None and max_time is None:
        min_time = df.index[0]
        max_time = df.index[-1]

    activities_by_days = dict()
    activities_by_days['timestamp'] = []
    activities_by_days['assessments'] = []
    activities_by_days['non_assessments'] = []
    activities_by_days['total'] = []

    non_assessment_activities = ['resource', 'discussion', 'link', 'page', 'module', 'quiz', 'homework', 'test',
                                 'forum-topic', 'review', 'course']
    time = min_time
    while time <= max_time:
        next_time = time + pd.Timedelta(days=1)
        daily_df = df[(df.index >= time) & (df.index < next_time)]

        activities_by_days['timestamp'].append(time)
        activities_by_days['assessments'].append(daily_df[(~daily_df['result.score.scaled'].isna()) & (
                daily_df['object.definition.type'] != 'cmi.interaction')].shape[0])
        activities_by_days['non_assessments'].append(daily_df[(daily_df['object.definition.type'].isin(
            non_assessment_activities)) & (daily_df['result.score.scaled'].isna())].shape[0])
        activities_by_days['total'].append(daily_df.shape[0])

        time = next_time

    activity_df = pd.DataFrame(activities_by_days).set_index('timestamp')

    return activity_df


def actor_timeline(df, actor_id):
    actor_df = df[df['actor.id'] == actor_id]
    actor_df = actor_df.set_index('timestamp').sort_index()

    colours = {'UEF': 'red', 'SU': 'blue', 'UL': 'green', 'BMU': 'yellow'}
    min_time = pd.Timestamp(min(df['timestamp']).year, min(df['timestamp']).month, min(df['timestamp']).day)
    max_time = pd.Timestamp(max(df['timestamp']).year, max(df['timestamp']).month, max(df['timestamp']).day)

    actor_actions = get_actions(actor_df, min_time, max_time)
    institution_colour = colours[actor_df['Institution'].iloc[0]]
    return actor_actions, institution_colour


def display_actions(df, actor_id, metric):
    actor_actions, institution_colour = actor_timeline(df, actor_id)
    fig, ax = plt.subplots()

    ax.figure(figsize=(10, 5))
    ax.plot(actor_actions.index, actor_actions[metric], c=institution_colour)
    ax.xticks(rotation=45, ha='right')

    ax.xlabel('Date')
    ax.ylabel('Count')
    ax.title('Activity')

    ax.tight_layout()
    return fig


def course_or_institution_timeline(df, name):
    object_type = 'Course'
    if name in set(df['Institution']):
        object_type = 'Institution'

    object_df = df[df[object_type] == name]
    object_df = object_df.set_index('timestamp').sort_index()

    colours = {'UEF': 'red', 'SU': 'blue', 'UL': 'green', 'BMU': 'yellow'}
    min_time = pd.Timestamp(min(df['timestamp']).year, min(df['timestamp']).month, min(df['timestamp']).day)
    max_time = pd.Timestamp(max(df['timestamp']).year, max(df['timestamp']).month, max(df['timestamp']).day)

    object_actions = get_actions(object_df)
    institution_colour = colours[object_df['Institution'].iloc[0]]
    return object_actions, institution_colour


def display_course_or_institution_actions(df, name, metric):
    object_actions, institution_colour = course_or_institution_timeline(df, name)

    fig, ax = plt.subplots()
    if metric == 'both':
        ax.plot(object_actions.index, object_actions['non_assessments'], c=institution_colour)
        ax.plot(object_actions.index, object_actions['assessments'], c='purple')
    else:
        ax.plot(object_actions.index, object_actions[metric], c=institution_colour)

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Activity')

    plt.tight_layout()
    return fig


def analyze_time_series(df, name, metric):
    object_actions, institution_colour = course_or_institution_timeline(df, name)

    lag_acf = 30
    lag_pacf = 30
    f, ax = plt.subplots(nrows=2, ncols=1)
    plot_acf(object_actions[metric], lags=lag_acf, ax=ax[0])
    plot_pacf(object_actions[metric], lags=lag_pacf, ax=ax[1], method='ols')
    plt.tight_layout()
    return f