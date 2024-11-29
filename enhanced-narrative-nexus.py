# app.py
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time
import random

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'history' not in st.session_state:
    st.session_state.history = []

def save_to_history(content_type, content):
    """Save generated content to history"""
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': content_type,
        'content': content
    })

def generate_story(prompt, genre, length, style, tone):
    """Generate a story with enhanced parameters"""
    story_prompt = f"""Write a {genre} story that is approximately {length} words long.
    Style: {style}
    Tone: {tone}
    Story prompt: {prompt}
    Please ensure the story has a clear beginning, middle, and end, with engaging character development."""
    response = model.generate_content(story_prompt)
    return response.text

def generate_script(prompt, format, num_characters, genre, tone):
    """Generate a script with enhanced parameters"""
    script_prompt = f"""Create a {format} script in {genre} genre with {num_characters} characters.
    Tone: {tone}
    Premise: {prompt}
    Include character descriptions, stage directions, and dialogue formatting."""
    response = model.generate_content(script_prompt)
    return response.text

def generate_character(name, archetype, background, goals, conflicts):
    """Generate detailed character profile"""
    character_prompt = f"""Create a detailed character profile for {name}
    Archetype: {archetype}
    Background: {background}
    Goals: {goals}
    Internal/External Conflicts: {conflicts}
    
    Include:
    - Physical description
    - Personality traits
    - Motivations
    - Relationships
    - Character arc potential"""
    response = model.generate_content(character_prompt)
    return response.text

def generate_world(setting_type, culture, magic_system, technology, conflicts):
    """Generate world-building details"""
    world_prompt = f"""Create a detailed world setting with the following parameters:
    Setting Type: {setting_type}
    Culture: {culture}
    Magic System: {magic_system}
    Technology Level: {technology}
    Major Conflicts: {conflicts}
    
    Include:
    - Geography and climate
    - Social structure
    - Economic system
    - History and lore
    - Unique features"""
    response = model.generate_content(world_prompt)
    return response.text

def generate_dialogue(characters, situation, tone, length):
    """Generate realistic dialogue"""
    dialogue_prompt = f"""Write a dialogue scene between {characters} in the following situation:
    {situation}
    Tone: {tone}
    Length: {length} exchanges
    
    Focus on natural conversation flow and character voice."""
    response = model.generate_content(dialogue_prompt)
    return response.text

def poetry_generator(theme, style, length):
    """Generate poetry"""
    poetry_prompt = f"""Create a {style} poem about {theme}
    Length: {length} lines
    Include literary devices and meaningful imagery."""
    response = model.generate_content(poetry_prompt)
    return response.text

# UI Configuration
st.set_page_config(
    page_title="NarrativeNexus Pro",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .success-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎭 NarrativeNexus Pro")
st.sidebar.markdown("---")

# User Projects Section
with st.sidebar.expander("📁 My Projects", expanded=False):
    project_name = st.text_input("Project Name")
    if st.button("Create Project"):
        st.session_state.projects.append({
            'name': project_name,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': []
        })

# Navigation
mode = st.sidebar.selectbox(
    "Create",
    ["🏠 Dashboard", "📖 Story Generator", "🎬 Script Writer", 
     "👤 Character Creator", "🌍 World Builder", "💭 Dialogue Generator",
     "📝 Poetry Studio", "📚 Content Library"]
)

if mode == "🏠 Dashboard":
    st.title("Welcome to NarrativeNexus Pro")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Stories Created", len([x for x in st.session_state.history if x['type'] == 'story']))
    with col2:
        st.metric("Characters Created", len([x for x in st.session_state.history if x['type'] == 'character']))
    with col3:
        st.metric("Scripts Written", len([x for x in st.session_state.history if x['type'] == 'script']))
    with col4:
        st.metric("Total Projects", len(st.session_state.projects))
    
    # Recent Activity
    st.subheader("Recent Activity")
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"**{item['type'].title()}** created at {item['timestamp']}")

elif mode == "📖 Story Generator":
    st.title("Story Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        story_prompt = st.text_area("Story Premise", height=100)
        genre = st.selectbox("Genre", [
            "Fantasy", "Science Fiction", "Romance", "Mystery", 
            "Horror", "Adventure", "Historical Fiction", "Literary Fiction",
            "Thriller", "Comedy", "Drama"
        ])
        style = st.selectbox("Writing Style", [
            "Descriptive", "Minimalist", "Stream of Consciousness",
            "Experimental", "Classical", "Modern"
        ])
    
    with col2:
        length = st.select_slider(
            "Story Length (words)",
            options=[1000, 2000, 3000, 4000, 5000]
        )
        tone = st.select_slider(
            "Tone",
            options=["Dark", "Neutral", "Light", "Humorous", "Dramatic"]
        )
    
    if st.button("Generate Story"):
        with st.spinner("Crafting your story..."):
            story = generate_story(story_prompt, genre, length, style, tone)
            save_to_history('story', story)
            st.markdown("### Your Story")
            st.write(story)
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save to Project"):
                    if st.session_state.projects:
                        project_idx = st.selectbox("Select Project", range(len(st.session_state.projects)))
                        st.session_state.projects[project_idx]['content'].append({
                            'type': 'story',
                            'content': story,
                            'metadata': {
                                'genre': genre,
                                'length': length,
                                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        })
            with col2:
                st.download_button(
                    label="Download Story",
                    data=story,
                    file_name=f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

elif mode == "🎬 Script Writer":
    st.title("Script Writer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        script_prompt = st.text_area("Script Premise")
        format = st.selectbox("Format", [
            "Movie", "TV Episode", "Short Film", "Theater Play",
            "Radio Play", "Web Series", "Animation"
        ])
        genre = st.selectbox("Genre", [
            "Drama", "Comedy", "Action", "Romance", "Thriller",
            "Science Fiction", "Horror", "Musical"
        ])
    
    with col2:
        num_characters = st.number_input("Number of Characters", 2, 10, 4)
        tone = st.select_slider(
            "Tone",
            options=["Dark", "Neutral", "Light", "Humorous", "Dramatic"]
        )
    
    if st.button("Generate Script"):
        with st.spinner("Writing your script..."):
            script = generate_script(script_prompt, format, num_characters, genre, tone)
            save_to_history('script', script)
            st.markdown("### Your Script")
            st.text(script)

elif mode == "👤 Character Creator":
    st.title("Character Creator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        character_name = st.text_input("Character Name")
        archetype = st.selectbox("Character Archetype", [
            "Hero", "Mentor", "Sidekick", "Antagonist", "Anti-hero",
            "Trickster", "Love Interest", "Wise Old Man/Woman"
        ])
        background = st.text_area("Character Background")
    
    with col2:
        goals = st.text_area("Character Goals")
        conflicts = st.text_area("Internal/External Conflicts")
    
    if st.button("Generate Character Profile"):
        with st.spinner("Creating character profile..."):
            profile = generate_character(character_name, archetype, background, goals, conflicts)
            save_to_history('character', profile)
            st.markdown("### Character Profile")
            st.write(profile)

elif mode == "🌍 World Builder":
    st.title("World Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        setting_type = st.selectbox("Setting Type", [
            "Fantasy Realm", "Future Earth", "Alternate History",
            "Space Colony", "Post-Apocalyptic", "Urban Fantasy"
        ])
        culture = st.text_area("Cultural Elements")
        magic_system = st.text_area("Magic/Technology System")
    
    with col2:
        technology = st.select_slider(
            "Technology Level",
            options=["Primitive", "Medieval", "Industrial", "Modern", "Future", "Advanced"]
        )
        conflicts = st.text_area("Major Conflicts")
    
    if st.button("Generate World"):
        with st.spinner("Creating your world..."):
            world = generate_world(setting_type, culture, magic_system, technology, conflicts)
            save_to_history('world', world)
            st.markdown("### World Description")
            st.write(world)

elif mode == "💭 Dialogue Generator":
    st.title("Dialogue Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        characters = st.text_input("Characters (comma-separated)")
        situation = st.text_area("Situation/Context")
    
    with col2:
        tone = st.select_slider(
            "Tone",
            options=["Formal", "Casual", "Tense", "Romantic", "Humorous"]
        )
        length = st.number_input("Number of Exchanges", 3, 20, 10)
    
    if st.button("Generate Dialogue"):
        with st.spinner("Creating dialogue..."):
            dialogue = generate_dialogue(characters, situation, tone, length)
            save_to_history('dialogue', dialogue)
            st.markdown("### Dialogue")
            st.write(dialogue)

elif mode == "📝 Poetry Studio":
    st.title("Poetry Studio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.text_input("Theme/Subject")
        style = st.selectbox("Poetry Style", [
            "Sonnet", "Haiku", "Free Verse", "Limerick",
            "Ballad", "Ode", "Villanelle"
        ])
    
    with col2:
        length = st.number_input("Number of Lines", 3, 50, 14)
    
    if st.button("Generate Poem"):
        with st.spinner("Creating poetry..."):
            poem = poetry_generator(theme, style, length)
            save_to_history('poem', poem)
            st.markdown("### Your Poem")
            st.write(poem)

elif mode == "📚 Content Library":
    st.title("Content Library")
    
    # Filter options
    content_type = st.selectbox(
        "Filter by Type",
        ["All", "Story", "Script", "Character", "World", "Dialogue", "Poem"]
    )
    
    # Display history with filters
    for item in reversed(st.session_state.history):
        if content_type == "All" or content_type.lower() == item['type']:
            with st.expander(f"{item['type'].title()} - {item['timestamp']}"):
                st.write(item['content'])
                if st.button(f"Delete {item['timestamp']}", key=f"del_{item['timestamp']}"):
                    st.session_state.history.remove(item)
                    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by NarrativeNexus Pro</p>
        <p>Powered by Gemini AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
