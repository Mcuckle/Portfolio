import streamlit as st


def render_sidebar_nav():
    """Renders a clean, mission-control style sidebar navigation."""
    st.sidebar.markdown("### 🚀 CONNOR PUNSHON")
    st.sidebar.caption("Space Scientist & Systems Engineer")
    st.sidebar.markdown("---")

    # Navigation radio menu
    selection = st.sidebar.radio(
        "Navigation",
        ["Home", "Projects", "About & Skills", "Resume"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Contact & Links")
    st.sidebar.markdown("[LinkedIn Profile](https://linkedin.com)")
    st.sidebar.markdown("📧 connor.space@outlook.com")

    return selection