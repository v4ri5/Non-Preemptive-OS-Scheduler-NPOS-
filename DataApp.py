from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas as pd


def create_gantt(df, chart_title):
    fig = go.Figure()

    df = df.sort_values("Start Time").copy()

    # Shift entire schedule so earliest process begins at 0
    offset = df["Start Time"].min()

    df["Plot Start"] = df["Start Time"] - offset
    df["Plot Finish"] = df["Completion Time"] - offset
    df["Duration"] = df["Completion Time"] - df["Start Time"]

    for _, row in df.iterrows():
        fig.add_trace(
            go.Bar(
                y=[str(row["PID"])],
                x=[row["Duration"]],
                base=[row["Plot Start"]],
                orientation="h",

                # Make short bars easier to see
                marker_line_width=1,

                customdata=[[
                    row["Start Time"],
                    row["Completion Time"],
                    row["Duration"]
                ]],

                hovertemplate=(
                    f"<b>PID {row['PID']}</b><br>"
                    "Start: %{customdata[0]:,.000f}<br>"
                    "Finish: %{customdata[1]:,.000f}<br>"
                    "Duration: %{customdata[2]:,.000f}"
                    "<extra></extra>"
                ),

                showlegend=False
            )
        )

    fig.update_layout(
        title=chart_title,
        xaxis_title="Time",
        yaxis_title="PID",

        height=max(500, len(df) * 50),

        bargap=0.15,

        plot_bgcolor="white",

        margin=dict(
            l=80,
            r=30,
            t=70,
            b=70
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        rangemode="tozero",

        # IMPORTANT: interactive zoom slider
        rangeslider=dict(visible=True)
    )

    fig.update_yaxes(
        autorange="reversed",
        type="category",
        showgrid=False
    )

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
        "CSV_Workload.csv",
        "Workload (Real Processes)",
        "Workload Gantt Chart"
    ),
        create_section(
        "CSV_FCFS.csv",
        "FIFO (Harvested)",
        "FIFO Gantt Chart (Harvested)"
    ),

        create_section(
        "CSV_Custom_FCFS.csv",
        "FIFO (Custom)",
        "FIFO Gantt Chart (Custom)"
    ),
    
        create_section(
        "CSV_SJF.csv",
        "Shortest Job First (Harvested)",
        "Shortest Job First Gantt Chart (Harvested)"
    ),

        create_section(
        "CSV_Custom_SJF.csv",
        "Shortesst Job First (Custom)",
        "Shortest Job First (Custom)"
    ),

        create_section(
        "CSV_Priority.csv",
        "Priority (Harvested)",
        "Priority Gantt Chart (Harvested)"
    ),

        create_section(
        "CSV_Custom_Priority.csv",
        "Priority (Custom)",
        "Priority (Custom)"
    ),

        create_section(
        "CSV_RR.csv",
        "Round Robin (Harvested)",
        "Round Robin Gantt (Harvested)"
    ),
        
        create_section(
        "CSV_Custom_RR.csv",
        "Round Robin (Custom)",
        "Round Robin (Custom)"
    )
])


if __name__ == "__main__":
    app.run(debug=True)