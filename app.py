import streamlit as st
import pandas as pd
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Prompt Lab",
    page_icon="🤖",
    layout="centered"
)

# ---------------- GOOGLE GENERATIVE AI CLIENT ----------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------------- TITLE ----------------

st.title("🤖 Prompt Lab")

# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #f4f6f9;
}

/* Main Heading */
h1 {
    color: #0B3D91;
    text-align: center;
    font-weight: 700;
}

/* Subheading */
h3 {
    color: #333333;
    text-align: center;
}

/* Buttons */
.stButton > button {
    background-color: #0B3D91;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
    font-weight: bold;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #d0d7de;
    background-color: white;
}

/* Info Boxes */
div.stAlert {
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0B3D91;
    color: white;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px;
    font-weight: bold;
}

/* Metric Styling */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

st.subheader("AI-Powered Prompt Engineering Evaluator")

# ---------------- USER DETAILS ----------------

st.markdown("## 👤 User Information")

user_name = st.text_input(
    "Enter Your Name",
    placeholder="Example: Aditi Singh"
)

employee_id = st.text_input(
    "Employee ID (Optional)",
    placeholder="Example: TS1024"
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🏭 Prompt Lab")

    st.markdown("""
### About This Project

AI-powered prompt engineering evaluation platform designed for industrial learning environments.

### Key Features
- Prompt Evaluation
- RCTCF Analysis
- AI Feedback
- Dynamic Scoring
- Visual Analytics
- Downloadable Reports

### Internship Focus
Designed for Tata Steel Learning & Development use cases.
""")

    st.markdown("---")

    st.caption("Built using Streamlit + Gemini AI")

# ---------------- INTRO ----------------

st.markdown("""
Welcome to the Prompt Lab.

This system helps users practice prompt engineering using the RCTCF framework.

### RCTCF Framework
- **R** → Role
- **C** → Context
- **T** → Task
- **C** → Constraints
- **F** → Format
""")

# ---------------- SCENARIO SELECTION ----------------

scenario_options = {

    "Troubleshooting Assistance":
    """
    A technician at Tata Steel notices sudden conveyor vibration during operation.

    Task:
    Create a structured AI prompt using the RCTCF framework to get troubleshooting guidance.
    """,

    "SOP Retrieval":
    """
    An employee needs the emergency shutdown SOP for a conveyor system.

    Task:
    Create a structured AI prompt to retrieve the SOP correctly.
    """,

    "Safety Guidance":
    """
    A new employee entering the blast furnace area wants to understand mandatory PPE and safety precautions.

    Task:
    Create a structured AI prompt using the RCTCF framework.
    """,

    "Learning Recommendation":
    """
    A new blast furnace operator joins Tata Steel and wants to know what training modules should be completed first.

    Task:
    Create a structured AI prompt using the RCTCF framework.
    """
}

selected_scenario = st.selectbox(
    "Select Industrial Scenario",
    list(scenario_options.keys())
)

scenario = scenario_options[selected_scenario]

# ---------------- DISPLAY SCENARIO ----------------

st.markdown("## 📌 Scenario")
st.info(scenario)

# ---------------- USER INPUT ----------------

user_prompt = st.text_area(
    "✍️ Write your prompt here:",
    height=200,
    placeholder="Type your structured prompt here..."
)

# ---------------- BUTTON ----------------

if st.button("Evaluate Prompt"):

    if user_prompt.strip() == "":
        st.warning("Please enter a prompt first.")

    else:

        evaluation_prompt = f"""
You are a professional prompt engineering evaluator.

Analyze the user's prompt using the RCTCF framework.

RCTCF:
- R → Role
- C → Context
- T → Task
- C → Constraints
- F → Format

Evaluate the prompt and return output in the following structured format:

# Prompt Score
Give score out of 10.

# RCTCF Analysis
Mention whether each component is Present or Missing:
- Role
- Context
- Task
- Constraints
- Format

# Strengths
Mention what is good in the prompt.

# Missing Components
Mention what is missing.

# Suggestions for Improvement
Explain how the prompt can be improved.

# Improved Prompt
Generate a better version of the user's prompt.

User Prompt:
{user_prompt}
"""

        with st.spinner("Evaluating prompt..."):

            response = model.generate_content(evaluation_prompt)

            result = response.text

        # ---------------- OUTPUT ----------------

        st.markdown("## ✅ Evaluation Result")

        with st.expander("📊 AI Evaluation Feedback", expanded=True):
            st.write(result)

        st.success("Prompt evaluation completed successfully.")

        st.info(
            "Tip: Better context and clearer formatting usually improve AI output quality."
        )

        # ---------------- DYNAMIC RCTCF SCORING ----------------

        role_score = 1 if "you are" in user_prompt.lower() else 0

        context_score = 1 if len(user_prompt.split()) > 15 else 0

        task_score = 1 if any(
            word in user_prompt.lower()
            for word in ["explain", "generate", "retrieve", "provide"]
        ) else 0

        constraint_score = 1 if any(
            word in user_prompt.lower()
            for word in ["step-by-step", "brief", "detailed", "simple"]
        ) else 0

        format_score = 1 if any(
            word in user_prompt.lower()
            for word in ["table", "bullet", "checklist", "format"]
        ) else 0

        score_data = {
            "Component": ["Role", "Context", "Task", "Constraints", "Format"],
            "Score": [
                role_score,
                context_score,
                task_score,
                constraint_score,
                format_score
            ]
        }

        df = pd.DataFrame(score_data)

        st.markdown("## 📊 RCTCF Component Analysis")

        st.bar_chart(df.set_index("Component"))

        # ---------------- OVERALL SCORE ----------------

        total_score = (
            role_score +
            context_score +
            task_score +
            constraint_score +
            format_score
        )

        percentage = int((total_score / 5) * 100)

        st.markdown("## 🎯 Overall Prompt Quality Score")

        st.progress(percentage / 100)

        st.metric(
            label="Prompt Quality",
            value=f"{percentage}%"
        )

        # ---------------- DOWNLOAD REPORT ----------------

        report = f"""
PROMPT LAB EVALUATION REPORT

User Name:
{user_name}

Employee ID:
{employee_id}

Scenario:
{selected_scenario}

User Prompt:
{user_prompt}

Overall Prompt Quality:
{percentage}%

AI Evaluation:
{result}
"""

        st.download_button(
            label="📥 Download Evaluation Report",
            data=report,
            file_name="prompt_evaluation_report.txt",
            mime="text/plain"
        )

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("Prompt Lab Prototype | Tata Steel AI Learning Initiative")