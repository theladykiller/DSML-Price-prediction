"""
Report: Mobile Price Prediction - Full Workflow
This script documents the analysis from data loading, plotting to prediction.
"""

# --- 1. Setup ---
import pandas as pd
import plotly.io as pio
from HelperMethods.fileRead import file_read
from HelperMethods.dataScale import data_scale
from PlotCreation.barPlot import bar_plot
from PlotCreation.regressionCurvePlot import regression_curve_plot
from PlotCreation.highToLowEndPlot import low_to_high_end_plot
from model import knn_predict
from PlotCreation.constants import cost_labels
import webbrowser

# ---1. Render mode: HTML output for browser
pio.renderers.default = "browser"

import os

def save_figures_to_html(figures, filename, title):
    os.makedirs("Plots", exist_ok=True)
    path = os.path.join("Plots", filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"<html><head><title>{title}</title></head><body>\n")
        f.write(f"<h1 style='text-align:center'>{title}</h1>\n")
        for fig in figures:
            inner = pio.to_html(fig, include_plotlyjs='cdn', full_html=False)
            f.write(inner + "<hr>\n")
        f.write("</body></html>")
    webbrowser.open(path)

def save_knn_results_to_html(details, filename, title):
    os.makedirs("Plots", exist_ok=True)
    path = os.path.join("Plots", filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"<html><head><title>{title}</title></head><body>\n")
        f.write(f"<h1 style='text-align:center'>{title}</h1>\n")
        f.write("<ul style='font-family:Arial; font-size:16px;'>\n")
        for d in details:
            label = cost_labels[d['predicted_price']]
            dist = f"{d['avg_distance']:.2f}"
            f.write(f"<li>Test Point {d['test_point']}: <b>{label}</b> (Avg. Distance: {dist})</li>\n")
        f.write("</ul></body></html>")
    webbrowser.open(path)

# --- 2. Load and Preprocess Data ---
print("Loading and scaling data...")
x_train, y_train, x_test = file_read()
x_train = x_train.astype(float)
y_train = y_train.astype(int)
x_test = x_test.astype(float)
x_train_scaled, x_test_scaled = data_scale(x_train, x_test)
print("Data loaded successfully. Shapes:")
print("x_train:", x_train.shape, "| y_train:", y_train.shape, "| x_test:", x_test.shape)

# --- 3. Plotting: Distribution of Features by Price Class ---
print("\nGenerating bar plots...")
bar_figures = bar_plot(x_train, y_train, use_plotly=True)
save_figures_to_html(bar_figures, "bar_plots.html", "Feature Distribution")
print("Bar plots reveal how each feature is distributed across price classes.")

# --- 4. Plotting: Regression Curve Plots ---
print("\nGenerating regression curve plots...")
regression_figures = regression_curve_plot(x_train, y_train, use_plotly=True)
save_figures_to_html(regression_figures, "regression_plots.html", "Feature-Price Regression")
print("Regression plots help us understand feature trends across price ranges.")

# --- 5. Plotting: Low-End to High-End Positioning ---
print("\nGenerating low-to-high-end feature average plot...")
highlow_figures = low_to_high_end_plot(x_train_scaled, y_train, use_plotly=True)
save_figures_to_html(highlow_figures, "highlow_plots.html", "Low-End to High-End Analysis")
print("This plot shows how the average feature values correspond to phone pricing tiers.")

# --- 6. KNN Prediction ---
k = 5
print(f"\nRunning KNN prediction with k={k}...")
predictions, details = knn_predict(x_train_scaled, y_train, x_test_scaled, k)
save_knn_results_to_html(details, "knn_predictions.html", f"KNN Predictions with k = {k}")

print("\nKNN classification complete.")
print(f"Total test points classified: {len(predictions)}")