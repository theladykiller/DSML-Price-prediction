import pandas as pd
import plotly.graph_objects as go
from .constants import cost_labels, cost_categories,palette
#from matplotlib.patches import Rectangle
#import seaborn as sns
#import matplotlib.pyplot as plt

def bar_plot(columns, target, use_plotly=False):
    # Create a DataFrame for easier manipulation
    data = pd.DataFrame(columns)
    data['target'] = target


    # Replace target values with the custom labels
    data['target_label'] = data['target'].map(cost_labels)
    # Set the correct order of categories
    data['target_label'] = pd.Categorical(data['target_label'], categories=cost_categories, ordered=True)

    if use_plotly:
        figures = []
        for column in data.columns[:-2]:  # Exclude 'target' and 'target_label' columns
            fig = go.Figure()
            
            for label in cost_categories:
                mask = data['target_label'] == label
                fig.add_trace(go.Histogram(
                    x=data[mask][column],
                    name=label,
                    marker_color=palette[label],
                ))
            # Check if the feature only contains 0 and 1
            unique_values = data[column].dropna().unique()
            if set(unique_values).issubset({0, 1}):
                fig.update_xaxes(range=[-0.1, 1.1], ticktext=["No", "Yes"], tickvals=[0, 1])
                fig.update_layout(xaxis_title='')
            else:
                fig.update_layout(xaxis_title='Value')
            fig.update_layout(
                barmode='stack',
                title=column,
                yaxis_title='Frequency',
                showlegend=True,
                legend_title='Price Range'
            )
            figures.append(fig)
        return figures

    else:
        return None
        # matplotlib/seaborn implementation