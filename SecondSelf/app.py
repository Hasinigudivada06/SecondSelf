import streamlit as st
import plotly.graph_objects as go
from simulator import simulate

st.set_page_config(
    page_title="SecondSelf",
    page_icon="🔮",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
}

h2 {
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 16px;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.08);
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.7rem;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "goal": "",
        "skill": 50,
        "study": 2,
        "projects": 1,
        "exercise": 3
    }

if "simulation" not in st.session_state:
    st.session_state.simulation = None


# ---------- SIDEBAR ----------
st.sidebar.title("🔮 SecondSelf")
st.sidebar.caption("Explore the consequences of your choices.")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "👤 Current Self",
        "🔮 Future Simulator",
        "📊 Comparison"
    ]
)


# ---------- HOME ----------
if page == "🏠 Home":

    st.title("🔮 SecondSelf")
    st.subheader("Explore the consequences of your choices before living them.")

    st.write(
        "SecondSelf is a personal scenario simulator that lets you "
        "experiment with different habits, goals and decisions."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Skill", f"{st.session_state.profile['skill']}/100")

    with col2:
        st.metric("Study / Day", f"{st.session_state.profile['study']} hrs")

    with col3:
        st.metric(
            "Projects / Month",
            st.session_state.profile["projects"]
        )

    st.divider()

    st.info(
        "💡 SecondSelf does NOT predict your actual future. "
        "It simulates possible outcomes using transparent assumptions."
    )


# ---------- CURRENT SELF ----------
elif page == "👤 Current Self":

    st.title("👤 Your Current Self")

    st.write("Tell SecondSelf where you are starting from.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Your Name",
            value=st.session_state.profile["name"]
        )

        goal = st.text_input(
            "Main Goal",
            value=st.session_state.profile["goal"],
            placeholder="e.g. Become an AI Engineer"
        )

        skill = st.slider(
            "Current Skill Level",
            0,
            100,
            st.session_state.profile["skill"]
        )

    with col2:
        study = st.slider(
            "Study / Learning Hours per Day",
            0,
            12,
            st.session_state.profile["study"]
        )

        projects = st.slider(
            "Projects per Month",
            0,
            10,
            st.session_state.profile["projects"]
        )

        exercise = st.slider(
            "Exercise Days per Week",
            0,
            7,
            st.session_state.profile["exercise"]
        )

    if st.button("💾 Save Profile", use_container_width=True):

        st.session_state.profile = {
            "name": name,
            "goal": goal,
            "skill": skill,
            "study": study,
            "projects": projects,
            "exercise": exercise
        }

        st.success("Profile saved successfully!")


# ---------- FUTURE SIMULATOR ----------
elif page == "🔮 Future Simulator":

    st.title("🔮 Future Simulator")

    st.write(
        "Change your habits and explore a possible future scenario."
    )

    current = st.session_state.profile

    col1, col2 = st.columns(2)

    with col1:

        future_study = st.slider(
            "📚 Study Hours / Day",
            0,
            12,
            current["study"]
        )

        future_projects = st.slider(
            "💻 Projects / Month",
            0,
            10,
            current["projects"]
        )

    with col2:

        future_exercise = st.slider(
            "🏃 Exercise Days / Week",
            0,
            7,
            current["exercise"]
        )

        duration = st.slider(
            "⏳ Simulation Duration (Months)",
            1,
            24,
            6
        )

    st.divider()

    if st.button("🚀 SIMULATE FUTURE", use_container_width=True):

        result = simulate(
            current_skill=current["skill"],
            current_study=current["study"],
            current_projects=current["projects"],
            current_exercise=current["exercise"],

            future_study=future_study,
            future_projects=future_projects,
            future_exercise=future_exercise,

            duration_months=duration
    )

        st.session_state.simulation = result

    st.success("Simulation complete! 🚀")


    # Show results
    if st.session_state.simulation:

        result = st.session_state.simulation
        final = result["final"]
        st.subheader("📊 Simulated Future")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Skill Growth",
                f"{final['skill']}/100"
            )

        with c2:
            st.metric(
                "Project Experience",
                f"{final['projects']}/100"
            )

        with c3:
            st.metric(
                "Consistency",
                f"{final['consistency']}/100"
            )

        with c4:
            st.metric(
                "Balance",
                f"{final['balance']}/100"
            )

        # Radar chart
        categories = [
            "Skill",
            "Projects",
            "Consistency",
            "Balance"
        ]

        values = [
            final["skill"],
            final["projects"],
            final["consistency"],
            final["balance"]
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name="Future Scenario"
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.subheader("📈 Your Journey Over Time")

        trajectory = go.Figure()

        trajectory.add_trace(
            go.Scatter(
                x=result["months"],
                y=result["skill"],
                mode="lines+markers",
                name="Skill"
            )
        )

        trajectory.add_trace(
            go.Scatter(
                x=result["months"],
                y=result["projects"],
                mode="lines+markers",
                name="Projects"
            )
        )

        trajectory.add_trace(
            go.Scatter(
                x=result["months"],
                y=result["consistency"],
                mode="lines+markers",
                name="Consistency"
            )
        )

        trajectory.add_trace(
            go.Scatter(
                x=result["months"],
                y=result["balance"],
                mode="lines+markers",
                name="Balance"
            )
        )

        trajectory.update_layout(
            xaxis_title="Months",
            yaxis_title="Simulation Indicator",
            yaxis=dict(range=[0, 100]),
            hovermode="x unified"
        )

        st.plotly_chart(
            trajectory,
            use_container_width=True
        )

# ---------- COMPARISON ----------
elif page == "📊 Comparison":

    st.title("📊 Compare Possible Futures")

    st.write(
        "Different choices can create different trade-offs."
    )

    current = st.session_state.profile
    result = st.session_state.simulation

    if not result:

        st.warning(
            "Run a simulation first."
        )

    else:

        data = {
            "Current Self": [
                current["skill"],
                current["projects"] * 10,
                60,
                70
            ],
            "Simulated Future": [
                result["final"]["skill"],
                result["final"]["projects"],
                result["final"]["consistency"],
                result["final"]["balance"]
            ]
        }

        fig = go.Figure()

        categories = [
            "Skill",
            "Projects",
            "Consistency",
            "Balance"
        ]

        for name, values in data.items():

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill="toself",
                    name=name
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("🤖 AI Explanation")

        st.info(
            "Your simulated scenario shows how changing your "
            "study time, project activity and exercise habits "
            "could affect different development indicators. "
            "The model highlights trade-offs rather than "
            "predicting a guaranteed outcome."
        )