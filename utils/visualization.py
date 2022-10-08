from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from utils import change_province,change_json
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import geopandas as gpd
import plotly.express as px
import folium


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


def get_chart_map(dataset, target, title, source):
    file_geo = 'dataset/Indonesia/BATAS_PROVINSI_DESEMBER_2019_DUKCAPIL.shp'
    df_geo = gpd.read_file(file_geo)
    df_geo = change_province(df_geo)

    data = pd.merge(df_geo, dataset, on=["Provinsi"])

    # Create variables that will be used in some parameters later
    values = int(target)
    values2 = title

    # Create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(35, 10))

    # Set the value range for the choropleth map
    vmin, vmax = data[values].min(), data[values].max()

    # Remove the axis as we do not need it
    ax.axis('off')

    # Add labels
    data['coords'] = data['geometry'].apply(lambda x: x.representative_point().coords[:])
    data['coords'] = [coords[0] for coords in data['coords']]
    for idx, row in data.iterrows():
        ann = row['Provinsi']
        ann += '\n'
        ann += str(row[values])
        plt.annotate(text=ann,
                     fontsize=3,
                     xy=row['coords'],
                     horizontalalignment='center')

    # Add a map title
    title = '{}'.format(values2)
    ax.set_title(title, fontdict={'fontsize': '20',
                                  'fontweight': '10'})

    # Create an annotation for the data source
    ax.annotate(str('Source: ' + source), xy=(0.1, .08),
                xycoords='figure fraction',
                horizontalalignment='left',
                verticalalignment='top', fontsize=12, fontweight='bold', color='k')

    # Generate the map
    data.plot(column=values, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8',
              norm=plt.Normalize(vmin=vmin, vmax=vmax), legend=True)

    return fig, ax


def get_folium_map(dataset, target):
    file_geo = r"C:\Users\Nanda\Downloads\Dataset\Indonesia_SHP.json"
    df_geo = gpd.read_file(file_geo)
    df_geo = change_province(df_geo)

    df_merged = pd.merge(df_geo, dataset, on=["Provinsi"])

    # Create a map object for choropleth map
    map_indo = folium.Map(location=[-2.49607, 117.89587],
                          tiles='OpenStreetMap',
                          zoom_start=5)

    # Set up Choropleth map object with key on Province
    folium.Choropleth(geo_data=df_merged,
                      data=df_merged,
                      columns=['Provinsi', int(target)],
                      key_on='feature.properties.Provinsi',
                      fill_color='YlOrRd',
                      fill_opacity=1,
                      line_opacity=0.2,
                      legend_name='Rate',
                      smooth_factor=0,
                      Highlight=True,
                      line_color='#0000',
                      name='Rate',
                      show=True,
                      overlay=True).add_to(map_indo)

    # Add hover functionality
    # Style function
    style_function = lambda x: {'fillColor': '#ffffff', 'color': '#000000', 'fillOpacity': 0.1, 'weight': 0.1}

    # Highlight function
    highlight_function = lambda x: {'fillColor': '#000000', 'color': '#000000', 'fillOpacity': 0.50, 'weight': 0.1}

    # Create popup tooltip object
    NIL = folium.features.GeoJson(data=df_merged,
                                  style_function=style_function,
                                  control=False,
                                  highlight_function=highlight_function,
                                  tooltip=folium.features.GeoJsonTooltip(
                                      fields=['Provinsi', str(target)],
                                      aliases=['Provinsi', 'Value'],
                                      style=('background-color: white; '
                                             'color: #333333; font-family: arial; '
                                             'font-size: 12px; padding: 10px;')))

    # Add tooltip object to the map
    map_indo.add_child(NIL)
    map_indo.keep_in_front(NIL)

    # Add dark and light mode
    # folium.TileLayer('cartodbdark_matter',
    #                  name='dark mode',
    #                  control=True).add_to(map_indo)
    # folium.TileLayer('cartodbpositron',
    #                  name='light mode',
    #                  control=True).add_to(map_indo)

    # Add a layer controller
    folium.LayerControl(collapsed=False).add_to(map_indo)

    return map_indo