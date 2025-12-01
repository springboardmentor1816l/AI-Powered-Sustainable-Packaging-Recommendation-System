# analytics utilities for BI dashboard (plotly export)
import pandas as pd
import plotly.express as px

def co2_trend(df: pd.DataFrame):
    fig = px.line(df, x="date", y="co2_saved")
    fig.write_html("docs/co2_trend.html")
    return "docs/co2_trend.html"
