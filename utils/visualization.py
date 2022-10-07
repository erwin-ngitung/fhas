from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt


def interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df,
        enableRowGroup=True,
        enableValue=True,
        enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


def get_chart_line(data, x_label, y_label, title):
    hover = alt.selection_single(
        fields=[x_label],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x=x_label,
            y=y_label,
            color="symbol",
            strokeDash="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x_label,
            y=y_label,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x_label, title=x_label),
                alt.Tooltip(y_label, title=y_label),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


def get_bar_horizontal(data, x_label, title):
    chart_data = pd.melt(data, id_vars=["Provinsi"])

    hover = alt.selection_single(
        fields=[x_label],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Horizontal stacked bar chart
    chart = (
        alt.Chart(chart_data,
                  title=title,
                  width=700,
                  height=400)
        .mark_bar()
        .encode(
            x=alt.X(x_label, type="nominal", title=x_label),
            y=alt.Y("value", type="quantitative", title="Value"),
            color=alt.Color("variable", type="nominal", title=""),
            order=alt.Order("variable", sort="descending"),
        )
    )

    tooltips = (
        alt.Chart(chart_data)
        .mark_rule()
        .encode(
            x=x_label,
            y="value",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0.3)),
            tooltip=[
                alt.Tooltip(x_label, title=x_label),
                alt.Tooltip("value", title="value"),
            ],
        )
        .add_selection(hover)
    )

    return chart.interactive()


def get_bar_vertical(data, y_label, title):
    chart_data = pd.melt(data, id_vars=["Provinsi"])

    hover = alt.selection_single(
        fields=[y_label],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Horizontal stacked bar chart
    chart = (
        alt.Chart(chart_data,
                  title=title,
                  width=700)
        .mark_bar()
        .encode(
            x=alt.X("value", type="quantitative", title="Value"),
            y=alt.Y(y_label, type="nominal", title="Province"),
            color=alt.Color("variable", type="nominal", title=""),
            order=alt.Order("variable", sort="descending"),
        )
    )

    tooltips = (
        alt.Chart(chart_data)
        .mark_rule()
        .encode(
            x="value",
            y=y_label,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0.3)),
            tooltip=[
                alt.Tooltip("value", title="value"),
                alt.Tooltip(y_label, title=y_label),
            ],
        )
        .add_selection(hover)
    )

    return chart.interactive()

