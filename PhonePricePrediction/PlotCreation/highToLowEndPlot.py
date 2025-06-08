import pandas as pd
import plotly.express as px

from PlotCreation.constants import cost_labels, cost_categories, palette

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
        fig = px.strip(
            data,
            x='mean_value',
            y='target_label',
            color='target_label',
            color_discrete_map=palette,
            stripmode='overlay'  # all points slightly jittered
        )

        fig.update_layout(
            title='Device Position from Low-End to High-End by Average Feature Value',
            yaxis_title='',
            xaxis_title='',
            showlegend=False,
            xaxis=dict(
                ticktext=["Low-End", "High-End"],
                tickvals=[0.15, 0.775],
                range=[0.125, 0.8]
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=['Very Low Cost', 'Low Cost', 'High Cost', 'Very High Cost']  # <<<< THIS LINE
            )
        )

        return [fig]
    return None
