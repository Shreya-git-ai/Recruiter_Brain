import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st

st.set_page_config(
    page_title="Ranking Results",
    layout="wide",
    page_icon="🏆"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "results_df" not in st.session_state:
    st.session_state["results_df"] = None

if "selected" not in st.session_state:
    st.session_state["selected"] = None

# --------------------------------------------------
# Layout
# --------------------------------------------------
col_main, col_right = st.columns([2.4, 1])

# ==================================================
# LEFT PANEL
# ==================================================
with col_main:

    st.title("🏆 Candidate Rankings")

    df = st.session_state["results_df"]

    if df is None:

        st.warning("No ranking results available.")

        st.markdown(
            """
            Go to **Home** and run the matching engine first.
            """
        )

    else:

        # -----------------------------------------
        # Filters
        # -----------------------------------------

        filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

        with filter_col1:
            search_text = st.text_input(
                "🔍 Search Candidate ID",
                placeholder="e.g. CAND_0042871"
            )

        with filter_col2:
            min_score = st.slider(
                "Minimum Score",
                0.0,
                1.0,
                0.0,
                0.05
            )

        with filter_col3:
            show_count = st.selectbox(
                "Show",
                [10, 20, 50, 100],
                index=1
            )

        # -----------------------------------------
        # Apply Filters
        # -----------------------------------------

        filtered_df = df.copy()

        filtered_df = filtered_df[
            filtered_df["score"] >= min_score
        ]

        if search_text:
            filtered_df = filtered_df[
                filtered_df["candidate_id"]
                .str.contains(search_text, case=False)
            ]

        filtered_df = filtered_df.head(show_count)

        # -----------------------------------------
        # Stats
        # -----------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Visible Candidates", len(filtered_df))

        with c2:
            st.metric(
                "Top Score",
                f"{filtered_df['score'].max():.3f}"
                if len(filtered_df)
                else "-"
            )

        with c3:
            st.metric(
                "Avg Score",
                f"{filtered_df['score'].mean():.3f}"
                if len(filtered_df)
                else "-"
            )

        st.divider()

        # -----------------------------------------
        # Candidate Cards
        # -----------------------------------------

        for _, row in filtered_df.iterrows():

            rank = int(row["rank"])

            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = "🏅"

            if row["score"] >= 0.80:
                badge = "🟢 Strong Match"
            elif row["score"] >= 0.60:
                badge = "🟡 Moderate Match"
            else:
                badge = "⚪ Potential Match"

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.markdown(
                        f"### {medal} Rank #{rank} — {row['candidate_id']}"
                    )

                    st.caption(badge)

                    st.write(row["reasoning"])

                with col2:

                    st.metric(
                        "Score",
                        f"{row['score']:.3f}"
                    )

                if st.button(
                    "View Details",
                    key=f"btn_{row['candidate_id']}"
                ):
                    st.session_state["selected"] = row.to_dict()

        st.divider()

        csv_data = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Results CSV",
            data=csv_data,
            file_name="ranked_candidates.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==================================================
# RIGHT PANEL
# ==================================================
with col_right:

    st.title("🧠 Candidate Insight")

    selected = st.session_state.get("selected", None)

    if selected:

        st.subheader(selected["candidate_id"])

        m1, m2 = st.columns(2)

        with m1:
            st.metric(
                "Rank",
                f"#{selected['rank']}"
            )

        with m2:
            st.metric(
                "Score",
                f"{selected['score']:.3f}"
            )

        st.divider()

        st.markdown("### Why this candidate?")

        st.info(selected["reasoning"])

        st.divider()

        st.markdown("### Match Strength")

        st.progress(
            float(
                min(
                    max(selected["score"], 0.0),
                    1.0
                )
            )
        )

        score = selected["score"]

        if score >= 0.80:
            st.success(
                "Strong alignment with the target role."
            )

        elif score >= 0.60:
            st.warning(
                "Moderate alignment. Worth recruiter review."
            )

        else:
            st.error(
                "Lower alignment compared with higher-ranked candidates."
            )

    else:

        st.info(
            "Select a candidate to inspect ranking details."
        )