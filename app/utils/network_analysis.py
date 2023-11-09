import pandas as pd
import matplotlib.colors as cls
import plotly.graph_objects as go


def get_network(df):
    color_df = pd.DataFrame({
        'Institution': df['Institution'].unique(),
        'color': ['yellow', 'blue', 'red', 'green']
    })
    color_df = color_df.merge(df[['Course', 'Institution']].drop_duplicates(), how='left')

    df_obj = (df
              .groupby(['Course', 'object.definition.type'])['object.definition.type']
              .count()
              .unstack(fill_value=0)
              .stack()
              .reset_index()
              .rename(columns={0: 'count'}))

    df_obj_merged = df_obj.merge(color_df[['Course', 'color']], how='left')

    unique_source_target = list(pd.unique(df_obj_merged[['Course', 'object.definition.type']].values.ravel('k')))

    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}

    links = pd.DataFrame()
    links['source'] = df_obj_merged['Course'].map(mapping_dict)
    links['target'] = df_obj_merged['object.definition.type'].map(mapping_dict)
    links['value'] = df_obj_merged['count']

    color_df['Course'] = color_df['Course'].map(mapping_dict)

    links = links.to_dict(orient='list')

    fig = go.Figure(data=[go.Sankey(
        textfont=dict(color="rgba(0,0,0,1)", size=13),
        node=dict(
            pad=10,
            thickness=15,
            label=unique_source_target,
            color=[cls.to_hex(cls.to_rgba(color_df[color_df['Course'] == i].iloc[0]['color'])) for i in range(8)]
        ),
        link=dict(
            source=links['source'],
            target=links['target'],
            value=links['value'],
            color='lightgray'
        ),
    )
    ])

    fig.update_layout(
        title='Number of interactions per course',
        autosize=False,
        width=1000,
        height=800,
        hovermode='x'
    )

    df_obj = df_obj.rename(columns={'object.definition.type': 'Interaction with'})

    return fig, df_obj
