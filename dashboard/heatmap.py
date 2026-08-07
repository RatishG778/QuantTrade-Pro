import streamlit as st

from research.optimization.heatmap import HeatmapBuilder


def heatmap_page():

    builder = HeatmapBuilder()

    table = builder.moving_average()

    st.subheader("🔥 Parameter Heatmap")

    if table.empty:

        st.info("Run optimizer first.")

        return

    st.dataframe(
        table,
        use_container_width=True
    )