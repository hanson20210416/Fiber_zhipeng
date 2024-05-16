#imports
import pandas as pd
from parsers.processing_data import *
from extra.boxplot_randomly import select_random_days
from bokeh.models import Band, ColumnDataSource
from bokeh.plotting import figure, show

# Create some random data
df, _ = data_processing() 
df = df.loc[df['ID'] == id]

if id == 1:
    baseline_dates = pd.date_range(start='2024-01-29', periods=8)
    control_dates = select_random_days(df, '2024-02-14', '2024-03-18', 8)
else:
    baseline_dates = pd.date_range(start='2024-01-08', periods=14)
    control_dates = select_random_days(df, '2024-01-22', '2024-03-05', 14)
    
# Filter data for baseline and control periods
baseline_data = df[df['Date'].isin(baseline_dates)]
control_data = df[df['Date'].isin(control_dates)]
vars = df.column()[1:]
for var in vars:
    df = pd.DataFrame(data=dict(x=df['Date'], y=df[var])).sort_values(by="x")

    df2 = df.y.rolling(window=300).agg({"y_mean": "mean", "y_std": "std"})

    df = pd.concat([df, df2], axis=1)
    df["lower"] = df.y_mean - df.y_std
    df["upper"] = df.y_mean + df.y_std

    source = ColumnDataSource(df.reset_index())

    p = figure(tools="", toolbar_location=None, x_range=(40, 160))
    p.title.text = "Rolling Standard Deviation"
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5

    p.scatter(x="x", y="y", color="blue", marker="dot", size=10, alpha=0.4, source=source)

    p.line("x", "y_mean", line_dash=(10, 7), line_width=2, source=source)

    band = Band(base="x", lower="lower", upper="upper", source=source,
                fill_alpha=0.3, fill_color="yellow", line_color="black")
    p.add_layout(band)

    show(p)
