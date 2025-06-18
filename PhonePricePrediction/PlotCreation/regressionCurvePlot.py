import pandas as pd
import plotly.graph_objects as go
import numpy as np

#from PlotCreation.constants import cost_labels, cost_categories,palette
from .constants import cost_labels, cost_categories, palette

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
    
    if layout_settings['is_binary']:
        yes_proportions = []
        for idx, (category, stat) in enumerate(zip(cost_categories, stats)):
            values = stat['values']
            yes_count = (values == 1).sum()
            no_count = (values == 0).sum()
            total = yes_count + no_count
            
            # Berechne relative Häufigkeiten
            yes_proportion = yes_count / total if total > 0 else 0
            no_proportion = no_count / total if total > 0 else 0
            
            # Speichere für Regression
            yes_proportions.append(yes_proportion)
            
            # Füge Balken hinzu
            fig.add_trace(go.Bar(
                x=[category],
                y=[no_proportion],
                name='No',
                marker_color='lightgray',
                offsetgroup=0
            ))
            
            fig.add_trace(go.Bar(
                x=[category],
                y=[yes_proportion],
                name='Yes',
                marker_color=palette[category],
                offsetgroup=0
            ))

        x_numeric = list(range(len(cost_categories)))

        coeffs = np.polyfit(x_numeric, yes_proportions, 1)
        trend = np.poly1d(coeffs)

        fig.add_trace(go.Scatter(
            x=cost_categories,
            y=[trend(x) for x in x_numeric],
            mode='lines',
            name='Trend',
            line=dict(color='black', width=2, dash='dash')
        ))

        fig.add_trace(go.Scatter(
            x=cost_categories,
            y=yes_proportions,
            mode='markers',
            name='Actual Yes Proportion',
            marker=dict(color='black', size=8)
        ))

    else:
        mean_values = []
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

        # Mittelwert-Linie für nicht-binäre Daten
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
        yaxis_title='Proportion' if layout_settings['is_binary'] else 'Value',
        xaxis_title='',
        showlegend=True,
        legend_title='Legend',
        barmode='stack'
    )

    if layout_settings['is_binary']:
        fig.update_layout(
            yaxis=dict(
                range=[0, 1],
                tickformat=',.0%'
            )
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