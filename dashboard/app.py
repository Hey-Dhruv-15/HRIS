import streamlit as st
import pandas as pd
from pathlib import Path
import json
import os
import tempfile
from datetime import datetime
from agent.adk_client import ask_agent
from sarvamai import SarvamAI
from sarvamai.play import save

st.set_page_config(page_title="NHRIS Dashboard", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"]  { font-family: 'IBM Plex Sans', sans-serif; }
h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; }
.metric-card {
  background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
  border: 1px solid #1f2937;
  padding: 16px 18px;
  border-radius: 14px;
  color: #e5e7eb;
}
.metric-title { font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: #9ca3af; }
.metric-value { font-size: 28px; font-weight: 700; margin-top: 6px; }
.badge { display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; }
.badge-high { background: #7f1d1d; color: #fecaca; border: 1px solid #991b1b; }
.badge-med { background: #78350f; color: #fde68a; border: 1px solid #b45309; }
.badge-low { background: #064e3b; color: #a7f3d0; border: 1px solid #047857; }
.section { padding: 6px 0 2px 0; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("National Health Risk Intelligence System (NHRIS)")
st.caption("Real-time national health risk monitoring • Spark + Delta Lake + Airflow + AI")

base_dir = Path(os.environ.get("NHRIS_DATA", "data"))
alerts_path = base_dir / "alerts" / "latest.json"

if not alerts_path.exists():
    st.warning("No alerts found. Run the generator + Spark job first.")
    st.caption(f"Looking for alerts at: {alerts_path}")
    st.stop()

payload = json.loads(alerts_path.read_text(encoding="utf-8"))
alerts = payload.get("alerts", [])

if not alerts:
    st.info("No active alerts.")
    st.stop()

df = pd.DataFrame(alerts)
df["case_count"] = pd.to_numeric(df["case_count"], errors="coerce").fillna(0).astype(int)
df["severity"] = pd.cut(
    df["case_count"],
    bins=[-1, 24, 49, 1000],
    labels=["Low", "Medium", "High"],
)

generated_at = payload.get("generated_at")
if generated_at:
    try:
        generated_at = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except Exception:
        generated_at = None

st.sidebar.title("NHRIS Control Room")
st.sidebar.caption("Ops view for demo")
auto_refresh = st.sidebar.toggle("Auto-refresh (10s)", value=False, key="auto_refresh")
region_filter = st.sidebar.multiselect(
    "Filter by region",
    sorted(df["region"].dropna().unique().tolist()),
)
diag_filter = st.sidebar.multiselect(
    "Filter by diagnosis",
    sorted(df["diagnosis"].dropna().unique().tolist()),
)
if auto_refresh:
    st.sidebar.info("Auto-refresh enabled")

if region_filter:
    df = df[df["region"].isin(region_filter)]
if diag_filter:
    df = df[df["diagnosis"].isin(diag_filter)]

st.markdown("### Situation Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f\"\"\"<div class='metric-card'>
        <div class='metric-title'>Active Alerts</div>
        <div class='metric-value'>{len(df)}</div>
        </div>\"\"\",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f\"\"\"<div class='metric-card'>
        <div class='metric-title'>Regions Impacted</div>
        <div class='metric-value'>{df['region'].nunique()}</div>
        </div>\"\"\",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f\"\"\"<div class='metric-card'>
        <div class='metric-title'>Max Cases</div>
        <div class='metric-value'>{df['case_count'].max()}</div>
        </div>\"\"\",
        unsafe_allow_html=True,
    )
with col4:
    ts = generated_at.strftime("%b %d, %H:%M UTC") if generated_at else "Unknown"
    st.markdown(
        f\"\"\"<div class='metric-card'>
        <div class='metric-title'>Last Update</div>
        <div class='metric-value' style='font-size:18px'>{ts}</div>
        </div>\"\"\",
        unsafe_allow_html=True,
    )

st.markdown("### Active Alerts")
show_cols = ["region", "city", "diagnosis", "case_count", "alert_reason", "severity"]
st.dataframe(
    df[show_cols]
    .sort_values(["case_count"], ascending=False)
    .reset_index(drop=True),
    width="stretch",
    hide_index=True,
)

st.markdown("### Regional Hotspots")
region_df = df.groupby("region", as_index=False)["case_count"].sum()
geo = pd.DataFrame(
    {
        "lat": [12.9716, 19.0760, 28.6139, 13.0827, 9.9312, 23.0225],
        "lon": [77.5946, 72.8777, 77.2090, 80.2707, 76.2673, 72.5714],
        "region": ["Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Kerala", "Gujarat"],
    }
)
geo = geo.merge(region_df, on="region", how="left").fillna({"case_count": 0})
st.map(geo.rename(columns={"case_count": "cases"}))

left, right = st.columns([1.1, 1])
with left:
    st.markdown("### Alerts by Diagnosis")
    diag_df = df.groupby("diagnosis", as_index=False)["case_count"].sum().sort_values("case_count", ascending=False)
    st.bar_chart(diag_df.set_index("diagnosis"))
with right:
    st.markdown("### Severity Mix")
    sev_df = df["severity"].value_counts().reset_index()
    sev_df.columns = ["severity", "count"]
    st.bar_chart(sev_df.set_index("severity"))

st.markdown("### Hospital Overload Signals")
overload = df[df["alert_reason"].str.contains("overload", case=False, na=False)]
if overload.empty:
    st.write("No overload alerts in current batch.")
else:
    st.table(overload[["region", "city", "case_count", "alert_reason"]])

st.markdown("### Fever Spikes")
fever = df[df["diagnosis"] == "fever"]
if fever.empty:
    st.write("No fever spikes in current batch.")
else:
    st.table(fever[["region", "city", "case_count", "alert_reason"]])

st.divider()
st.markdown("### AI Command Center")
question = st.text_input("Ask a health risk question", key="ai_question", placeholder="Which regions show abnormal fever cases today?")
if st.button("Ask", key="ai_ask_button"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            answer = ask_agent(question)
            st.write(answer or "No response from agent.")
        except Exception as e:
            st.error(f"ADK error: {e}")

st.markdown("### Voice Interface (Sarvam AI)")
sarvam_key = os.environ.get("SARVAM_API_KEY")

audio_input = None
try:
    audio_input = st.audio_input("Tap to record a voice query", key="voice_record")
except Exception:
    audio_input = None

uploaded = st.file_uploader(
    "Or upload a short audio query (wav/mp3/m4a)",
    type=["wav", "mp3", "m4a"],
    key="voice_upload",
)

audio_source = audio_input or uploaded

if audio_source and st.button("Transcribe + Answer", key="voice_transcribe"):
    if not sarvam_key:
        st.error("SARVAM_API_KEY is not set.")
    else:
        try:
            client = SarvamAI(api_subscription_key=sarvam_key)
            # Normalize to a file-like object
            if hasattr(audio_source, "read"):
                file_obj = audio_source
            else:
                tmp_in = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tmp_in.write(audio_source)
                tmp_in.flush()
                tmp_in.seek(0)
                file_obj = open(tmp_in.name, "rb")

            response = client.speech_to_text.transcribe(file=file_obj, model="saaras:v2.5")
            transcript = response.get("transcript", "")
            st.text_area("Transcript", transcript, height=80, key="voice_transcript")

            answer = ask_agent(transcript) or "No response from agent."
            st.text_area("Answer", answer, height=80, key="voice_answer")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio = client.text_to_speech.convert(
                    target_language_code="en-IN",
                    text=answer,
                    model="bulbul:v2",
                    speaker="anushka",
                )
                save(audio, tmp.name)
                st.audio(tmp.name)
        except Exception as e:
            st.error(f"Sarvam error: {e}")
