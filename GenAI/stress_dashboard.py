import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Page configuration
st.set_page_config(
    page_title="Student Stress Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #DADDEC;
        padding: 1rem;
        border-radius: 0.8rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    div[data-testid="metric-container"] > label {
        color: #0F52BA;
        font-weight: 600;
    }
    div[data-testid="metric-container"] > div {
        color: #1E88E5;
        font-family: 'Arial Black';
    }
    div[data-testid="stMetricValue"] > div {
        background-color: #E3F2FD;
        padding: 0.5rem;
        border-radius: 0.5rem;
        font-size: 1.5rem;
    }
    div[data-testid="stMetricDelta"] > div {
        background-color: #E8F5E9;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
    }
    /* Stress level indicators */
    .low-stress { color: #4CAF50 !important; }
    .medium-stress { color: #FFA726 !important; }
    .high-stress { color: #EF5350 !important; }
    </style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('E:/Data Analytics/Gen AI/ProjectsGH/StressLevelDataset.csv')
    return df

# Load the model
@st.cache_resource
def load_model():
    model = joblib.load('stress_level_model.joblib')
    scaler = joblib.load('stress_level_scaler.joblib')
    return model, scaler

# Main function
def main():
    # Title
    st.title("📊 Student Stress Level Analysis Dashboard")
    st.markdown("---")

    # Load data and model
    try:
        df = load_data()
        model, scaler = load_model()
        
        # Sidebar
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Overview", "Stress Factors", "Predictions", "Recommendations"])

        if page == "Overview":
            show_overview(df)
        elif page == "Stress Factors":
            show_stress_factors(df)
        elif page == "Predictions":
            show_predictions(df, model, scaler)
        else:
            show_recommendations()

    except Exception as e:
        st.error(f"Error loading data or model: {str(e)}")

def show_overview(df):
    st.header("Overview of Student Stress Levels")
    
    # Calculate stress level distributions
    low_stress = df[df['stress_level'] <= 2]
    medium_stress = df[(df['stress_level'] > 2) & (df['stress_level'] <= 5)]
    high_stress = df[df['stress_level'] > 5]
    
    total_students = len(df)
    low_stress_percent = (len(low_stress) / total_students) * 100
    medium_stress_percent = (len(medium_stress) / total_students) * 100
    high_stress_percent = (len(high_stress) / total_students) * 100
    
    # Key metrics with color-coded stress levels
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Low Stress Level", 
                 f"{low_stress_percent:.1f}%", 
                 f"{len(low_stress)} students",
                 help="Students with stress level 0-2")
        st.markdown('<style>div[data-testid="metric-container"] > div { color: #4CAF50 !important; }</style>', 
                   unsafe_allow_html=True)
    with col2:
        st.metric("Medium Stress Level", 
                 f"{medium_stress_percent:.1f}%",
                 f"{len(medium_stress)} students",
                 help="Students with stress level 3-5")
        st.markdown('<style>div[data-testid="stMetricValue"]:nth-of-type(2) > div { color: #FFA726 !important; }</style>', 
                   unsafe_allow_html=True)
    with col3:
        st.metric("High Stress Level", 
                 f"{high_stress_percent:.1f}%",
                 f"{len(high_stress)} students",
                 help="Students with stress level 6-8")
        st.markdown('<style>div[data-testid="stMetricValue"]:nth-of-type(3) > div { color: #EF5350 !important; }</style>', 
                   unsafe_allow_html=True)

    # Distribution of stress levels
    st.subheader("Distribution of Stress Levels")
    fig = px.histogram(df, x='stress_level', 
                      title='Distribution of Stress Levels',
                      labels={'stress_level': 'Stress Level', 'count': 'Number of Students'},
                      color='stress_level')
    st.plotly_chart(fig)

    # Correlation heatmap
    st.subheader("Correlation Between Factors")
    fig = px.imshow(df.corr(), 
                    aspect='auto',
                    labels=dict(color="Correlation"))
    st.plotly_chart(fig)

def show_stress_factors(df):
    st.header("Analysis of Stress Factors")

    # Feature importance plot
    importance_df = pd.DataFrame({
        'feature': ['blood_pressure', 'sleep_quality', 'extracurricular_activities', 
                   'bullying', 'basic_needs', 'teacher_student_relationship'],
        'importance': [0.15, 0.09, 0.08, 0.075, 0.07, 0.065]
    })
    
    st.subheader("Top Factors Contributing to Stress")
    fig = px.bar(importance_df, x='importance', y='feature', orientation='h',
                 title='Impact of Different Factors on Stress Levels')
    st.plotly_chart(fig)

    # Interactive factor analysis
    selected_factor = st.selectbox("Select a factor to analyze:", df.columns[:-1])
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(df, x='stress_level', y=selected_factor,
                    title=f'{selected_factor} vs Stress Level')
        st.plotly_chart(fig)
    
    with col2:
        fig = px.violin(df, x='stress_level', y=selected_factor,
                       title=f'Distribution of {selected_factor} by Stress Level')
        st.plotly_chart(fig)

def show_predictions(df, model, scaler):
    st.header("Stress Level Prediction")
    st.write("Enter your information to predict stress level")

    # Create input form with all required features
    col1, col2 = st.columns(2)
    
    with col1:
        basic_needs = st.slider("Basic Needs Met (1-5)", 1, 5, 3)
        blood_pressure = st.slider("Blood Pressure Level (1-5)", 1, 5, 3)
        breathing_problem = st.slider("Breathing Problems (1-5)", 1, 5, 1)
        headache = st.slider("Headache Frequency (1-5)", 1, 5, 2)
        living_conditions = st.slider("Living Conditions (1-5)", 1, 5, 3)
        sleep_quality = st.slider("Sleep Quality (1-5)", 1, 5, 3)
        extracurricular = st.slider("Extracurricular Activities (1-5)", 1, 5, 3)
        bullying = st.slider("Bullying Experience (1-5)", 1, 5, 1)

    with col2:
        teacher_relation = st.slider("Teacher-Student Relationship (1-5)", 1, 5, 3)
        anxiety = st.slider("Anxiety Level (1-5)", 1, 5, 3)
        depression = st.slider("Depression Level (1-5)", 1, 5, 2)
        panic_attack = st.slider("Panic Attack Frequency (1-5)", 1, 5, 1)
        peer_pressure = st.slider("Peer Pressure (1-5)", 1, 5, 2)
        self_esteem = st.slider("Self Esteem (1-5)", 1, 5, 3)
        study_load = st.slider("Study Load (1-5)", 1, 5, 3)
        social_support = st.slider("Social Support (1-5)", 1, 5, 3)

    if st.button("Predict Stress Level"):
        # Create input data with all required features
        input_data = {
            'basic_needs': basic_needs,
            'blood_pressure': blood_pressure,
            'breathing_problem': breathing_problem,
            'headache': headache,
            'living_conditions': living_conditions,
            'sleep_quality': sleep_quality,
            'extracurricular_activities': extracurricular,
            'bullying': bullying,
            'teacher_student_relationship': teacher_relation,
            'anxiety_level': anxiety,
            'depression': depression,
            'panic_attack': panic_attack,
            'peer_pressure': peer_pressure,
            'self_esteem': self_esteem,
            'study_load': study_load,
            'social_support': social_support
        }
        
        # Make prediction
        input_df = pd.DataFrame([input_data])
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
        
        # Show prediction
        st.subheader("Prediction Result")
        stress_levels = {0: "Low", 1: "Medium", 2: "High"}
        st.write(f"Predicted Stress Level: **{stress_levels[prediction]}**")
        
        # Show gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = prediction,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Stress Level"},
            gauge = {
                'axis': {'range': [0, 2]},
                'steps': [
                    {'range': [0, 0.7], 'color': "lightgreen"},
                    {'range': [0.7, 1.3], 'color': "yellow"},
                    {'range': [1.3, 2], 'color': "red"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': prediction}}))
        st.plotly_chart(fig)

def show_recommendations():
    st.header("Recommendations for Stress Management")

    # Categories of recommendations
    categories = {
        "Physical Health": [
            "Regular exercise (30 minutes daily)",
            "Maintain consistent sleep schedule",
            "Balanced diet and proper nutrition",
            "Regular health check-ups",
            "Breathing exercises and meditation"
        ],
        "Academic Balance": [
            "Create a structured study schedule",
            "Take regular breaks using the Pomodoro Technique",
            "Join study groups for support",
            "Seek help from professors during office hours",
            "Break large tasks into smaller, manageable parts"
        ],
        "Mental Well-being": [
            "Practice mindfulness and meditation",
            "Seek counseling services when needed",
            "Maintain a journal for emotional expression",
            "Set realistic goals and expectations",
            "Practice positive self-talk"
        ],
        "Social Support": [
            "Stay connected with family and friends",
            "Join campus clubs or organizations",
            "Participate in group activities",
            "Build a support network",
            "Share concerns with trusted individuals"
        ]
    }

    for category, recommendations in categories.items():
        with st.expander(f"{category} 👉"):
            for rec in recommendations:
                st.write(f"• {rec}")

    # Additional Resources
    st.subheader("Additional Resources")
    st.write("""
    - Campus Counseling Services
    - Student Health Center
    - Academic Advisory Services
    - Peer Support Groups
    - Online Mental Health Resources
    """)

if __name__ == "__main__":
    main()
