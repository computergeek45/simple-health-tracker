import streamlit as st
from datetime import datetime, timedelta
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Health Tracker Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for ultra-modern, functional design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background with animated gradient */
    .main {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Modern card design */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.25);
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    
    /* Headers with modern styling */
    h1 {
        color: white !important;
        font-weight: 900 !important;
        font-size: 4rem !important;
        text-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.5rem !important;
        letter-spacing: -2px;
    }
    
    h2 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h3 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        text-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
        margin-top: 1.5rem !important;
    }
    
    /* Modern button design */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 18px 40px;
        font-weight: 700;
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(-2px);
    }
    
    /* Input fields with modern design */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        color: white;
        font-weight: 500;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        padding: 14px 18px;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        transform: scale(1.02);
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Slider with gradient */
    .stSlider>div>div>div {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .stSlider>div>div>div>div>div {
        background: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        width: 24px;
        height: 24px;
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 12px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 14px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 700;
        padding: 14px 32px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Expander with modern styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        color: white !important;
        font-weight: 700;
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 18px 24px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateX(8px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 24px;
        margin-top: 8px;
    }
    
    /* Sidebar with gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] h2 {
        font-size: 1.5rem !important;
    }
    
    /* Alert boxes with modern design */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 2px solid rgba(16, 185, 129, 0.5);
        padding: 20px;
        color: white;
        font-weight: 600;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2));
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 2px solid rgba(59, 130, 246, 0.5);
        padding: 20px;
        color: white;
        font-weight: 600;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.2));
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 2px solid rgba(245, 158, 11, 0.5);
        padding: 20px;
        color: white;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2));
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 2px solid rgba(239, 68, 68, 0.5);
        padding: 20px;
        color: white;
        font-weight: 600;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        letter-spacing: 0.5px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.3);
        margin: 40px 0;
        border-width: 2px;
    }
    
    /* Select slider */
    .stSelectSlider>div>div>div {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        padding: 8px;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 28px;
        margin: 16px 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .recommendation-card h4 {
        color: white;
        font-weight: 800;
        font-size: 1.3rem;
        margin-bottom: 12px;
    }
    
    .recommendation-card p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    /* Progress bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        height: 32px;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .progress-bar {
        height: 100%;
        transition: width 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 16px;
        font-weight: 800;
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        font-size: 0.95rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing data
if 'health_data' not in st.session_state:
    st.session_state.health_data = []

# Helper function to save data
def add_health_entry(mood, energy, sleep, water, exercise, notes):
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'mood': mood,
        'energy': energy,
        'sleep': sleep,
        'water': water,
        'exercise': exercise,
        'notes': notes
    }
    st.session_state.health_data.append(entry)
    return True

# Helper function to get mood score
def get_mood_score(mood):
    mood_scores = {
        "Very Bad": 1,
        "Bad": 2,
        "Neutral": 3,
        "Good": 4,
        "Excellent": 5
    }
    return mood_scores.get(mood, 3)

# Helper function to generate personalized recommendations
def generate_recommendations(avg_energy, avg_sleep, avg_water, avg_exercise, avg_mood_score):
    recommendations = []
    
    # Sleep recommendations
    if avg_sleep < 6:
        recommendations.append({
            'icon': '😴',
            'title': 'Critical: Improve Your Sleep',
            'description': f'You\'re averaging {avg_sleep:.1f} hours of sleep. This is significantly below the recommended 7-9 hours.',
            'action': 'Try setting a consistent bedtime, avoid screens 1 hour before sleep, and create a dark, cool sleeping environment.',
            'priority': 'high'
        })
    elif avg_sleep < 7:
        recommendations.append({
            'icon': '😴',
            'title': 'Increase Sleep Duration',
            'description': f'You\'re getting {avg_sleep:.1f} hours of sleep. Aim for 7-9 hours for optimal recovery.',
            'action': 'Try going to bed 30 minutes earlier and establish a relaxing bedtime routine.',
            'priority': 'medium'
        })
    elif avg_sleep > 9:
        recommendations.append({
            'icon': '😴',
            'title': 'Monitor Sleep Quality',
            'description': f'You\'re sleeping {avg_sleep:.1f} hours. While rest is important, oversleeping can indicate other issues.',
            'action': 'Consider tracking sleep quality and consult a healthcare provider if you still feel tired.',
            'priority': 'medium'
        })
    
    # Water recommendations
    if avg_water < 6:
        recommendations.append({
            'icon': '💧',
            'title': 'Hydration Alert',
            'description': f'You\'re only drinking {avg_water:.1f} glasses of water daily. This is below the recommended 8 glasses.',
            'action': 'Set hourly reminders to drink water, keep a water bottle nearby, and flavor water with lemon if needed.',
            'priority': 'high'
        })
    elif avg_water < 8:
        recommendations.append({
            'icon': '💧',
            'title': 'Boost Hydration',
            'description': f'You\'re drinking {avg_water:.1f} glasses daily. You\'re close to the goal of 8 glasses!',
            'action': 'Add one glass of water with each meal to reach your hydration goal.',
            'priority': 'low'
        })
    
    # Exercise recommendations
    if avg_exercise < 20:
        recommendations.append({
            'icon': '🏃',
            'title': 'Start Moving More',
            'description': f'You\'re averaging {avg_exercise:.0f} minutes of exercise. WHO recommends 150 minutes per week (about 20-30 min/day).',
            'action': 'Start with 10-minute walks after meals, take stairs instead of elevators, or try desk exercises.',
            'priority': 'high'
        })
    elif avg_exercise < 30:
        recommendations.append({
            'icon': '🏃',
            'title': 'Increase Physical Activity',
            'description': f'You\'re exercising {avg_exercise:.0f} minutes daily. You\'re making progress!',
            'action': 'Gradually increase to 30 minutes daily with activities you enjoy - dancing, cycling, or swimming.',
            'priority': 'medium'
        })
    elif avg_exercise >= 60:
        recommendations.append({
            'icon': '🏃',
            'title': 'Excellent Exercise Routine!',
            'description': f'Amazing! You\'re exercising {avg_exercise:.0f} minutes daily.',
            'action': 'Ensure you\'re incorporating rest days and varying your workout intensity to prevent burnout.',
            'priority': 'low'
        })
    
    # Energy recommendations
    if avg_energy < 4:
        recommendations.append({
            'icon': '⚡',
            'title': 'Address Low Energy Levels',
            'description': f'Your energy is averaging {avg_energy:.1f}/10. This may indicate underlying issues.',
            'action': 'Review your sleep, nutrition, and stress levels. Consider consulting a healthcare provider.',
            'priority': 'high'
        })
    elif avg_energy < 6:
        recommendations.append({
            'icon': '⚡',
            'title': 'Boost Your Energy',
            'description': f'Your energy is at {avg_energy:.1f}/10. There\'s room for improvement.',
            'action': 'Focus on regular meals, stay hydrated, take short breaks during work, and get morning sunlight.',
            'priority': 'medium'
        })
    
    # Mood recommendations
    if avg_mood_score < 2.5:
        recommendations.append({
            'icon': '😊',
            'title': 'Mood Support Needed',
            'description': f'Your mood has been consistently low. Your wellbeing matters.',
            'action': 'Consider talking to a mental health professional, practice mindfulness, and connect with supportive friends.',
            'priority': 'high'
        })
    elif avg_mood_score < 3.5:
        recommendations.append({
            'icon': '😊',
            'title': 'Elevate Your Mood',
            'description': 'Your mood could use a boost. Small changes can make a big difference.',
            'action': 'Try gratitude journaling, spend time in nature, engage in hobbies, or practice meditation.',
            'priority': 'medium'
        })
    
    # Positive reinforcements
    if avg_energy >= 7 and avg_sleep >= 7 and avg_water >= 8:
        recommendations.append({
            'icon': '🌟',
            'title': 'Outstanding Health Habits!',
            'description': 'You\'re crushing it! Your sleep, hydration, and energy levels are all excellent.',
            'action': 'Keep up the amazing work! Consider sharing your routine with others to inspire them.',
            'priority': 'success'
        })
    elif avg_exercise >= 30 and avg_mood_score >= 4:
        recommendations.append({
            'icon': '💪',
            'title': 'Great Physical & Mental Health!',
            'description': 'Your exercise routine and positive mood are serving you well.',
            'action': 'Maintain this balance and consider setting new fitness goals to stay motivated.',
            'priority': 'success'
        })
    
    # If no specific recommendations
    if not recommendations:
        recommendations.append({
            'icon': '✨',
            'title': 'Maintain Your Balance',
            'description': 'Your health metrics are looking good! Keep monitoring your progress.',
            'action': 'Continue tracking daily to identify patterns and maintain your healthy habits.',
            'priority': 'low'
        })
    
    return recommendations

# Header with modern styling
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("🏥 Health Tracker")
    st.markdown("<p style='color: rgba(255,255,255,0.9); font-size: 1.2rem; font-weight: 500; margin-top: -10px;'>Track your wellness journey with intelligent insights</p>", unsafe_allow_html=True)
with col_header2:
    st.markdown(f"<div style='text-align: right; color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 30px; font-weight: 600;'>📅 {datetime.now().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Log Entry", "📊 Dashboard", "📈 Insights"])

# Tab 1: Log Entry
with tab1:
    st.markdown("## Record Your Daily Health")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        mood = st.select_slider(
            "😊 Mood",
            options=["Very Bad", "Bad", "Neutral", "Good", "Excellent"],
            value="Neutral"
        )
        
        energy = st.slider("⚡ Energy Level", 0, 10, 5)
        
        sleep = st.number_input("😴 Hours of Sleep", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    
    with col2:
        water = st.number_input("💧 Water Intake (glasses)", min_value=0, max_value=20, value=8)
        
        exercise = st.number_input("🏃 Exercise (minutes)", min_value=0, max_value=300, value=30)
        
        notes = st.text_area("📝 Notes", placeholder="How are you feeling today? Any observations...", height=100)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💾 Save Entry", use_container_width=True):
        if add_health_entry(mood, energy, sleep, water, exercise, notes):
            st.success("✅ Health entry saved successfully!")
            st.balloons()

# Tab 2: Dashboard
with tab2:
    st.markdown("## Your Health Overview")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.health_data:
        # Get latest entry
        latest = st.session_state.health_data[-1]
        
        # Display metrics in a modern grid
        col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
        
        with col1:
            st.metric("😊 Mood", latest['mood'])
        with col2:
            st.metric("⚡ Energy", f"{latest['energy']}/10")
        with col3:
            st.metric("😴 Sleep", f"{latest['sleep']}h")
        with col4:
            st.metric("💧 Water", f"{latest['water']} 🥤")
        with col5:
            st.metric("🏃 Exercise", f"{latest['exercise']}m")
        
        st.markdown("---")
        
        # Recent entries with modern cards
        st.markdown("### 📋 Recent Entries")
        st.markdown("<br>", unsafe_allow_html=True)
        
        for entry in reversed(st.session_state.health_data[-5:]):
            with st.expander(f"📅 {entry['date']} • {entry['mood']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**😊 Mood:** {entry['mood']}")
                    st.markdown(f"**⚡ Energy:** {entry['energy']}/10")
                with col2:
                    st.markdown(f"**😴 Sleep:** {entry['sleep']} hours")
                    st.markdown(f"**💧 Water:** {entry['water']} glasses")
                with col3:
                    st.markdown(f"**🏃 Exercise:** {entry['exercise']} minutes")
                
                if entry['notes']:
                    st.markdown("---")
                    st.markdown(f"**📝 Notes:** {entry['notes']}")
    else:
        st.info("📝 No health data yet. Start logging your entries in the 'Log Entry' tab!")

# Tab 3: Insights
with tab3:
    st.markdown("## 📈 Health Insights & Recommendations")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(st.session_state.health_data) >= 1:
        # Calculate averages
        avg_energy = sum(e['energy'] for e in st.session_state.health_data) / len(st.session_state.health_data)
        avg_sleep = sum(e['sleep'] for e in st.session_state.health_data) / len(st.session_state.health_data)
        avg_water = sum(e['water'] for e in st.session_state.health_data) / len(st.session_state.health_data)
        avg_exercise = sum(e['exercise'] for e in st.session_state.health_data) / len(st.session_state.health_data)
        avg_mood_score = sum(get_mood_score(e['mood']) for e in st.session_state.health_data) / len(st.session_state.health_data)
        
        # Top metrics row
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.metric("⚡ Avg Energy", f"{avg_energy:.1f}/10")
        with col2:
            st.metric("😴 Avg Sleep", f"{avg_sleep:.1f}h")
        with col3:
            st.metric("💧 Avg Water", f"{avg_water:.1f} 🥤")
        with col4:
            st.metric("🏃 Avg Exercise", f"{avg_exercise:.0f}m")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Wellness score
        wellness_score = (
            (avg_energy / 10) * 25 +
            (min(avg_sleep / 8, 1)) * 25 +
            (min(avg_water / 8, 1)) * 25 +
            (min(avg_exercise / 30, 1)) * 25
        ) * 100
        
        col_score1, col_score2, col_score3 = st.columns([1, 2, 1])
        with col_score2:
            st.markdown("### 💪 Overall Wellness Score")
            st.metric("", f"{wellness_score:.0f}%", delta=None)
            
            # Progress bar visualization
            progress_color = "linear-gradient(90deg, #10b981, #059669)" if wellness_score >= 70 else "linear-gradient(90deg, #f59e0b, #d97706)" if wellness_score >= 50 else "linear-gradient(90deg, #ef4444, #dc2626)"
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="background: {progress_color}; width: {wellness_score}%;">
                    {wellness_score:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Personalized Recommendations
        st.markdown("### 💡 Personalized Recommendations")
        st.markdown("<br>", unsafe_allow_html=True)
        
        recommendations = generate_recommendations(avg_energy, avg_sleep, avg_water, avg_exercise, avg_mood_score)
        
        # Display recommendations in cards
        for rec in recommendations:
            priority_colors = {
                'high': 'rgba(239, 68, 68, 0.3)',
                'medium': 'rgba(245, 158, 11, 0.3)',
                'low': 'rgba(59, 130, 246, 0.3)',
                'success': 'rgba(16, 185, 129, 0.3)'
            }
            
            border_colors = {
                'high': 'rgba(239, 68, 68, 0.6)',
                'medium': 'rgba(245, 158, 11, 0.6)',
                'low': 'rgba(59, 130, 246, 0.6)',
                'success': 'rgba(16, 185, 129, 0.6)'
            }
            
            bg_color = priority_colors.get(rec['priority'], 'rgba(255, 255, 255, 0.15)')
            border_color = border_colors.get(rec['priority'], 'rgba(255, 255, 255, 0.3)')
            
            st.markdown(f"""
            <div class="recommendation-card" style="background: {bg_color}; border-color: {border_color};">
                <h4>{rec['icon']} {rec['title']}</h4>
                <p><strong>Insight:</strong> {rec['description']}</p>
                <p><strong>Action:</strong> {rec['action']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Stats footer
        st.markdown("---")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.markdown(f"<p style='color: white; font-size: 1.1rem; font-weight: 600;'>📊 Total Entries: {len(st.session_state.health_data)}</p>", unsafe_allow_html=True)
        with stat_col2:
            st.markdown(f"<p style='color: white; font-size: 1.1rem; font-weight: 600;'>📅 Days Tracked: {len(st.session_state.health_data)}</p>", unsafe_allow_html=True)
        with stat_col3:
            if st.session_state.health_data:
                first_date = datetime.strptime(st.session_state.health_data[0]['date'], '%Y-%m-%d %H:%M')
                days_since = (datetime.now() - first_date).days + 1
                st.markdown(f"<p style='color: white; font-size: 1.1rem; font-weight: 600;'>🔥 Journey: {days_since} day{'s' if days_since != 1 else ''}</p>", unsafe_allow_html=True)
        
    else:
        st.info("📊 Start logging entries to see personalized insights and recommendations!")

# Sidebar with modern styling
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.health_data = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    st.markdown(f"**Entries:** {len(st.session_state.health_data)}")
    
    if st.session_state.health_data:
        st.markdown(f"**Latest:** {st.session_state.health_data[-1]['date']}")
        avg_energy = sum(e['energy'] for e in st.session_state.health_data) / len(st.session_state.health_data)
        st.markdown(f"**Avg Energy:** {avg_energy:.1f}/10")
    
    st.markdown("---")
    
    st.markdown("### 📖 About")
    st.markdown("""
    This Health Tracker helps you monitor:
    
    • 😊 Daily mood  
    • ⚡ Energy levels  
    • 😴 Sleep patterns  
    • 💧 Water intake  
    • 🏃 Exercise activity
    
    **Get personalized recommendations based on your data!**
    """)
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; opacity: 0.7; font-size: 0.85rem;'>Made with ❤️ for your wellness</div>", unsafe_allow_html=True)