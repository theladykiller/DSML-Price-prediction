import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from .constants import cost_labels, cost_categories,palette

def prepare_data(columns, target):
    data = pd.DataFrame(columns)
    data['target'] = target
    data['target_label'] = data['target'].map(cost_labels)
    return data

def get_layout_settings(column_data):
    """Bestimmt die Layout-Einstellungen basierend auf den Dateneigenschaften"""
    unique_values = column_data.dropna().unique()
    is_binary = set(unique_values).issubset({0, 1})
    return {
        'is_binary': is_binary,
        'y_range': [-0.1, 1.1] if is_binary else None,
        'y_ticks': (["No", "Center", "Yes"], [0, 0.5, 1]) if is_binary else None

    }
def calculate_statistics(data, column, categories):
    stats = []
    for label in categories:
        subset = data[data['target_label'] == label]
        stats.append({
            'mean': subset[column].mean(),
            'values': subset[column],
            'count': len(subset)
        })
    return stats

def create_plotly_figure(column_name, stats, layout_settings):
    fig = go.Figure()
    mean_values = []
    # Box-Plots für jede Kategorie
    for idx, (category, stat) in enumerate(zip(cost_categories, stats)):
        fig.add_trace(go.Box(
            y=stat['values'],
            name=category,
            marker_color=palette[category],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8
        ))
        mean_values.append(stat['mean'])
    # Mittelwert-Linie
    fig.add_trace(go.Scatter(
        x=cost_categories,
        y=mean_values,
        mode='lines+markers',
        name='Mean Value per Class',
        line=dict(color='black', width=2),
        marker=dict(size=8)
    ))
    # Layout anpassen
    fig.update_layout(
        title=column_name,
        yaxis_title='Value',
        xaxis_title='',
        showlegend=True,
        legend_title='Legend'
    )
    if layout_settings['is_binary']:
        fig.update_layout(
            yaxis=dict(
                range=layout_settings['y_range'],
                ticktext=layout_settings['y_ticks'][0],
                tickvals=layout_settings['y_ticks'][1]
            ),
            shapes=[dict(
                type='line',
                yref='y',
                y0=0.5,
                y1=0.5,
                xref='paper',
                x0=0,
                x1=1,
                line=dict(color='black', width=0.5)
            )]
        )
    return fig

def regression_curve_plot(columns, target, use_plotly=False):
    """Hauptfunktion für die Erstellung der Regressionsplots"""
    data = prepare_data(columns, target)
    figures = []
    for column in data.columns[:-2]:  # Exclude target and target_label columns
        layout_settings = get_layout_settings(data[column])
        stats = calculate_statistics(data, column, cost_categories)
        if use_plotly:
            fig = create_plotly_figure(column, stats, layout_settings)
            figures.append(fig)
        #else wenn ich matplotlib benutzen will
    return figures if use_plotly else None