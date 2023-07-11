"""This is a test to run the streamlit app features"""

import streamlit as st

from python_files import clustering
from python_files.test_analysis import MetricCalculator
from python_files.utils import change_delta_color
import python_files.clustering
from st_pages import show_pages_from_config, add_page_title


add_page_title()
show_pages_from_config()


""" Streamlit App """


def main():

    st.title("MetaPals Dashboard")
    st.markdown("Hello, **MetaPals Team**!, this is the place where you can see complex data :sunglasses:")

    x = 10

    # Start a metric instance
    metric_calculator = MetricCalculator()
    # Slider to modify the variable value
    st.text("Here you can modify the variable value")
    new_variable = st.slider("Select a value", -10, 10, 0)
    # Take the variable from the class
    metric_calculator.variable = new_variable

    # Calculate the metric
    metric = metric_calculator.calculate_metric()

    col1, col2, col3 = st.columns(3)
    col1.metric("Metric", metric, delta=metric, delta_color=change_delta_color(metric))
    col2.metric("Number of Users", 10, delta=x, delta_color=change_delta_color(x))
    col3.metric("Number of Events", 10, delta=x, delta_color=change_delta_color(x))

    # Clusters
    st.text("Clusters")
    st.table(clustering.polar)

    st.vega_lite_chart(clustering.polar, {
        "mark": {"type": "bar", "tooltip": True},
        "encoding": {
            "x": {"field": "variable", "type": "nominal"},
            "y": {"field": "value", "type": "quantitative"},
            "color": {"field": "label", "type": "nominal"}
        }
    })

    # Distribution of the clusters
    st.text("Distribution of the clusters")
    st.table(clustering.pie)

    st.vega_lite_chart(clustering.pie, {
        "mark": {"type": "arc", "tooltip": True},
        "encoding": {
            "theta": {"field": "value", "type": "quantitative"},
            "color": {"field": "label", "type": "nominal"}
        }
    })

if __name__ == "__main__":
    main()
