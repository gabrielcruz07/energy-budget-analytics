import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import calendar

def build_annual_comparison_chart(df_annual: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing predicted vs. realized annual targets by category."""
    df_melted = df_annual.melt(
        id_vars=["category"],
        value_vars=["predicted_total_year","realized_total_year"],
        var_name="Metric",
        value_name="Value (R$)",
    )
    df_melted["Metric"] = df_melted["Metric"].replace(
        {"predicted_total_year": "Predicted", "realized_total_year": "Realized"})

    fig = px.bar(
        df_melted,
        x="category",
        y="Value(R$)",
        color="Metric",
        barmode="group",
        text_auto=".2s",
        color_discrete_map={"Predicted": "#636EFA", "Realized": "#00CC96"}
    )
    fig.update_layout(margin=dict(t=20,b=20,l=0,))
    return fig

def build_monthly_evolution_chart(df_monthly: pd.DataFrame) -> go.Figure:
    """Line chart showing monthly predicted vs. realized trajectory."""
    monthly_grouped = (
        df_monthly.groupby(["month_number"],as_index=False)[
            ["predicted_month","realized_month"]
        ]
        .sum()
        .sortvalues("month_number")
    )

    monthly_grouped["month_label"] = monthly_grouped["month_number"].apply(
        lambda m: calendar.month_abbr[int(m)]
    )
    monthly_grouped = monthly_grouped.rename(
        columns={"predicted_month": "Predicted", "realized_month": "Realized"}
    )

    fig = px.line(
        monthly_grouped,
        x="month_label",
        y="Predicted,Realized",
        markers=True,
        labels={"value": "Value (R$)","month_label":"Month","variable":"Metric"},
        color_discrete_map={"Predicted": "#636EFA", "Realized": "#00CC96"}
    )
    fig.update_layout(margin=dict(t=20,b=20,l=0,r=0))
    return fig

def build_seller_ranking_chart(df_sellers: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart ranking sellers by average completion percentage."""
    seller_ranking = (
        df_sellers.groupby("seller_name",as_index=False)["completion_percentage"]
        .mean()
        .sort_values("completion_percentage",ascending=True)
    )

    fig  = px.bar(
        seller_ranking,
        x="completion_percentage",
        y="seller_name",
        orientation="h",
        text_auto=".1f",
        labels={"completion_percentage":"Average Completion %","seller_name":"Seller"},
        color="completion_percentage",
        color_continuous_scale="Tealgrn"
    )
    fig.update_layout(margin=dict(t=20,b=20,l=0,r=0),coloraxis_showscale=False)
    return fig