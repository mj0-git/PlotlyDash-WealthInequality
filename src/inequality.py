import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime


def plot_wealth(df_share, df_networth):
# Create Plots: 1. Share of Wealth by Percentiles
#               2. Change in Total Net Worth Held
#               3. Effective Federal Funds Rate
#               4. Balance Sheet
# Input: df, df_networth
# Return: fig_wealth
 
    # Share of Wealth by Percentiles Plot
    fig_wealth = go.Figure()
    col = ["Top 1%","90th to 99th ", "50th to 90th", "Bottom 50%"]
    agg_date = df_networth["date"].iloc[0]
    fig_wealth = make_subplots(rows=2, cols=2,shared_xaxes=True,
                    vertical_spacing=0.05, horizontal_spacing = 0.02, row_width=[0.2, 0.8], 
                    column_widths=[0.7, 0.3], 
                    subplot_titles=(None, " Change in Total Net Worth Held - Millions <br><sup> (" +str(datetime.strftime(agg_date,'%b %Y')) + " = 0) </sup>", "Effective Federal Funds Rate", "Balance Sheet"))
    fig_wealth.add_trace(go.Scatter(x=df_share.date, y=df_share[col[2]], fill='tonexty',line_color='#338498', name=col[2]), row=1, col=1)
    fig_wealth.add_trace(go.Scatter(x=df_share.date, y=df_share[col[1]], fill='tonexty', line_color='red', name=col[1]), row=1, col=1)
    fig_wealth.add_trace(go.Scatter(x=df_share.date, y=df_share[col[3]], opacity=1, fill='tozeroy',line_color='#562287',name=col[3]), row=1, col=1 ) 
    fig_wealth.add_trace(go.Scatter(x=df_share.date, y=df_share[col[0]], fill='tonexty',line_color='#F3FF2C',name=col[0]), row=1, col=1)
    fig_wealth.update_yaxes(title_text="Share of Wealth", row=1, col=1)

    # Federal Funds Rate Plot
    fig_wealth.add_trace(go.Scatter(x=df_share.date, y=df_share["EFFR"], line_color='black',name="Effective Federal Funds Rate", mode='lines+markers',showlegend=False), row=2, col=1) 
    fig_wealth.update_yaxes(title_text="EFF Rate", row=2, col=1, tickformat="0%")
    

    # Highlight Covid via Rect
    if('2020' in df_share.date):
        fig_wealth.add_vrect(x0="2020-02-01", x1="2020-04-01", 
                annotation_text="COVID-19 Recession", annotation_position="right", annotation_textangle=-90,
                fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=1, col=1)
        fig_wealth.add_vrect(x0="2020-02-01", x1="2020-04-01", 
                annotation_text="", annotation_position="right", annotation_textangle=-90,
                fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=2, col=1)
              
    # Highlight GFC via Rect
    if('2008' in df_share.date):
        fig_wealth.add_vrect(x0="2007-12-01", x1="2009-06-01", 
            annotation_text="Great Recession", annotation_x ="2008-10-01", annotation_position="right", annotation_textangle=-90,
            fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=1, col=1)
        fig_wealth.add_vrect(x0="2007-12-01", x1="2009-06-01", 
            annotation_text="", annotation_position="right",
            fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=2, col=1)

    # Highlight Dotcom via Rectxx
    if('2001' in df_share.date):
        fig_wealth.add_vrect(x0="2001-03-01", x1="2001-11-01", 
            annotation_text="Dot-com Bubble", annotation_position="left", annotation_textangle=-90,
            fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=1, col=1)
        fig_wealth.add_vrect(x0="2001-03-01", x1="2001-11-01", 
            annotation_text="", annotation_position="left", annotation_textangle=-90,
            fillcolor="#eeeee4", opacity=0.4, line_width=1,line_dash="dash", row=2, col=1)
    

    # Change in Total Net Worth Held Plot
    fig_wealth.add_trace(go.Scatter(
        x=df_networth.date, y=df_networth["Top 1%"], name='Top 1%', showlegend=False, marker_color = "#f3ff2c"
    ),row=1, col=2)
    fig_wealth.add_trace(go.Scatter(
        x=df_networth.date, y=df_networth["90th to 99th "], name='90th to 99th', showlegend=False, marker_color = "red"
    ), row=1, col=2)
    fig_wealth.add_trace(go.Scatter(
        x=df_networth.date, y=df_networth["50th to 90th"], name='50th to 90th', showlegend=False, marker_color = "#338498"
    ),row=1, col=2)
    fig_wealth.add_trace(go.Scatter(
        x=df_networth.date, y=df_networth["Bottom 50%"], name='Bottom 50%', showlegend=False, marker_color = "#562287"
    ),row=1, col=2)
    
    # Balance Sheet Plot
    fig_wealth.add_trace(go.Scatter(
        x=df_networth.date, y=df_networth["balance_sheet"], name='Balance Sheet', showlegend=False, line_color='black',
    ),row=2, col=2)
    

    # Update Figure Properties
    fig_wealth.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            height=700, title_text="Share of Wealth by Percentiles",yaxis=dict(tickformat=".00%") )
    
    return (fig_wealth)


def plot_economy(df_economy):
# Create Plot: Financial vs Real Economy
# Input: df_economy, df_economy_qtr
# Return: fig_economy

    fig_economy =  go.Figure()

    fig_financial = make_subplots(rows=2, cols=1,shared_xaxes=True,
                    vertical_spacing=0.05, horizontal_spacing = 0.02, 
                    row_width=[0.3,0.7])

    # Real GDP line plot
    fig_economy.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["gdp"], name='Real GDP', marker_color='#562287'
    ))
     # CSI bar plot
    fig_economy.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["consumer_sentiment"], name='Consumer Sentiement Index', marker_color='indianred'
    ))
    # Industrial Production bar plot
    fig_economy.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["industrial"], name='Industrial Production', marker_color='blue'
    ))


    # CPI Purchasing Power of USD bar plot
    fig_financial.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["purchase_power"], name='Purchasing Power of USD', marker_color='green'
    ))
    # S&P 500 bar plot
    fig_financial.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["sp500"], name='S&P 500', marker_color='lightsalmon'
    ),row=1, col=1)
    # Median Sales of Houses line plot
    fig_financial.add_trace(go.Bar(
        x=df_economy.date, y=df_economy["median_house"], name='Median Sales Price of Houses', marker_color='#338498'
    ),row=1, col=1)

    # Balance Sheet
    fig_financial.add_trace(go.Scatter(
        x=df_economy.date, y=df_economy["debt_held_fed"], name='Debt Held by Federal Reserve', opacity=1, fill='tozeroy', line_color='red'
    ),row=2, col=1)
   
    # Highlight Covid via Rect
    if('2020' in df_economy.date):
        fig_economy.add_vrect(x0="2020-02-01", x1="2020-04-01", 
                annotation_text="", annotation_position="right", annotation_textangle=-90,
                fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")
    if('2020' in df_economy.date):
        fig_financial.add_vrect(x0="2020-02-01", x1="2020-04-01", 
                annotation_text="", annotation_position="right", annotation_textangle=-90,
                fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")
              
    # Highlight GFC via Rect
    if('2008' in df_economy.date):
        fig_economy.add_vrect(x0="2007-12-01", x1="2009-06-01", 
            annotation_text="", annotation_position="right",
            fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")
    if('2008' in df_economy.date):
        fig_financial.add_vrect(x0="2007-12-01", x1="2009-06-01", 
            annotation_text="", annotation_position="right",
            fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")

    # Highlight Dotcom via Rect
    if('2001' in df_economy.date):
        fig_economy.add_vrect(x0="2001-03-01", x1="2001-11-01", 
            annotation_text="", annotation_position="left", annotation_textangle=-90,
            fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")
    if('2001' in df_economy.date):
         fig_financial.add_vrect(x0="2001-03-01", x1="2001-11-01", 
            annotation_text="", annotation_position="left", annotation_textangle=-90,
            fillcolor="#eeeee4", opacity=0.3, line_width=1,line_dash="dash")

    # Update Figure Properties
    agg_date = df_economy["date"].iloc[0]
    fig_economy.update_layout(barmode='group', 
            height=400,title_text="Real Economy", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    fig_economy.update_yaxes(title_text="Index <br><sup>(" + str(datetime.strftime(agg_date,'%b %Y')) + " = 0 )</sup>")
    fig_economy.add_hline(y=0)
    fig_economy.add_vline(x=agg_date, opacity=0.7, line_width=1)

    fig_financial.update_layout(barmode='group',title_text="Financial Economy", xaxis_tickangle=-45, 
            height=600, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    fig_financial.update_yaxes(title_text="Index <br><sup>(" + str(datetime.strftime(agg_date,'%b %Y')) + " = 0 )</sup>")
    fig_financial.add_hline(y=0)
    fig_financial.add_vline(x=agg_date, opacity=0.7, line_width=1)

    return fig_economy, fig_financial

def index_data(data):
    data = np.asarray(data)
    r = np.append(1, data[1:] / data[:-1])
    return r.cumprod() * 100

# Load share of wealth csv
df_s = pd.read_csv("src/wealth_share.csv")
df_s.date = pd.to_datetime(df_s.date)
df_s = df_s.set_index('date')

# Load change in total net worth held csv
df_h = pd.read_csv("src/wealth_held.csv")
df_h.date = pd.to_datetime(df_h.date)
df_h = df_h.set_index('date')

# Load finanical and real economy csv
df_ec = pd.read_csv("src/economy.csv")
df_ec.date = pd.to_datetime(df_ec.date)
df_ec = df_ec.set_index('date')



r = list(range(2000, 2022,1))
mark = {i: {"label": str(i), "style": {"transform": "rotate(45deg)"}} for i in r}

# Dash web app
app = Dash(__name__)

# Configure UI 
app.layout = html.Div([
    html.Div([
        html.Pre(children= "Wealth Inequality in the United States",
        style={"text-align": "center", 'margin-bottom':0, 'font-family':'sans-serif', "font-size":"30px", "color":"black"}),
    ]),
    html.Div(
            [html.Pre(id='output-container-range-slider',
            style={"text-align": "center", 'font-family':'sans-serif', "font-size":"14px", "color":"black"}),
            dcc.RangeSlider(
                min=2000,
                max=2021,
                step=None,
                marks=mark,
                value=[2000, 2021],
                id='my-range-slider'
            )
    ], style={'margin': "auto", 'width':'600px', "text-align": "center"}),    
    html.Div([dcc.Graph(
        id='wealth',
    )], style={} ),
    html.Div([dcc.Graph(
        id='economy',
    )], style={'margin': "right",} ),
    html.Div([dcc.Graph(
        id='financial',
    )], style={'margin-top': "-50px",} ),

])
@app.callback(
    [ Output('output-container-range-slider', 'children'), Output('economy', 'figure'), Output('wealth', 'figure'), Output('financial', 'figure')],
    [Input('my-range-slider', 'value')])


def update_output(value):
    min_date = str(min(value))
    max_date = str(max(value))

    df_share = df_s[min_date:max_date].copy()
    df_share["date"] = df_share.index 
    df_share[["Top 1%","90th to 99th ", "50th to 90th", "Bottom 50%", "EFFR"]] = df_share[["Top 1%","90th to 99th ", "50th to 90th", "Bottom 50%", "EFFR"]]/100 # Reflect percentage
    
    df_networth = df_h[min_date:max_date].copy()
    df_networth = df_networth.assign(**df_networth.apply(index_data))
    df_networth["date"] = df_networth.index 
    df_networth[["Top 1%","90th to 99th ", "50th to 90th", "Bottom 50%", "balance_sheet"]] = df_networth[["Top 1%","90th to 99th ", "50th to 90th", "Bottom 50%", "balance_sheet"]] - 100 # Set index to 0
    
    df_economy = df_ec[min_date:max_date].copy()
    df_economy = df_economy.assign(**df_economy.apply(index_data))
    df_economy["date"] = df_economy.index 
    df_economy[["sp500", "consumer_sentiment", "purchase_power","industrial","debt_held_fed", "median_house", "gdp"]] = df_economy[["sp500", "consumer_sentiment", "purchase_power","industrial","debt_held_fed", "median_house", "gdp"]] - 100 # Set index to 0

    # Plot Wealth
    fig_wealth = plot_wealth(df_share.copy(), df_networth.copy())
    
    # Plot Financial and Real Economy
    fig_economy, fig_financial = plot_economy(df_economy)

    date_select = "(" + min_date +" - " + max_date +")"
    return date_select, fig_economy,  fig_wealth, fig_financial

if __name__ == '__main__':
    app.run_server(debug=True)

