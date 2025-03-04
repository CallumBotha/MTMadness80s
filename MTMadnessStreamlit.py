import random
import requests
import os
from rapidfuzz import fuzz
import streamlit as st

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Music Trivia Madness",
    layout="wide",
    page_icon="🎵",
    initial_sidebar_state="collapsed"
)

input_folder = "https://github.com/CallumBotha/MTMadness80s/tree/main/Question1"
output_folder = "https://github.com/CallumBotha/MTMadness80s/tree/main/Question1/Question1Trimmed"

music_data = []

for filename in input_folder
    if filename.endswith('.mp3'):
        artist_song = filename.replace('.mp3', '').split(' - ')
        if len(artist_song) == 2:
            artist_name, song_name = artist_song
            original_file_url = f"{input_folder}/{filename}"  # Full song URL
            trimmed_file_url = f"{output_folder}/{filename}"  # Trimmed song URL

            response = requests.head(trimmed_file_url)  # Check if the trimmed file exists on GitHub
            if response.status_code != 200:
                # If the file doesn't exist, you could flag or log it, but no trimming is done here.
                print(f"Trimmed version of {filename} not found!")
            music_data.append({
                'song': song_name,
                'artist': artist_name,
                'full_file': original_file_url,  # Full song URL
                'trimmed_file': trimmed_file_url  # Trimmed song URL
            })
# Example output of the music data list
for song in music_data:
    print(song)



# Display your headings, questions, and answers here
st.title("Music Trivia Madness!")
st.subheader("Guess the song and artist")
st.write("Answer the following questions by selecting the correct artist and song from the list below.")

# Example of your questions and answer boxes
question_1 = st.radio("Question 1: Who sings 'Song A'?", ["Artist A", "Artist B", "Artist C"])
question_2 = st.radio("Question 2: Who sings 'Song B'?", ["Artist D", "Artist E", "Artist F"])

# Display the questions and answers
st.write("Your answers: ")
st.write(f"Question 1: {question_1}")
st.write(f"Question 2: {question_2}")

# Display songs and allow users to play them
if music_data:
    for song_info in music_data:
        song_name = song_info['song']
        artist_name = song_info['artist']
        trimmed_file_url = song_info['trimmed_file']

        # Display song name and artist
        st.subheader(f"{song_name} by {artist_name}")
        
        # Display audio player for the full song
        st.audio(trimmed_file_url, format="audio/mp3", start_time=0)
        st.write("Trimmed version (Full song)")

else:
    st.error("Failed to retrieve music files from GitHub. Check folder path or API rate limits.")

# Ensure at least 5 songs before sampling
if len(music_data) >= 5:
    st.session_state.selected_songs = random.sample(music_data, 5)
else:
    st.session_state.selected_songs = music_data  # Use all available songs

# Custom CSS for styling
#background_url = "https://i.pinimg.com/1200x/01/9a/f5/019af5b99acc623a0dae65d4221dd33a.jpg"
background_url = "https://i.ibb.co/bRH8S1fr/A-seamless-sticker-bomb-collage-inspired-by-80s-music-culture-designed-like-retro-gift-wrap-Features.jpg"
# Custom CSS for styling
# Custom CSS for styling, including hiding anchor tags
st.markdown(
    f"""
    <style>
        a {{
            display: none !important;
        }}
        body {{
            background-image: url("{background_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .stApp {{
            background: none !important;
            padding: 20px;
            border-radius: 10px;
            margin-right: 10px;
            margin-left: 10px;
            margin-top: -110px;
            margin-bottom: 30px;
        }}
        .stMarkdown {{
            color: white !important;
            padding: 0px;
            margin-left: 10px;
            margin-right: 10px;
            margin-top: 50px;
            margin-bottom: 10px;
            border-radius: 10px;
        }}
        .stTextInput {{
            background: rgba(0, 0, 0, 0.93) !important;
            color: white !important;
            padding-left: 11px;
            padding-right: 11px;
            padding-bottom: 11px;
            padding-top: 3px;
            margin-left: 10px;
            margin-right: 10px;
            margin-top: 5px;
            margin-bottom: 5px;
            -webkit-text-stroke: 0.08px black;
            border: 1px solid black;
            border-radius: 10px;
        }}
        .stAudio {{
            background: rgba(0, 0, 0, 0.93) !important;
            padding-left: 10px;
            padding-right: 10px;
            padding-top: 10px;
            padding-bottom: 10px;
            margin-left: 10px;
            margin-right: 10px;
            margin-top: 10px;
            border: 1.3px solid black;
            border-radius: 10px;
        }}
        .stButton {{
            background: rgba(0, 0, 0, 0.93) !important;
            padding-left: 5px;
            padding-right: 5px;
            padding-top: 5px;
            padding-bottom: 5px;
            margin-left: 10px;
            margin-right: 10px;
            margin-top: 0px;
            border-radius: 10px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            background: rgba(0, 0, 0, 0.93) !important;
            padding: 10px;
            display: inline-block;
            border-radius: 10px;
        }}
        header {{
            visibility: hidden;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 40px; font-weight: bold; color: white; 
                  background-color: rgba(0, 0, 0, 0.5); padding: 20px; 
                  border-radius: 10px; display: inline-block;">
            🎵 Music Trivia Madness: 80s Edition! 🎵
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)



# Initialize session state variables
if 'selected_songs' not in st.session_state:
    st.session_state.selected_songs = random.sample(music_data, 5)
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [{} for _ in range(len(st.session_state.selected_songs))]
if 'game_completed' not in st.session_state:
    st.session_state.game_completed = False

# Function to reset game state
def reset_game():
    st.session_state.game_completed = False
    st.session_state.selected_songs = random.sample(music_data, 5)
    st.session_state.user_answers = [{} for _ in range(len(st.session_state.selected_songs))]

    # Clear input fields by resetting their keys
    for i in range(len(st.session_state.selected_songs)):
        st.session_state[f"song_input_{i}"] = ""
        st.session_state[f"artist_input_{i}"] = ""

    st.rerun()

selected_songs = st.session_state.selected_songs

# Game logic
for idx, entry in enumerate(selected_songs):
    correct_artist = entry['artist']
    correct_song = entry['song']
    trimmed_file_path = entry['trimmed_file']

    st.write(f"### Question {idx + 1}")

    # Display the 15-second preview for trivia
    if os.path.exists(trimmed_file_path):
        st.audio(trimmed_file_path)

    # Ask for the song's name with a unique key
    song_name = st.text_input(
        f" What is the name of the song?",
        key=f"song_input_{idx}",
        value=st.session_state.get(f"song_input_{idx}", ""),  # Retain value in session state
    )

    # Ask for the artist's name with a unique key
    artist_name = st.text_input(
        f" Who is the artist of the song?",
        key=f"artist_input_{idx}",
        value=st.session_state.get(f"artist_input_{idx}", ""),  # Retain value in session state
    )

    # Store answers temporarily in session_state
    st.session_state.user_answers[idx] = {
        'song': song_name,
        'artist': artist_name,
        'correct_song': correct_song,
        'correct_artist': correct_artist,
        'full_file': entry['full_file'],  # Store full song path
    }


# Display button to submit answers after all questions have been answered
submit_all = st.button("Submit All Answers")


# Check answers after the user has submitted all
if submit_all:
    correct_answers = 0
    responses = []  # Clear any previous responses

    # Check each answer
    for answer in st.session_state.user_answers:
        response = {}

        # Check the song answer
        SIMILARITY_THRESHOLD = 70  # Adjust as needed
        def is_close_enough(user_input, correct_answer):
            similarity = fuzz.ratio(user_input.lower(), correct_answer.lower())
            return similarity >= SIMILARITY_THRESHOLD

        if is_close_enough(answer['song'], answer['correct_song']):
            correct_answers += 1
            response['song_correct'] = True
        else:
            response['song_correct'] = False
            response['correct_song'] = answer['correct_song']
            response['your_song'] = answer['song']

        # Check the artist answer
        if is_close_enough(answer['artist'], answer['correct_artist']):
            correct_answers += 1
            response['artist_correct'] = True
        else:
            response['artist_correct'] = False
            response['correct_artist'] = answer['correct_artist']
            response['your_artist'] = answer['artist']

        response['full_file'] = answer['full_file']  # Include the full song file path
        responses.append(response)

    # Display final score
    def styled_text(text, color="white", background="rgba(0, 0, 0, 0.93)", margin_top="1px", margin_bottom="-100px", font_size="40px"):
        return f'<p style="background-color:{background}; color:{color}; padding:8px; border-radius:10px; margin-top:{margin_top}; margin-bottom:{margin_bottom}; font-size:{font_size};">{text}</p>'

    st.markdown(styled_text(f"🎉 Trivia Completed! Your total score: {correct_answers}/{len(selected_songs) * 2}", margin_top="1px", margin_bottom="1px"), unsafe_allow_html=True)


    # Mark game as completed
    st.session_state.game_completed = True
    st.markdown("\n### Review of your answers:")

    # Function to style text with a black background
    def styled_text(text, font_size = "20px", font_weight = "bold", color="white", padding = "20px", background="rgba(0, 0, 0, 0.93)", margin_top="-50px", margin_bottom="-50px"):
        return f"""
        <div style="
            font-size: {font_size};
            font-weight: {font_weight};
            color: {color};
            margin-top: {margin_top};
            margin-bottom: {margin_bottom};
            text-align: left;
            background: {background};
            padding: {padding};
            border-radius: 10px;
            margin-top: 60px;
        ">
           {text}
        </div>
        """
#    def styled_text(text, color="white", background="rgba(0, 0, 0, 0.93)", margin_top="-50px", margin_bottom="-50px"):
 #       return f'<p style="background-color:{background}; color:{color}; padding:8px; border-radius:5px; margin-top:{margin_top}; margin-bottom:{margin_bottom};">{text}</p>'

    # Review answers & provide full song playback buttons after both artist and song name answers are given
    for idx, response in enumerate(responses):
        song_correct = response.get('song_correct', False)
        artist_correct = response.get('artist_correct', False)

        # Get the user's actual input
        your_song = st.session_state.user_answers[idx]['song']
        your_artist = st.session_state.user_answers[idx]['artist']

        correct_song = response.get('correct_song', 'N/A')
        correct_artist = response.get('correct_artist', 'N/A')

        # Construct user's combined answer for fully correct and incorrect answers
        user_answer = f"{your_song} - {your_artist}"  # Song - Artist
        # Example of a styled text function with customizable font size
        def styled_text(text, font_size="20px", margin_top="-20px", margin_bottom="-30px", padding = "20px", color="white"):
            return f"""
            <div style="
                font-size: {font_size};
                color: {color};
                text-align: left;
                background: rgba(0, 0, 0, 0.93);
                padding: {padding};
                border-radius: 10px;
                margin-top: {margin_top};
                margin-bottom: {margin_bottom};
            ">
               {text}
            </div>
            """      
        # Determine the status of the answer
        if song_correct and artist_correct:
            st.markdown(styled_text(f" Question {idx + 1}: Correct! ✔️ Your answer: {user_answer}"), unsafe_allow_html=True)
        elif song_correct or artist_correct:
            st.markdown(styled_text(f" Question {idx + 1}: Half Correct! ⚠️ You got either the artist or song name correct."), unsafe_allow_html=True)
            if song_correct:
                st.markdown(styled_text(f" You got the song name correct ✔️: {your_song or 'No song given'}"), unsafe_allow_html=True)
            else:
                st.markdown(styled_text(f" You got the song name incorrect ❌: {your_song or 'No song given'}"), unsafe_allow_html=True)

            if artist_correct:
                st.markdown(styled_text(f" You got the artist correct ✔️: {your_artist}"), unsafe_allow_html=True)
            else:
                st.markdown(styled_text(f" You got the artist name incorrect ❌ : {your_artist or 'No artist given'}"), unsafe_allow_html=True)

        # Formatting for when both answers are incorrect
        else:
            # Determine message based on if any answer was given at all
            if not your_artist and not your_song:
                user_answer = "No answer given"
            elif not your_artist:
                user_answer = f"No artist given - {your_song}" # Song first
            elif not your_song:
                user_answer = f"{your_artist} - No song given" # Artist first

            st.markdown(styled_text(f" Question {idx + 1}: Incorrect ❌ Your answer: {user_answer}"), unsafe_allow_html=True)

        # Provide the full song for every answer, correct or incorrect
        st.markdown(f"###### Correct answer: {selected_songs[idx]['song']} - {selected_songs[idx]['artist']}")  # Song - Artist
        full_song_file = response.get('full_file')

        # Check if full song file is present before displaying
        if full_song_file and os.path.exists(full_song_file):
            st.audio(full_song_file)
        else:
            st.markdown("Full song not available.")




# Function to reset game state
def reset_game():
    # Clear all session state variables
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.game_completed = False
    st.session_state.selected_songs = random.sample(music_data, 5)
    st.session_state.user_answers = [{} for _ in range(len(st.session_state.selected_songs))]

    st.rerun()

# Reset game button after completion
if st.session_state.game_completed:
    if st.button("Reset Game"):
        reset_game()

