import streamlit as st
import pandas as pd
from gtts import gTTS
import os
from pathlib import Path
import hashlib

st.set_page_config(page_title="News Summarizer", layout="wide")

# App Title
st.markdown("<h1 style='text-align: center;'>📰 News Summarizer with Audio</h1>", unsafe_allow_html=True)
st.markdown("---")

# Set up folder paths
csv_folder = Path(__file__).resolve().parent
category_csv_files = {
    'India': csv_folder / 'india.csv',
    'World': csv_folder / 'world.csv',
    'Business': csv_folder / 'business.csv',
    'Technology': csv_folder / 'tech.csv',
    'Sports': csv_folder / 'sports.csv'
}

# Category selection
selected_category = st.selectbox('📂 Select a News Category', list(category_csv_files.keys()))
st.markdown(f"## 🗂️ {selected_category} News")

# Read CSV
csv_file = category_csv_files[selected_category]
df = pd.read_csv(csv_file)

# Create audio cache folder
audio_dir = Path("temp_audio")
audio_dir.mkdir(exist_ok=True)

# Helper to create unique audio filenames
def get_audio_filename(text: str) -> str:
    hash_object = hashlib.md5(text.encode())
    return str(audio_dir / f"{hash_object.hexdigest()}.mp3")

# Display articles
for i in range(min(50, len(df))):
    row = df.iloc[i]
    if all(isinstance(field, str) and field.strip() for field in [row['Article Title'], row['Article Summary'], row['Article Link'], row['Article Image']]):
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['Article Image'], width=250, caption="Click below to read full article")
                st.markdown(f"[🔗 Read Full Article]({row['Article Link']})", unsafe_allow_html=True)
            with col2:
                st.markdown(f"### 📰 {row['Article Title'].replace('$', '\\$')}")
                st.write(row['Article Summary'].replace('$', '\\$'))

                # Audio conversion button
                audio_file_path = get_audio_filename(row['Article Summary'])
                convert_button_key = f"convert_button_{i}"
                if st.button("🔊 Convert to Audio", key=convert_button_key):
                    if not os.path.exists(audio_file_path):
                        tts = gTTS(row['Article Summary'], lang='en-uk')
                        tts.save(audio_file_path)
                    st.audio(audio_file_path)

            st.markdown("---")
    else:
        st.warning(f"⚠️ Skipped article {i + 1}: Missing or invalid data.")

# Optional: clean up on session end (not automatic with Streamlit's session model)
# import shutil; shutil.rmtree(audio_dir)
