from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas as pd


def create_gantt(df, chart_title):
    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_trace(
            go.Bar(
                y=[str(row["PID"])],
                x=[row["Completion Time"] - row["Start Time"]],
                base=row["Start Time"],
                orientation="h",
                text=str(row["PID"]),
                hovertemplate=(
                    "PID: %{text}<br>"
                    "Start: %{base}<br>"
                    "Finish: %{base+x}<extra></extra>"
                ),
                showlegend=False
            )
        )

    fig.update_layout(
        title=chart_title,
        xaxis_title="Time",
        yaxis_title="PID",
        barmode="overlay",
        height=500
    )

    fig.update_yaxes(autorange="reversed")

    return fig

# creates gantt chart and table for page using csv file
def create_section(csv_file, heading, chart_title):

    df = pd.read_csv(csv_file)

    fig = create_gantt(df, chart_title)

    return html.Div([

        html.H1(heading),

        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[
                {"field": column}
                for column in df.columns
            ],
            style={"height": "400px"}
        ),

        dcc.Graph(figure=fig),

        html.Hr()
    ])


app = Dash()

app.layout = html.Div([

        create_section(
        "CSV_FCFS.csv",
        "FIFO (Harvested)",
        "FIFO Gantt Chart (Harvested)"
    ),
    
        create_section(
        "CSV_SJF.csv",
        "Shortest Job First (Harvested)",
        "Shortest Job First Gantt Chart (Harvested)"
    ),

        create_section(
        "CSV_Priority.csv",
        "Priority (Harvested)",
        "Priority Gantt Chart (Harvested)"
        ),

        create_section(
            "CSV_RR.csv",
            "Round Robin (Harvested)",
            "Round Robin Gantt (Harvested)"
            )
])


if __name__ == "__main__":
    app.run(debug=True)