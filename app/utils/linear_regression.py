import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def regression_results(y_true, y_pred):
    explained_variance = metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)

    return ' - Explained variance (%): ' + str(round(explained_variance, 4)) + \
        '\n - R2: ' + str(round(r2, 4)) + \
        '\n - MAE: ' + str(round(mean_absolute_error, 4)) + \
        '\n - MSE: ' + str(round(mse, 4)) + \
        '\n - RMSE: ' + str(round(np.sqrt(mse), 4))


def regression(df):
    df_reg = pd.get_dummies(df['Course']).astype(int)
    df_reg = pd.concat([df_reg, pd.get_dummies(df['Teaching']).astype(int)], axis=1)
    df_reg['actor.id'] = df['actor.id']
    df_reg = df_reg.groupby('actor.id').max()
    df_object_by_actor = df.groupby('actor.id')['object.definition.type'].value_counts().unstack(
        fill_value=0).stack().reset_index()
    df_object_by_actor = pd.concat([
        pd.Series(v.values, name=k) for k, v in df_object_by_actor.groupby('object.definition.type')[0]
    ],
        axis=1
    )
    df_reg = pd.concat([df_reg, df_object_by_actor], axis=1)
    df_reg['score'] = df.groupby('actor.id')['result.score.scaled'].mean()
    df_reg = df_reg.loc[df_reg['score'].notnull()].reset_index().drop(columns=['index', 'lesson'], axis=1)

    fig1, ax = plt.subplots()
    fig1.set_figwidth(15)
    fig1.set_figheight(15)
    sns.heatmap(df_reg.corr(), annot=True, ax=ax)

    X = df_reg.drop('score', axis=1)
    y = df_reg['score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    regression_1 = LinearRegression()
    regression_1.fit(X_train, y_train)
    regression_1.score(X_train, y_train)
    coef_df = pd.DataFrame(zip(regression_1.coef_, X_train.columns))
    y_pred = regression_1.predict(X_test)

    fig2, ax = plt.subplots()

    coeff = coef_df.iloc[(coef_df[0].abs() * -1.0).argsort()]
    sns.barplot(x=coeff[0], y=coeff[1], orient='h', palette='flare', hue=coeff[0], legend=None)
    plt.xlabel('Value')
    plt.ylabel('Parameter')

    return fig1, fig2, regression_results(y_test, y_pred)
