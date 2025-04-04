import plotly.graph_objects as go
import numpy as np
from plotly.express.colors import sample_colorscale

from data import read_data


def generate_plot() -> None:
    """
    Generate a plot of the deadliest earthquakes by year from 2001 to 2025.
    """

    DARK_GRAY = "#404040"
    LIGHT_RED = sample_colorscale("Reds", [0.2])[0]
    MED_RED_1 = sample_colorscale("Reds", [0.45])[0]
    MED_RED_2 = sample_colorscale("Reds", [0.7])[0]
    DARK_RED = sample_colorscale("Reds", [0.95])[0]

    df = read_data()

    fig = go.Figure()

    for i in range(len(df)):
        fig.add_shape(
            type="line",
            x0=df["Year"][i],
            x1=df["Year"][i],
            y0=0,
            y1=df["Depth_km"][i],
            xref="x",
            yref="y",
            line=dict(color="gainsboro", width=2),
            layer="below",
        )
    fig.add_trace(
        go.Scatter(x=df["Year"],
                   y=df["Depth_km"],
                   mode="markers",
                   customdata=np.stack((df["EarthquakeName"],
                                        df["Fatalities"],
                                        df["Date"]), axis=-1),
                   hoverlabel=dict(
                       bgcolor="white",
                       bordercolor="rgb(0, 0, 0, 0)",
                       font=dict(color="black")),
                   hovertemplate=(
                        "<b>%{customdata[0]}</b><br>" +
                        "Fatalities: %{customdata[1]}<br>" +
                        "Depth: %{y} km<br>" +
                        "Date: %{customdata[2]}<br>" +
                        "Magnitude: %{marker.color}<extra></extra>"
                    ),
                   marker=dict(
                        size=0.15 * np.sqrt(df['Fatalities']),
                        color=df['MaxMagnitude'],
                        colorscale=[(0.00, LIGHT_RED),   (0.25, LIGHT_RED),
                                    (0.25, MED_RED_1), (0.50, MED_RED_1),
                                    (0.50, MED_RED_2),  (0.75, MED_RED_2),
                                    (0.75, DARK_RED),  (1.00, DARK_RED)],
                        opacity=1.0,
                        showscale=True,
                        sizemode='diameter',
                        sizemin=4,
                        cmin=6,
                        cmax=10,
                        colorbar=dict(
                            orientation="h",
                            x=0.5,
                            y=0.35,
                            xanchor="left",
                            len=0.4,
                            thickness=10,
                            tickfont=dict(
                                    color=DARK_GRAY,
                                    size=12),
                            title=dict(
                                text="Magnitude",
                                side="top",
                                font=dict(size=14,
                                          color=DARK_GRAY)),
                            outlinewidth=0)),
                   line=dict(
                        color="gainsboro",
                        width=5)))

    for yval in ([10, 20, 30, 40, 50, 60, 70, 80, 90]):
        fig.add_annotation(
            xref="x",
            yref="y",
            x=1999.75,
            y=yval - 2.25,
            text=str(yval) + " km",
            showarrow=False,
            align="left",
            font=dict(size=12,
                      color=DARK_GRAY,
                      weight=600),)

    fig.update_layout(
        width=1000, height=500, plot_bgcolor="white",
        yaxis=dict(range=[0, 90],
                   title=dict(text="Depth",
                              font=dict(size=14,
                                        color=DARK_GRAY,
                                        weight=600)),
                   ticks="",
                   ticklen=0,
                   autorange="reversed",
                   showticklabels=False,
                   zeroline=True,
                   zerolinewidth=2,
                   showgrid=True,
                   zerolinecolor="gainsboro",
                   gridcolor="gainsboro",
                   gridwidth=1,
                   griddash="solid",
                   tickfont=dict(size=12,
                                 color=DARK_GRAY,
                                 weight=600)),
        xaxis=dict(range=[1999, 2026],
                   side="top",
                   tickangle=315,
                   tickvals=[year for year in range(2001, 2026)],
                   ticks="inside",
                   tickwidth=0,
                   ticklen=0,
                   zeroline=False,
                   showgrid=False,
                   tickfont=dict(size=12,
                                 color=DARK_GRAY,
                                 weight=600)),
        showlegend=False,
        margin=dict(l=20, r=20, t=85, b=10)
    )

    images = []
    for i in range(len(df)):
        images.append(
            dict(
                source=f"https://flagcdn.com/w320/{df['FlagCode'][i]}.png",
                xref="x",
                yref="y",
                x=df["Year"][i] + 0.1,
                y=2,
                sizex=1,
                sizey=2.5,
                xanchor="left",
                yanchor="middle",
                layer="above"
                )
        )
    fig.update_layout(images=images)

    fig.add_annotation(
        text="<b>Deadliest Earthquakes by Year, 2001 - 2025</b>",
        x=-0.03, y=1.16, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/Lists_of_21st-century_"
        + "earthquakes'>Wikipedia</a>",
        x=2026, y=87.75, showarrow=False,
        xref="x", yref="y", align="center", xanchor="right",
        font={"color": DARK_GRAY, "size": 11})

    fig.write_html("reports/html/earthquakes.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image("reports/figures/earthquakes.png")


if __name__ == "__main__":
    generate_plot()
