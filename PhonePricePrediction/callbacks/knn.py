from dash import html
from dash.dependencies import Input, Output, State
from app import app
from model import knn_predict
from PlotCreation.constants import cost_labels
from sklearn.neighbors import KNeighborsClassifier
from joblib import parallel_backend

# Cache für Daten
data_cache = None

def get_cached_data():
    global data_cache
    if data_cache is None:
        from HelperMethods.fileRead import file_read
        from HelperMethods.dataScale import data_scale
        x_train, y_train, x_test = file_read()
        x_train = x_train.astype(float)
        y_train = y_train.astype(int)
        x_test = x_test.astype(float)
        x_train_scaled, x_test_scaled = data_scale(x_train, x_test)
        data_cache = (x_train_scaled, y_train, x_test_scaled)
    return data_cache

@app.callback(
    Output('prediction-results', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('k-value', 'value')]
)
def make_predictions(n_clicks, k):
    if n_clicks is None or k is None:
        return ''
    try:
        from HelperMethods.fileRead import file_read
        from HelperMethods.dataScale import data_scale
        x_train, y_train, x_test = file_read()
        x_train = x_train.astype(float)
        y_train = y_train.astype(int)
        x_test = x_test.astype(float)
        x_train_scaled, x_test_scaled = data_scale(x_train, x_test)

        predictions, details = knn_predict(x_train_scaled, y_train, x_test_scaled, k)
        
        # Gemeinsames Style für alle Header-Zellen
        header_style = {
            'textAlign': 'center', 
            'backgroundColor': 'black',
            'color': 'white', 
            'padding': '12px',
            'position': 'sticky',
            'top': '0',
            'zIndex': '1'
        }
        
        # Farben für jede Preis-Kategorie
        price_colors = {
            'Very Low Cost': '#28a745',    # Grün
            'Low Cost': '#17a2b8',         # Blau
            'High Cost': '#ffc107',        # Gelb
            'Very High Cost': '#dc3545'    # Rot
        }
        
        # Tabellen-Header mit gemeinsamem Style
        table_header = [
            html.Thead(html.Tr([
                html.Th("Test Point", style=header_style),
                html.Th("Predicted Price", style=header_style),
                html.Th("Average Distance", style=header_style)
            ]))
        ]
        
        # Tabellen-Zeilen mit farbiger Kategorisierung
        table_rows = []
        for i, d in enumerate(details[:1000]):
            # Farbe basierend auf der Preiskategorie
            price_category = cost_labels[d['predicted_price']]
            price_color = price_colors[price_category]

            bg_color = '#f8f9fa' if i % 2 == 0 else 'white'
            
            row = html.Tr([
                html.Td(f"Test Point {d['test_point']}", style={
                    'textAlign': 'center', 
                    'padding': '8px', 
                    'backgroundColor': bg_color
                }),
                html.Td(cost_labels[d['predicted_price']], style={
                    'textAlign': 'center', 
                    'padding': '8px', 
                    'fontWeight': 'bold', 
                    'backgroundColor': price_color,
                    'color': 'white',
                    'borderRadius': '4px'
                }),
                html.Td(f"{d['avg_distance']:.2f}", style={
                    'textAlign': 'center', 
                    'padding': '8px', 
                    'backgroundColor': bg_color
                })
            ])
            table_rows.append(row)
        
        #Tabelle mit Container für Scroll
        table = html.Table(
            table_header + [html.Tbody(table_rows)],
            style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'border': '1px solid #ddd',
                'fontFamily': 'Segoe UI, Arial, sans-serif',
                'fontSize': '14px'
            }
        )
        
        #Legende für die Farben
        legend_items = []
        for category, color in price_colors.items():
            legend_items.append(html.Span([
                html.Span("■", style={'color': color, 'fontSize': '20px', 'marginRight': '5px'}),
                html.Span(category, style={'marginRight': '20px', 'fontSize': '12px'})
            ]))
        
        return html.Div([
            html.H4(f'Predictions with k = {k}', style={'color': 'black', 'fontWeight': 'bold', 'marginBottom': '20px'}),
            html.Div([
                html.P(f"Total predictions: {len(details)}", style={'color': '#666', 'fontWeight': 'bold', 'fontSize': '12px', 'marginBottom': '10px'}),
                # Legende
                html.Div(legend_items, style={
                    'marginBottom': '15px', 
                    'padding': '10px', 
                    'backgroundColor': '#f8f9fa', 
                    'borderRadius': '4px',
                    'textAlign': 'center'
                }),
                # Container mit fester Höhe und Scroll
                html.Div(
                    table, 
                    style={
                        'maxHeight': '400px', 
                        'overflowY': 'auto',
                        'border': '1px solid #ddd',
                        'borderRadius': '4px'
                    }
                )
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ])
    except Exception as e:
        return html.Div([
            html.H4('Error occurred during prediction', style={'color': '#dc3545'}),
            html.P(str(e), style={'color': '#666'})
        ])

class OptimizedKNN:
    def __init__(self, n_jobs=-1):
        self.model = KNeighborsClassifier(n_jobs=n_jobs)
        
    def predict(self, x_train, y_train, x_test, k):
        self.model.n_neighbors = k
        self.model.fit(x_train, y_train)
        return self.model.predict(x_test)