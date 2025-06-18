import pandas as pd
import plotly.graph_objects as go

from PlotCreation.constants import cost_labels, cost_categories,palette

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
       # Precompute unique values for all columns
        unique_values_cache = {}
        for column in data.columns[:-2]:
            unique_values_cache[column] = data[column].dropna().unique()
        
        for column in data.columns[:-2]:  # Exclude 'target' and 'target_label' columns
            fig = go.Figure()
            
            #Use precomputed unique values
            unique_values = unique_values_cache[column]
            is_binary = set(unique_values).issubset({0, 1})
            
            for label in cost_categories:
                mask = data['target_label'] == label
                fig.add_trace(go.Histogram(
                    x=data[mask][column],
                    name=label,
                    marker_color=palette[label],
                ))
            
            # Optimize layout settings
            if is_binary:
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