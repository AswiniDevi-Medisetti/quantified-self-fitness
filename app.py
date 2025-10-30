import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from io import BytesIO
import base64

# Set up Streamlit page config
st.set_page_config(
    page_title="FitMetrics Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern color scheme
PRIMARY_COLOR = "#FF4B4B"
SECONDARY_COLOR = "#0F9D58"
BG_COLOR = "#0E1117"
CARD_COLOR = "#192841"

# Background image setup
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: rgba(14, 17, 23, 0.95);
            background-blend-mode: overlay;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom styling with enhanced features
st.markdown(f"""
    <style>
    :root {{
        --primary: {PRIMARY_COLOR};
        --secondary: {SECONDARY_COLOR};
    }}
    
    .main {{
        background-color: transparent;
        color: white;
    }}
    
    .stButton>button {{
        background-color: var(--primary) !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4) !important;
    }}
    
    .stSlider .st-c7 {{
        background-color: var(--primary) !important;
    }}
    
    .stRadio [role=radiogroup] label [data-testid=stMarkdownContainer] p {{
        font-size: 16px !important;
    }}
    
    .card {{
        background: linear-gradient(135deg, {CARD_COLOR}, #1a3a5f);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }}
    
    .metric-value {{
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
        text-shadow: 0 2px 10px rgba(255, 75, 75, 0.3);
    }}
    
    .progress-container {{
        height: 8px;
        background: #2c3e50;
        border-radius: 4px;
        margin: 10px 0;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 4px;
        transition: width 0.5s ease;
    }}
    
    .feature-card {{
        transition: transform 0.3s;
        border-radius: 10px;
        overflow: hidden;
        background: {CARD_COLOR};
        padding: 15px;
        margin-bottom: 10px;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    
    .achievement-badge {{
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }}
    
    .pulse-animation {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    footer {{
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #aaa;
    }}
    
    /* New styles for enhanced features */
    .workout-card {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}20, {SECONDARY_COLOR}20);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid var(--primary);
    }}
    
    .nutrition-card {{
        background: linear-gradient(135deg, #4CAF5020, #2196F320);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }}
    
    .challenge-card {{
        background: linear-gradient(135deg, #9C27B020, #E91E6320);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #9C27B0;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for new features
if 'workout_history' not in st.session_state:
    st.session_state.workout_history = []
if 'nutrition_log' not in st.session_state:
    st.session_state.nutrition_log = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'challenges' not in st.session_state:
    st.session_state.challenges = [
        {"name": "10K Steps Daily", "progress": 75, "target": 100},
        {"name": "30 Day Yoga", "progress": 45, "target": 100},
        {"name": "Hydration Master", "progress": 60, "target": 100}
    ]

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3082/3082015.png", width=80)
    st.title("FitMetrics Pro")
    st.markdown("### Track. Analyze. Transform.")
    st.markdown("Monitor your fitness journey with AI-powered insights")
    
    # User profile section
    st.subheader("👤 Your Profile")
    user_name = st.text_input("Name", "Aswini Shetty")
    fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    
    # Quick stats
    st.subheader("📊 Quick Stats")
    st.metric("Current Streak", "7 days 🔥")
    st.metric("Total Workouts", "24")
    st.metric("Calories Burned", "12,450 kcal")
    
    # Features with icons
    st.subheader("✨ Premium Features")
    features = [
        {"icon": "📈", "name": "Performance Analytics"},
        {"icon": "🎯", "name": "Smart Goal Setting"},
        {"icon": "🧠", "name": "AI Health Insights"},
        {"icon": "🏆", "name": "Achievement Badges"},
        {"icon": "🤝", "name": "Community Challenges"},
        {"icon": "📊", "name": "Body Composition"},
        {"icon": "🍎", "name": "Nutrition Tracking"},
        {"icon": "💤", "name": "Sleep Analysis"}
    ]
    
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                    <div class='feature-card'>
                        <div style="font-size:24px">{feature['icon']}</div>
                        <div>{feature['name']}</div>
                    </div>
                """, unsafe_allow_html=True)

# Main page layout
st.title("⚡ FitSynapse")
st.markdown("Leverage data-driven insights to optimize your fitness journey")

# NEW: Real-time Activity Tracker
with st.container():
    st.header("🎯 Real-time Activity Monitor")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="card pulse-animation">
                <h3>Live Heart Rate</h3>
                <div class="metric-value">72 BPM</div>
                <p>Normal resting rate</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="card">
                <h3>Active Calories</h3>
                <div class="metric-value">412</div>
                <p>Calories burned today</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="card">
                <h3>Step Count</h3>
                <div class="metric-value">8,542</div>
                <p>85% of daily goal</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class="card">
                <h3>Sleep Score</h3>
                <div class="metric-value">87</div>
                <p>Quality sleep achieved</p>
            </div>
        """, unsafe_allow_html=True)

# User Input Section
with st.container():
    st.header("📋 Fitness Profile")
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.subheader("Personal Stats")
        age = st.slider('Age', 1, 100, 28, help="Your current age")
        weight = st.number_input('Weight (kg)', 40, 200, 75)
        height = st.number_input('Height (cm)', 120, 220, 175)
        
    with col2:
        st.subheader("Activity Metrics")
        duration = st.slider('Workout Duration (min)', 1, 180, 45)
        heart_rate = st.slider('Heart Rate (BPM)', 50, 200, 125)
        steps = st.slider('Daily Steps', 1000, 25000, 8500)
        
    with col3:
        st.subheader("Body Composition")
        body_fat = st.slider('Body Fat %', 5, 50, 18)
        muscle_mass = st.slider('Muscle Mass %', 30, 90, 65)
        gender = st.radio("Gender", ("Male", "Female", "Other"))
        
    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    bmi_status = "Healthy" if 18.5 <= bmi <= 24.9 else "Needs improvement"
    st.info(f"**Your BMI:** {bmi:.1f} - {bmi_status}")

# NEW: Workout Planner Section
with st.container():
    st.header("🏋️ Smart Workout Planner")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Today's Recommended Workout")
        workout_type = st.selectbox("Workout Focus", ["Cardio", "Strength", "HIIT", "Yoga", "Recovery"])
        
        if workout_type == "Cardio":
            st.markdown("""
            <div class="workout-card">
                <h4>🏃‍♂️ Cardio Blast</h4>
                <p>• 30 min Running (moderate pace)</p>
                <p>• 15 min Cycling (high intensity)</p>
                <p>• 10 min Jump Rope intervals</p>
                <p>🔥 Estimated burn: 450 calories</p>
            </div>
            """, unsafe_allow_html=True)
        elif workout_type == "Strength":
            st.markdown("""
            <div class="workout-card">
                <h4>💪 Strength Training</h4>
                <p>• 4x10 Bench Press</p>
                <p>• 3x12 Squats</p>
                <p>• 3x15 Deadlifts</p>
                <p>• 3x12 Shoulder Press</p>
                <p>🔥 Estimated burn: 380 calories</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Weekly Progress")
        # Weekly progress chart
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        completion = [85, 90, 75, 95, 80, 65, 70]
        
        fig = go.Figure(data=[
            go.Bar(name='Completion %', x=days, y=completion, 
                  marker_color=PRIMARY_COLOR)
        ])
        fig.update_layout(
            title="Weekly Workout Completion",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

# NEW: Nutrition Tracking Section
with st.container():
    st.header("🍎 Nutrition & Hydration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Nutrition")
        nutrition_data = {
            'Macro': ['Protein', 'Carbs', 'Fats'],
            'Current': [120, 250, 65],
            'Target': [140, 300, 70]
        }
        df_nutrition = pd.DataFrame(nutrition_data)
        
        fig = px.bar(df_nutrition, x='Macro', y=['Current', 'Target'], 
                    barmode='group', title="Macronutrient Intake")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Hydration Tracker")
        water_intake = st.slider("Water Intake (ml)", 0, 4000, 2100, 100)
        st.markdown(f"""
        <div class="nutrition-card">
            <h4>💧 Hydration Status</h4>
            <p>Current: {water_intake}ml / 3000ml</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {water_intake/3000*100}%"></div>
            </div>
            <p>{'👍 Good job!' if water_intake >= 2000 else '💪 Keep drinking!'}</p>
        </div>
        """, unsafe_allow_html=True)

# Prediction Section
with st.container():
    st.header("🔥 Calories Burned Prediction")
    
    # Simulate processing
    with st.spinner("Analyzing your metrics with AI..."):
        time.sleep(1.5)
    
    # Create metrics cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <h3>Estimated Calories</h3>
                <div class="metric-value">412 kcal</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: 65%"></div>
                </div>
                <p>65% of daily goal</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="card">
                <h3>Metabolic Rate</h3>
                <div class="metric-value">1,850 kcal</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: 82%"></div>
                </div>
                <p>Daily energy expenditure</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="card">
                <h3>Fitness Score</h3>
                <div class="metric-value">86/100</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: 86%"></div>
                </div>
                <p>Excellent condition</p>
            </div>
        """, unsafe_allow_html=True)

# NEW: Achievements & Challenges Section
with st.container():
    st.header("🏆 Achievements & Challenges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Achievements")
        achievements = [
            {"icon": "🔥", "name": "7-Day Streak", "earned": True},
            {"icon": "💪", "name": "First 10K", "earned": True},
            {"icon": "🏃", "name": "Marathon Ready", "earned": False},
            {"icon": "🧘", "name": "Yoga Master", "earned": True},
            {"icon": "🏆", "name": "Elite Status", "earned": False}
        ]
        
        for achievement in achievements:
            status = "✅" if achievement["earned"] else "⏳"
            st.markdown(f"{status} {achievement['icon']} {achievement['name']}")
    
    with col2:
        st.subheader("Active Challenges")
        for challenge in st.session_state.challenges:
            progress_percent = (challenge['progress'] / challenge['target']) * 100
            st.markdown(f"""
            <div class="challenge-card">
                <h4>{challenge['name']}</h4>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress_percent}%"></div>
                </div>
                <p>{challenge['progress']}% Complete</p>
            </div>
            """, unsafe_allow_html=True)

# Visualization Section
with st.container():
    st.header("📊 Performance Analytics")
    
    # Generate fitness data
    dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
    activity_data = pd.DataFrame({
        'Date': dates,
        'Calories Burned': np.random.randint(300, 600, 7),
        'Workout Duration': np.random.randint(20, 90, 7),
        'Steps': np.random.randint(5000, 15000, 7),
        'Heart Rate': np.random.randint(110, 160, 7)
    })
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Weekly Trend", "Body Composition", "Performance Metrics", "Sleep Analysis"])
    
    with tab1:
        fig = px.line(activity_data, x='Date', y='Calories Burned', 
                      title='Weekly Calories Burned', markers=True)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        body_data = pd.DataFrame({
            'Metric': ['Body Fat', 'Muscle Mass', 'Hydration', 'Bone Density'],
            'Value': [18, 65, 72, 92],
            'Target': [15, 70, 80, 95]
        })
        fig = px.bar(body_data, x='Metric', y=['Value', 'Target'], barmode='group',
                     title='Body Composition Analysis')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        fig = px.scatter(activity_data, x='Workout Duration', y='Calories Burned', 
                         size='Heart Rate', color='Steps',
                         title='Workout Efficiency Analysis')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab4:
        # NEW: Sleep Analysis
        sleep_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Hours': [7.5, 6.8, 7.2, 8.1, 7.0, 8.5, 7.8],
            'Quality': [85, 75, 80, 90, 78, 92, 88]
        })
        fig = px.line(sleep_data, x='Day', y=['Hours', 'Quality'], 
                      title='Weekly Sleep Analysis', markers=True)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

# Health Insights
with st.container():
    st.header("💡 AI-Powered Health Insights")
    
    cols = st.columns(2)
    with cols[0]:
        with st.expander("📌 Nutritional Recommendations", expanded=True):
            st.markdown("""
            - **Increase protein intake** to 1.8g/kg body weight for muscle recovery
            - **Hydration target:** 3L water daily (currently at 2.1L)
            - **Add superfoods:** Chia seeds, blueberries, spinach
            - **Supplement suggestion:** Omega-3 and Vitamin D3
            """)
            
    with cols[1]:
        with st.expander("🏋️ Workout Optimization", expanded=True):
            st.markdown("""
            - **Optimal workout window:** 6:00-8:00 AM (based on chronotype)
            - **Recovery suggestion:** Add yoga 2x/week for flexibility
            - **New exercise:** Try kettlebell swings for core activation
            - **Progress plateau:** Increase weights by 5% next week
            """)
    
    # NEW: AI Recommendation Button with enhanced functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("💡 **AI Recommendation:** Increase cardio duration by 15% to reach your calorie target faster. Consider adding HIIT workouts 3x/week.")
    with col2:
        if st.button("🔄 Generate New AI Insights", use_container_width=True):
            st.balloons()
            st.success("New AI insights generated! Check your recommendations.")

# NEW: Community & Social Features
with st.container():
    st.header("🤝 Fitness Community")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Global Rank", "#1,247", "↑ 15")
    with col2:
        st.metric("Friends", "28", "↑ 3")
    with col3:
        st.metric("Weekly Challenges", "5", "Active")
    
    st.button("Join Community Challenge", use_container_width=True)

# Footer Section
st.markdown("---")
st.markdown("""
    <footer>
        <p>Developed with ❤️ using Streamlit | FitMetrics Pro v397.0</p>
        <p>© 2024 ASWINI DEVI MEDISETTI. All Rights Reserved. | Privacy Policy | Terms of Service</p>
    </footer>
""", unsafe_allow_html=True)

# Instructions for background image
st.sidebar.markdown("---")
st.sidebar.info("""
**To add background image:**
1. Save a fitness image as 'bg.jpg'
2. Place it in same folder
3. Uncomment the add_bg_from_local() call
""")

# Uncomment below and add your background image file
# add_bg_from_local('bg.jpg')