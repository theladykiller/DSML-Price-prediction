from dash import html
from dash.dependencies import Input, Output, State
from app import app
from model import knn_predict
from PlotCreation.constants import cost_labels

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
        prediction_list = [
            html.P(f"Test point {d['test_point']}: {cost_labels[d['predicted_price']]} "
                   f"(Average distance: {d['avg_distance']:.2f})")
            for d in details[:1000]
        ]
        return html.Div([
            html.H4(f'Predictions with k={k}'),
            html.Div(prediction_list)
        ])
    except Exception as e:
        return html.Div([
            html.H4('Error occurred during prediction'),
            html.P(str(e))
        ])