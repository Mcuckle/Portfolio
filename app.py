import streamlit as st
from components.project_loader import load_all_projects
import os
import glob
import random
import base64

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Connor Punshon | Space Scientist Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding, header, menu, and footer watermark
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 2. Modern Floating Sidebar & Professional UI Custom CSS
st.markdown("""
<style>
    /* Global dark background override */
    .stApp {
        background-color: #0b0f19 !important;
    }

    /* Ensure main content container acts as the precise coordinate anchor for centering */
    .stMainBlockContainer {
        position: relative !important;
        z-index: 1;
    }

    /* Centered Cinematic Warp Core anchored dynamically to the main content pane */
    .hyperdrive-core {
        position: absolute;
        top: 45vh;
        left: 50%;
        width: 0;
        height: 0;
        z-index: 0;
        pointer-events: none;
        overflow: visible;
    }

    /* Ultra-subtle, slow, elegant cinematic warp lines */
    .warp-line {
        position: absolute;
        top: 0;
        left: 0;
        height: 1px;
        background: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(138, 180, 248, 0.35), rgba(255, 255, 255, 0.6));
        transform-origin: left center;
        opacity: 0;
        animation: cinematicWarp cubic-bezier(0.25, 1, 0.5, 1) infinite;
    }

    @keyframes cinematicWarp {
        0% {
            transform: rotate(var(--angle)) translateX(15px) scaleX(0.05);
            opacity: 0;
        }
        25% {
            opacity: 0.25;
        }
        75% {
            opacity: 0.15;
        }
        100% {
            transform: rotate(var(--angle)) translateX(380px) scaleX(1.8);
            opacity: 0;
        }
    }

    /* Main sidebar background and padding */
    [data-testid="stSidebar"] {
        background-color: #111318;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        z-index: 10;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    /* Style Streamlit download button to match neutral card look */
    [data-testid="stSidebar"] .stDownloadButton button {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: 500 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stSidebar"] .stDownloadButton button:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
    }

    /* Hover effect for custom LinkedIn button anchor */
    .sidebar-linkedin-btn:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
    }

    /* Transform radio button options into floating cards */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 0.6rem;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.7rem 1.1rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        width: 100%;
    }

    /* Completely hide Streamlit's native radio circles, inputs, and pseudo-elements */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] input,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] svg,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] div[class*="st-key"],
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] span {
        display: none !important;
    }

    /* Target the inner container of the radio label to remove flex spacing gaps for the dot */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {
        display: contents !important;
    }

    /* Hover effect for floating cards */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
    }

    /* Active/Selected card style with vibrant modern gradient and glowing highlight */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(10, 132, 255, 0.25), rgba(94, 92, 230, 0.25));
        border-color: #0a84ff;
        box-shadow: 0 4px 20px rgba(10, 132, 255, 0.35);
    }

    /* Make active text bright white and crisp */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] p,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Enforce uniform image container height and object fitting for certificates */
    .cert-image-container img {
        height: 420px !important;
        object-fit: contain !important;
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Enforce identical fixed-size container boxes for all skill/tool logos */
    .logo-card-img {
        width: 100% !important;
        height: 110px !important;
        object-fit: contain !important;
        padding: 8px !important;
    }

    /* --- STICKY EXPANDER HEADER FOR SEAMLESS ACCESSIBILITY --- */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.01) !important;
    }

    [data-testid="stExpander"] summary {
        position: sticky !important;
        top: 3.5rem !important;
        z-index: 999 !important;
        background-color: #111420 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        border: 1px solid rgba(10, 132, 255, 0.3) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
    }

    [data-testid="stExpander"] summary:hover {
        border-color: #0a84ff !important;
        background-color: #161b2e !important;
    }
</style>
""", unsafe_allow_html=True)

# Generate slow, elegant, fine-tuned warp lines dynamically via Python
warp_lines_html = "".join([
    f'<div class="warp-line" style="--angle: {random.randint(0, 360)}deg; width: {random.randint(20, 50)}px; animation-duration: {random.uniform(7.0, 12.0)}s; animation-delay: -{random.uniform(0, 10)}s;"></div>'
    for _ in range(65)
])

# Render the container inside the main content flow so its absolute center adapts automatically to sidebar toggles
st.markdown(f"""
<div class="hyperdrive-core">
    {warp_lines_html}
</div>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation & Contact Details
st.sidebar.markdown("### CONNOR PUNSHON")
st.sidebar.caption("Space Scientist & Systems Engineer")

# Sidebar Action Buttons (Resume Download & LinkedIn Link)
resume_path = "assests/Connor_Punshon_Resume.pdf"
if os.path.exists(resume_path):
    with open(resume_path, "rb") as pdf_file:
        st.sidebar.download_button(
            label="Download Resume",
            data=pdf_file,
            file_name="Connor_Punshon_Resume.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="sidebar_resume_download"
        )
else:
    st.sidebar.warning("Resume PDF not found in `assests/`")

st.sidebar.markdown(
    """
    <div style="margin-top: 8px; margin-bottom: 10px;">
        <a href="https://www.linkedin.com/in/connor-punshon/" target="_blank" class="sidebar-linkedin-btn" style="display: flex; align-items: center; justify-content: center; gap: 8px; background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); color: #ffffff; padding: 0.6rem 1rem; border-radius: 10px; text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="#ffffff">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            LinkedIn Profile
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

selected_page = st.sidebar.radio(
    "Navigation",
    ["Home", "Projects", "About & Skills", "Credentials"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.caption("Portfolio v1.0")


# Helper function to convert local image to base64 for reliable circular HTML rendering
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""


# FOOLPROOF CASE-INSENSITIVE IMAGE RESOLVER (Handles .JPG vs .jpg, case variations, and subfolders)
def resolve_image_path(folder_name, file_str):
    if not file_str:
        return None

    clean_name = os.path.basename(file_str)
    stem, ext = os.path.splitext(clean_name)

    # 1. Direct explicit candidates check
    candidates = [
        f"projects/{folder_name}/{file_str}",
        f"projects/{folder_name}/Media/{file_str}",
        f"projects/{folder_name}/media/{file_str}",
        f"projects/{folder_name}/Media/Pitot tube photos/{clean_name}",
        f"projects/{folder_name}/media/Pitot tube photos/{clean_name}",
        f"projects/{folder_name}/Media/Nexus photos/{clean_name}",
        f"projects/{folder_name}/media/Nexus photos/{clean_name}",
        f"projects/{folder_name}/Pitot tube photos/{clean_name}",
        f"projects/{folder_name}/Nexus photos/{clean_name}",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path

    # 2. Case-insensitive filename & extension scan inside the project folder
    project_files = glob.glob(f"projects/{folder_name}/**/*.*", recursive=True)
    for fpath in project_files:
        fname = os.path.basename(fpath)
        f_stem = os.path.splitext(fname)[0]
        if fname.lower() == clean_name.lower() or f_stem.lower() == stem.lower():
            if fpath.lower().endswith(('.jpg', '.jpeg', '.png')):
                return fpath

    # 3. Global repository-wide case-insensitive fallback scan
    all_repo_files = glob.glob("**/*.*", recursive=True)
    for fpath in all_repo_files:
        fname = os.path.basename(fpath)
        f_stem = os.path.splitext(fname)[0]
        if fname.lower() == clean_name.lower() or f_stem.lower() == stem.lower():
            if fpath.lower().endswith(('.jpg', '.jpeg', '.png')):
                return fpath

    return None


# 4. Page Router
if selected_page == "Home":
    col_home_text, col_home_img = st.columns([3, 1], gap="large")

    with col_home_text:
        st.title("Connor Punshon")
        st.subheader("Space Scientist | Focused on Aerospace Engineering & Avionics")

    with col_home_img:
        profile_candidates = glob.glob("assests/connor*.*")
        profile_img_path = profile_candidates[0] if profile_candidates else "assests/connor photo.jpg"

        b64_img = get_base64_image(profile_img_path)
        if b64_img:
            st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-top: 5px;">
                <div style="width: 160px; height: 160px; border-radius: 50%; overflow: hidden; background-color: #0b0f19; border: 2px solid rgba(10, 132, 255, 0.6); box-shadow: 0 8px 24px rgba(0,0,0,0.6);">
                    <img src="data:image/jpeg;base64,{b64_img}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Profile photo not found at `{profile_img_path}`.")

    st.markdown("---")

    st.markdown("### Introduction")
    st.write(
        "Hi, I'm Connor, a Space Scientist with a focus on aerospace engineering, passionate about turning complex "
        "orbital challenges into reliable hardware. My passion for aviation and spaceflight drives me to combine "
        "systems thinking with hands-on hardware development, from executing high-fidelity flight procedures in "
        "simulators to integrating embedded electronics for aerospace applications. I enjoy solving complex engineering "
        "problems and developing practical, reliable solutions."
    )
    st.write(
        "I recently completed a Bachelor of Space Science and hold an Associate Degree in Applied Science. "
        "My project experience includes developing embedded C++ software and contributing to the design and integration "
        "of custom PCBs for a 1U CubeSat payload intended for parabolic flight experiments, as well as engineering an electrical "
        "monitoring subsystem for a scaled spacecraft habitat module using Raspberry Pi, embedded Python, and environmental sensors. "
        "These projects strengthened my skills in hardware integration, reliable data acquisition, and multidisciplinary systems engineering."
    )
    st.write(
        "I'm seeking graduate opportunities in spacecraft engineering, satellite systems, payload integration, embedded systems, "
        "or related aerospace roles where I can contribute to the development of next-generation space technologies."
    )

    st.markdown("---")

    st.markdown("### Featured Highlights")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.info(
            "**NEMS / NEXUS Telemetry System**\n\nRaspberry Pi IoT environmental monitoring and OLED display architecture for spacecraft modules."
        )
    with col2:
        st.info(
            "**HIVE ATLAS Pitot-Static CFD**\n\nANSYS Fluent aerodynamic simulation and validation of a high-powered rocket nose-cone pitot system."
        )

elif selected_page == "Projects":
    st.title("Engineering Projects")
    st.write(
        "Browse my technical work below. Each project features comprehensive documentation, design approach, and engineering results.")
    st.markdown("---")

    # Load all projects dynamically from the projects folder
    projects = load_all_projects()

    if not projects:
        st.info("No projects found yet. Add a project folder to get started!")
    else:
        for proj in projects:
            meta = proj["metadata"]

            # Safely determine folder name based on project title
            title_str = meta.get("title", "").lower()
            if "pitot" in title_str or "hive" in title_str:
                folder_name = "02_hive_pitot_tube"
            else:
                folder_name = "01_nexus_telementry"

            # Render a professional card container for each project
            with st.container():
                st.subheader(meta.get("title", "Untitled Project"))
                st.caption(
                    f"**Category:** {meta.get('category', 'General')} | **Type:** {meta.get('type', 'N/A')} | **Year:** {meta.get('year', 'N/A')}")
                st.write(meta.get("summary", ""))

                # Render tech stack tags nicely
                techs = meta.get("technologies", [])
                if techs:
                    st.write("**Technologies:** " + " • ".join([f"`{t}`" for t in techs]))

                # Sticky Expandable section for full technical report and gallery
                expander_label = "View Full Project Documentation & Engineering Breakdown"

                with st.expander(expander_label, expanded=False):

                    # Robustly locate banner image for each project
                    if folder_name == "01_nexus_telementry":
                        banner_candidates = [
                            resolve_image_path(folder_name, "Nexus photos/nexus_banner.jpg"),
                            resolve_image_path(folder_name, "nexus_banner.jpg"),
                            resolve_image_path(folder_name, "Figure 0 (banner).jpg"),
                            resolve_image_path(folder_name, "Figure 1.jpg")
                        ]
                    else:
                        banner_candidates = [
                            resolve_image_path(folder_name, "Pitot tube photos/Figure 0 (banner).jpg"),
                            resolve_image_path(folder_name, "Figure 0 (banner).jpg"),
                            resolve_image_path(folder_name, "Pitot tube photos/Figure 0 (banner).png"),
                            resolve_image_path(folder_name, "Pitot tube photos/Figure 1.jpg")
                        ]

                    banner_path = next((p for p in banner_candidates if p and os.path.exists(p)), None)
                    if banner_path:
                        st.image(banner_path, use_container_width=True)
                    else:
                        st.warning(f"Could not locate banner image for `{folder_name}`")

                    st.markdown("---")

                    # Single clean layout: Technical write-up first
                    st.markdown(proj["content"])

                    # Universal Field Journal & Documentation Section for both projects
                    st.markdown("---")
                    st.markdown("### Engineering Field Journal & Documentation")

                    if folder_name == "01_nexus_telementry":
                        st.write(
                            "Access the official 23-page engineering field journal documenting the complete development lifecycle, weekly progress logs, circuit topologies, and validation results from the Space Physics group.")

                        # 1. Field Journal PDF Download
                        journal_path = f"projects/{folder_name}/media/Spacecraft Systems Engineering Environmental Telemetry & IoT Integration Field Journal.pdf"
                        if not os.path.exists(journal_path):
                            matches = glob.glob(f"projects/{folder_name}/**/*.pdf", recursive=True)
                            journal_path = matches[0] if matches else journal_path

                        if os.path.exists(journal_path):
                            with open(journal_path, "rb") as pdf_file:
                                st.download_button(
                                    label="Download NEXUS Engineering Field Journal (PDF)",
                                    data=pdf_file,
                                    file_name="NEXUS_Field_Journal.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                    key="download_nexus_journal"
                                )
                        else:
                            st.warning("NEXUS field journal PDF not found.")

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 2. Project Poster JPG Download/View
                        poster_candidates = glob.glob(f"projects/{folder_name}/**/*.jpg", recursive=True) + glob.glob(
                            f"projects/{folder_name}/**/*.png", recursive=True)
                        nexus_poster_path = next(
                            (p for p in poster_candidates if "banner" not in p.lower() and "nexus" not in p.lower()),
                            poster_candidates[0] if poster_candidates else "")

                        if nexus_poster_path and os.path.exists(nexus_poster_path):
                            with open(nexus_poster_path, "rb") as img_file:
                                st.download_button(
                                    label="Download NEXUS Project Poster (JPG)",
                                    data=img_file,
                                    file_name="NEXUS_Project_Poster.jpg",
                                    mime="image/jpeg",
                                    use_container_width=True,
                                    key="download_nexus_poster"
                                )
                        else:
                            st.warning("NEXUS project poster JPG not found in media folder.")

                    else:
                        st.write(
                            "Access the official research documentation, CAD assembly reports, and CFD validation logs from the Space Physics group under RMIT University supervision.")

                        # 1. Field Journal PDF Download
                        field_journal_candidates = glob.glob(
                            f"projects/{folder_name}/**/*Pitot*.pdf", recursive=True) + glob.glob(
                            f"projects/{folder_name}/**/*.pdf", recursive=True)
                        pitot_journal_path = next(
                            (p for p in field_journal_candidates if "Journal" not in p and "ONPS" not in p),
                            field_journal_candidates[0] if field_journal_candidates else "")

                        if pitot_journal_path and os.path.exists(pitot_journal_path):
                            with open(pitot_journal_path, "rb") as pdf_file:
                                st.download_button(
                                    label="Download Pitot-Static CFD Research Field Journal (PDF)",
                                    data=pdf_file,
                                    file_name="Pitot_Tube_Field_Journal.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                    key="download_pitot_journal"
                                )
                        else:
                            st.warning("Pitot field journal PDF not found.")

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 2. Journal Publication PDF Download
                        pub_candidates = glob.glob(f"projects/{folder_name}/**/*ONPS*.pdf", recursive=True) + glob.glob(
                            f"projects/{folder_name}/**/*Publication*.pdf", recursive=True)
                        pitot_pub_path = pub_candidates[0] if pub_candidates else ""

                        if pitot_pub_path and os.path.exists(pitot_pub_path):
                            with open(pitot_pub_path, "rb") as pdf_file:
                                st.download_button(
                                    label="Download Journal Publication (PDF)",
                                    data=pdf_file,
                                    file_name="ONPS2668_Journal_Publication.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                    key="download_pitot_pub"
                                )
                        else:
                            st.warning("Journal publication PDF not found in media folder.")

                    # Modern Two-Column Equal-Height Portfolio Card Grid with Flow Arrows between figures
                    images = meta.get("images", [])
                    if images:
                        st.markdown("---")
                        st.markdown("### Engineering Figures & Visuals Gallery")


                        def render_portfolio_grid(img_subset):
                            for idx in range(0, len(img_subset), 2):
                                if idx + 1 < len(img_subset):
                                    col_l, col_arr, col_r = st.columns([10, 2, 10], gap="small")

                                    # Left Figure
                                    with col_l:
                                        item_l = img_subset[idx]
                                        f_path_l = resolve_image_path(folder_name, item_l['file'])
                                        if f_path_l and os.path.exists(f_path_l):
                                            with st.container(border=True):
                                                st.image(f_path_l, use_container_width=True)
                                                st.markdown(
                                                    f"<div style='font-size: 0.88rem; color: #d1d5db; line-height: 1.4;'><b>{item_l.get('caption', '')}</b></div>",
                                                    unsafe_allow_html=True)
                                        else:
                                            st.warning(f"Missing image: {item_l['file']}")

                                    # Center Flow Arrow
                                    with col_arr:
                                        st.markdown(
                                            "<div style='display: flex; align-items: center; justify-content: center; height: 100%; min-height: 280px;'><span style='font-size: 1.8rem; color: #0a84ff; font-weight: 300;'>→</span></div>",
                                            unsafe_allow_html=True)

                                    # Right Figure
                                    with col_r:
                                        item_r = img_subset[idx + 1]
                                        f_path_r = resolve_image_path(folder_name, item_r['file'])
                                        if f_path_r and os.path.exists(f_path_r):
                                            with st.container(border=True):
                                                st.image(f_path_r, use_container_width=True)
                                                st.markdown(
                                                    f"<div style='font-size: 0.88rem; color: #d1d5db; line-height: 1.4;'><b>{item_r.get('caption', '')}</b></div>",
                                                    unsafe_allow_html=True)
                                        else:
                                            st.warning(f"Missing image: {item_r['file']}")
                                else:
                                    # Single remaining image if odd count
                                    item = img_subset[idx]
                                    f_path = resolve_image_path(folder_name, item['file'])
                                    if f_path and os.path.exists(f_path):
                                        with st.container(border=True):
                                            st.image(f_path, use_container_width=True)
                                            st.markdown(
                                                f"<div style='font-size: 0.88rem; color: #d1d5db; line-height: 1.4;'><b>{item.get('caption', '')}</b></div>",
                                                unsafe_allow_html=True)
                                    else:
                                        st.warning(f"Missing image: {item['file']}")


                        if folder_name == "02_hive_pitot_tube":
                            st.markdown("#### 1. Physical Principles & Flight Environment")
                            render_portfolio_grid(images[0:4])
                            st.markdown("---")
                            st.markdown("#### 2. CAD Modeling & Technical Drawings")
                            render_portfolio_grid(images[4:11])
                            st.markdown("---")
                            st.markdown("#### 3. Computational Meshing & Domain Setup")
                            render_portfolio_grid(images[11:18])
                            st.markdown("---")
                            st.markdown("#### 4. CFD Pressure Contours & Error Analysis")
                            render_portfolio_grid(images[18:])

                            # --- CONCLUDING RESULTS SUMMARY FOR PITOT TUBE ---
                            st.markdown("---")
                            st.markdown("### Aerodynamic Validation & Operational Summary")
                            st.write(
                                "The computational fluid dynamics investigation successfully established the operational envelopes "
                                "and pressure recovery performance of the nose-cone-integrated pitot-static probe. By coupling "
                                "high-resolution wall-resolved RANS simulations with rigorous off-axis incidence sweeps, the study "
                                "confirmed that total-pressure measurement accuracy remains within the nominal plus/minus 1 percent "
                                "acceptance threshold for low angles of attack up to 5 degrees, providing critical design guidelines "
                                "for unguided high-powered sounding rocket avionics integration."
                            )
                        else:
                            render_portfolio_grid(images)

                            # --- CONCLUDING RESULTS SUMMARY FOR NEXUS ---
                            st.markdown("---")
                            st.markdown("### Subsystem Validation & Operational Summary")
                            st.write(
                                "The integration of the NEMS telemetry subsystem within the 1:8 scale NEXUS habitat module "
                                "demonstrated robust multi-sensor synchronization and reliable dual-protocol data distribution. "
                                "By successfully establishing local situational awareness via real-time OLED display arrays and "
                                "simultaneous remote redundancy through ThingSpeak cloud logging, the hardware architecture "
                                "proved fully capable of supporting long-duration, unattended environmental monitoring for "
                                "simulated crewed habitats."
                            )

                st.markdown("---")

elif selected_page == "About & Skills":
    st.title("About & Technical Competencies")
    st.write("Professional software tools, engineering methodologies, and laboratory hardware competencies.")
    st.markdown("---")


    # Helper function to render logo cards in columns with uniform dimensions and scaling
    def render_logo_grid(items_list):
        cols = st.columns(4, gap="medium")
        for idx, (name, filename) in enumerate(items_list):
            col_idx = idx % 4
            with cols[col_idx]:
                with st.container(border=True):
                    logo_path = f"assests/logos/{filename}"
                    if os.path.exists(logo_path):
                        b64_logo = get_base64_image(logo_path)
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: center; height: 110px; background-color: rgba(255, 255, 255, 0.02); border-radius: 6px; margin-bottom: 8px;">
                            <img src="data:image/jpeg;base64,{b64_logo}" class="logo-card-img">
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"Missing: {filename}")
                    st.markdown(
                        f"<div style='text-align: center; font-weight: 700; font-size: 1.05rem; margin-top: 4px; color: #ffffff;'>{name}</div>",
                        unsafe_allow_html=True)


    st.markdown("### Software & Programming")
    software_items = [
        ("Python", "Python logo.jpg"),
        ("C++", "C++ logo.jpg"),
        ("MATLAB", "Matlab logo.jpg"),
        ("Git", "GIT logo.jpg")
    ]
    render_logo_grid(software_items)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Engineering & Simulation")
    engineering_items = [
        ("ANSYS", "ANSYS logo.jpg"),
        ("Onshape", "Onshape logo.jpg"),
        ("Fusion 360", "Fusion 360 logo.jpg"),
        ("FreeFlyer", "FreeFlyer logo.jpg"),
        ("Simulink", "Simulink logo.jpg"),
        ("Altium Designer", "Altium logo.jpg"),
        ("LTspice", "LTspice logo.jpg"),
        ("Fritzing", "Fritzing logo.jpg")
    ]
    render_logo_grid(engineering_items)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Systems & Hardware Competencies")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        with st.container(border=True):
            st.markdown("#### Systems Engineering")
            st.write(
                "- Requirements Analysis\n"
                "- Trade Studies\n"
                "- Flight Readiness Reviews\n"
                "- Telemetry Architectures"
            )
    with col2:
        with st.container(border=True):
            st.markdown("#### Embedded Hardware")
            st.write(
                "- SPI & I2C Protocols\n"
                "- Sensor Integration\n"
                "- Raspberry Pi & Microcontrollers\n"
                "- OLED Dashboard Displays"
            )
    with col3:
        with st.container(border=True):
            st.markdown("#### Laboratory & Lab Skills")
            st.write(
                "- Oscilloscopes & Logic Analyzers\n"
                "- Soldering & PCB Prototyping\n"
                "- Multimeter Diagnostics\n"
                "- Mechanical Assembly"
            )

elif selected_page == "Credentials":
    st.title("Academic Credentials & Certificates")
    st.write("Official transcripts, certificates of completion, and professional qualifications.")
    st.markdown("---")

    # --- ROW 1: Bachelor of Space Science ---
    st.markdown("### Bachelor of Space Science")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Testamur")
        st.caption("Royal Melbourne Institute of Technology (RMIT)")

        testamur_space_img = "assests/Testamur - Bachelor of Space Science screenshot.png"
        if os.path.exists(testamur_space_img):
            st.markdown('<div class="cert-image-container">', unsafe_allow_html=True)
            st.image(testamur_space_img)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Testamur screenshot not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        testamur_space_pdf = "assests/Testamur - Bachelor of Space Science.pdf"
        if os.path.exists(testamur_space_pdf):
            with open(testamur_space_pdf, "rb") as pdf_file:
                st.download_button(
                    label="Download Testamur (PDF)",
                    data=pdf_file,
                    file_name="Testamur_Bachelor_of_Space_Science.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_testamur_space"
                )
        else:
            st.warning("Testamur PDF not found.")

    with col2:
        st.subheader("Statement of Completion")
        st.caption("Royal Melbourne Institute of Technology (RMIT)")

        soc_space_img = "assests/Statement of Completion - BP330 screenshot.png"
        if os.path.exists(soc_space_img):
            st.markdown('<div class="cert-image-container">', unsafe_allow_html=True)
            st.image(soc_space_img)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Statement of Completion screenshot not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        soc_space_pdf = "assests/Statement of Completion - BP330.pdf"
        if os.path.exists(soc_space_pdf):
            with open(soc_space_pdf, "rb") as pdf_file:
                st.download_button(
                    label="Download Statement of Completion (PDF)",
                    data=pdf_file,
                    file_name="Statement_of_Completion_BP330.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_soc_space"
                )
        else:
            st.warning("Statement of Completion PDF not found.")

    st.markdown("---")

    # --- ROW 2: Associate Degree in Applied Science ---
    st.markdown("### Associate Degree in Applied Science")
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.subheader("Testamur")
        st.caption("Royal Melbourne Institute of Technology (RMIT)")

        testamur_app_img = "assests/Testamur - Associate Degree in Applied Science screenshot.png"
        if os.path.exists(testamur_app_img):
            st.markdown('<div class="cert-image-container">', unsafe_allow_html=True)
            st.image(testamur_app_img)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Testamur screenshot not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        testamur_app_pdf = "assests/Testamur - Associate Degree in Applied Science.pdf"
        if os.path.exists(testamur_app_pdf):
            with open(testamur_app_pdf, "rb") as pdf_file:
                st.download_button(
                    label="DownloadTestamur (PDF)",
                    data=pdf_file,
                    file_name="Testamur_Associate_Degree_Applied_Science.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_testamur_app"
                )
        else:
            st.warning("Testamur PDF not found.")

    with col4:
        st.subheader("Statement of Completion")
        st.caption("Royal Melbourne Institute of Technology (RMIT)")

        soc_app_img = "assests/Statement of Completion - AD012 screenshot.png"
        if os.path.exists(soc_app_img):
            st.markdown('<div class="cert-image-container">', unsafe_allow_html=True)
            st.image(soc_app_img)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Statement of Completion screenshot not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        soc_app_pdf = "assests/Statement of Completion - AD012.pdf"
        if os.path.exists(soc_app_pdf):
            with open(soc_app_pdf, "rb") as pdf_file:
                st.download_button(
                    label="Download Statement of Completion (PDF)",
                    data=pdf_file,
                    file_name="Statement_of_Completion_AD012.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_soc_app"
                )
        else:
            st.warning("Statement of Completion PDF not found.")