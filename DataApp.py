from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas as pd

df = pd.read_csv("results9_10_26.csv")

#gnatt chart creation
fig = go.Figure()

for _, row in df.iterrows():
    fig.add_trace(
        go.Bar(
            y=[str(row["PID"])],
            x=[row["Completion Time"] - row["Start Time"]],
            base=row["Start Time"],
            orientation = "h",
            text=str(row["PID"]),
            hovertemplate = (
                "PID: %{text}<br>"
                "Start: %{base}<br>"
                "Finish: %{base+x}<extra></extra>"
            ),
            showlegend = False
        )
    )
fig.update_layout(
    title = "Shortest Job First Gnatt Chart",
    xaxis_title = "Time",
    yaxis_title="PID",
    barmode = "overlay",
    height = 700
)

#puts first process at top
fig.update_yaxes(autorange="reversed")


app = Dash()

app.layout = html.Div([
    #Data table
    html.H1('Shortest Job First'),
    dag.AgGrid(
        rowData= df.to_dict('records'),
        columnDefs=[{"field" : i} for i in df.columns],
        style = {"height":"400px"},
    ),

    #Gnatt chart
    dcc.Graph(figure=fig)
])


if __name__ == '__main__':
    app.run(debug=True)