import pandas as pd
import plotly.graph_objects as go
from .constants import cost_labels, cost_categories,palette
#import matplotlib.pyplot as plt
#import seaborn as sns


def low_to_high_end_plot(columns, target, use_plotly=False):
    # Calculate the mean value for each data point (row)
    mean_values = columns.mean(axis=1)

    # Create a DataFrame for plotting
    data = pd.DataFrame({
        'mean_value': mean_values,
        'target': target
    })

    data['target_label'] = data['target'].map(cost_labels)
    # Set the correct order
    data['target_label'] = pd.Categorical(data['target_label'], categories=cost_categories, ordered=True)

    if use_plotly:
        fig = go.Figure()

        for label in cost_categories:
            subset = data[data['target_label'] == label]
            
            fig.add_trace(go.Box(
                y=subset['mean_value'],
                name=label,
                marker_color=palette[label],
                boxpoints='all',  # zeige alle Punkte
                jitter=0.3,       # Punkte streuen
                pointpos=-1.8     # Position der Punkte
            ))

        fig.update_layout(
            title='Device Position from Low-End to High-End by Average Feature Value',
            yaxis_title='Average Feature Value',
            xaxis_title='',
            showlegend=False,
            xaxis=dict(
                ticktext=["Low-End", "High-End"],
                tickvals=[0.15, 0.775],
                range=[0.1, 0.825]
            )
        )
        return [fig]
    return None
    #else wenn ich matplotlib benutzen möchte
