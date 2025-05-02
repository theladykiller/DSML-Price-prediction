import pandas as pd
import plotly.graph_objects as go

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
    
    # Wenn binäre Daten vorliegen, erstelle Balkendiagramm statt Boxplot
    if layout_settings['is_binary']:
        for idx, (category, stat) in enumerate(zip(cost_categories, stats)):
            # Berechne den Anteil der "Yes"-Werte (1-Werte)
            yes_proportion = (stat['values'] == 1).mean()
            no_proportion = 1 - yes_proportion
            
            # Füge Balken für "No" und "Yes" hinzu
            fig.add_trace(go.Bar(
                x=[category],
                y=[no_proportion],
                name='No',
                offsetgroup=category,
                marker_color='lightgray'
            ))
            fig.add_trace(go.Bar(
                x=[category],
                y=[yes_proportion],
                name='Yes',
                offsetgroup=category,
                marker_color=palette[category]
            ))
            mean_values.append(yes_proportion)
    else:
        # Für nicht-binäre Daten den ursprünglichen Boxplot beibehalten
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
        yaxis_title='Proportion' if layout_settings['is_binary'] else 'Value',
        xaxis_title='',
        showlegend=True,
        legend_title='Legend'
    )
    if layout_settings['is_binary']:
        fig.update_layout(
            yaxis=dict(
                range=[0, 1],
                tickformat=',.0%'
            ),
            barmode='stack'
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