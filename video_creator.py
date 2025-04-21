import os
import random
import textwrap
import time
import requests
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# Use the standard import for moviepy
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, CompositeAudioClip, concatenate_audioclips
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

print("Starting script execution...")

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Set up folders
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("assets", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/videos", exist_ok=True)
os.makedirs("assets/music", exist_ok=True)
print("Folders created/confirmed")

# Set up Google Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
# Update the model name to match the current Gemini API version
model = genai.GenerativeModel('gemini-1.5-pro')
print("Google Gemini API configured")

# List of pre-defined quotes to avoid repetition
PREDEFINED_QUOTES = [
    ("Dream big, work hard, stay focused.", "Unknown"),
    ("Your only limit is your mind.", "Unknown"),
    ("The future belongs to those who believe in their dreams.", "Eleanor Roosevelt"),
    ("Take the risk or lose the chance.", "Unknown"),
    ("Don't stop until you're proud.", "Unknown"),
    ("The harder you work, the luckier you get.", "Gary Player"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The best way to predict the future is to create it.", "Abraham Lincoln"),
    ("Be the change you wish to see in the world.", "Mahatma Gandhi"),
]

# Keep track of used quotes to avoid repetition
used_quotes = []

def generate_quote():
    """Generate a motivational quote using Google Gemini API or predefined quotes"""
    global used_quotes
    
    # If we've used all predefined quotes, reset the list
    if len(used_quotes) >= len(PREDEFINED_QUOTES):
        used_quotes = []
    
    # Try to get a quote from Gemini API first
    try:
        print("Generating quote with Gemini API...")
        prompt = "Generate a short, powerful motivational quote (max 20 words) that would inspire someone to pursue their dreams. Return only the quote, nothing else."
        
        response = model.generate_content(prompt)
        quote = response.text.strip().strip('"\'')
        author = "Unknown"
        
        # Make sure quote isn't too long for Shorts
        if len(quote) > 100:
            quote = ' '.join(quote.split()[:15]) + '...'
        
        # If API call worked but we've seen this quote before, use a predefined one
        if (quote, author) in used_quotes:
            print("Quote already used, selecting a predefined quote instead")
            # Get unused predefined quotes
            unused_quotes = [q for q in PREDEFINED_QUOTES if q not in used_quotes]
            quote, author = random.choice(unused_quotes)
    
    except Exception as e:
        print(f"Error generating quote with API: {e}")
        # Choose a predefined quote that hasn't been used yet
        unused_quotes = [q for q in PREDEFINED_QUOTES if q not in used_quotes]
        if unused_quotes:
            quote, author = random.choice(unused_quotes)
        else:
            # If all quotes have been used, start over
            used_quotes = []
            quote, author = random.choice(PREDEFINED_QUOTES)
    
    # Add the chosen quote to used_quotes
    used_quotes.append((quote, author))
    print(f"Generated quote: '{quote}' - {author}")
    return quote, author

def text_to_speech(text, output_path="temp/speech.mp3"):
    """Convert text to speech using gTTS"""
    print(f"Converting text to speech: '{text}'")
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        print(f"Speech saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

def create_text_overlay(quote, author, width=1080, height=1920):
    """Create an image with the quote and author rendered on it"""
    print("Creating text overlay image...")
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Load fonts (you'll need to download these fonts or use system fonts)
    try:
        print("Loading fonts...")
        quote_font = ImageFont.truetype("assets/fonts/Montserrat-Bold.ttf", 70)
        author_font = ImageFont.truetype("assets/fonts/Montserrat-Regular.ttf", 40)
        print("Fonts loaded successfully")
    except Exception as e:
        # Fallback to default font if custom fonts not available
        print(f"Error loading custom fonts, using default: {e}")
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
    
    # Wrap text to fit width
    quote_lines = textwrap.wrap(quote, width=20)
    
    # Calculate positions
    quote_y = height // 2 - (len(quote_lines) * 80) // 2
    
    # Draw quote with subtle shadow for better readability
    print("Drawing text on image...")
    for line in quote_lines:
        # Shadow
        draw.text((width//2 + 2, quote_y + 2), line, font=quote_font, fill=(0, 0, 0, 180), anchor="mm")
        # Actual text
        draw.text((width//2, quote_y), line, font=quote_font, fill=(255, 255, 255, 255), anchor="mm")
        quote_y += 80
    
    # Draw author
    draw.text((width//2, quote_y + 50), f"- {author}", font=author_font, fill=(220, 220, 220, 220), anchor="mm")
    
    # Save the image
    output_path = "temp/text_overlay.png"
    image.save(output_path)
    print(f"Text overlay saved to {output_path}")
    return output_path

def get_random_file(directory):
    """Get a random file from the specified directory"""
    print(f"Getting random file from {directory}...")
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        print(f"No files found in {directory}")
        return None
    selected_file = os.path.join(directory, random.choice(files))
    print(f"Selected: {selected_file}")
    return selected_file

def create_video(quote, author, output_path="output/motivational_short.mp4"):
    """Create the final video by combining all elements"""
    print("Creating video...")
    
    # Set the exact target duration for all videos (15 seconds)
    TARGET_DURATION = 15.0
    
    # Get random background video and music
    print("Selecting background assets...")
    bg_video_path = get_random_file("assets/videos")
    bg_music_path = get_random_file("assets/music")
    
    if not bg_video_path:
        print("Error: No background videos found in assets/videos folder")
        return None
    
    # If no music file found, use a fallback error sound
    if not bg_music_path:
        print("Warning: No background music found. Creating a silent audio track.")
        # We'll create a silent audio clip later
    
    try:
        # Load the video clip
        print(f"Loading video clip: {bg_video_path}")
        video_clip = VideoFileClip(bg_video_path)
        print(f"Video loaded. Duration: {video_clip.duration}s, Resolution: {video_clip.size}")
        
        # Check if video already matches our aspect ratio
        clip_w, clip_h = video_clip.size
        print(f"Video dimensions: {clip_w}x{clip_h}")
        
        # If the video is already in the right format, just use it as is
        if clip_w != 1080 or clip_h != 1920:
            print("Warning: Video does not match target dimensions (1080x1920). Using as is.")
        
        # Make video exactly TARGET_DURATION seconds
        if video_clip.duration < TARGET_DURATION:
            print(f"Video too short ({video_clip.duration}s), extending to {TARGET_DURATION}s...")
            # Loop video to reach target duration
            video_clip = video_clip.loop(duration=TARGET_DURATION)
        elif video_clip.duration > TARGET_DURATION:
            print(f"Video too long ({video_clip.duration}s), trimming to {TARGET_DURATION}s...")
            video_clip = video_clip.subclip(0, TARGET_DURATION)
        
        print(f"Video duration set to exactly {TARGET_DURATION}s")
        
        # Generate speech
        print("Generating speech from quote...")
        speech_path = text_to_speech(quote)
        speech_clip = AudioFileClip(speech_path)
        speech_duration = speech_clip.duration
        print(f"Speech audio created. Duration: {speech_duration}s")
        
        # Calculate speech timing
        # We want speech to start at 1s and fit within our TARGET_DURATION
        speech_start = 1.0  # Start after 1 second
        
        # If speech is too long, speed it up slightly
        if speech_duration > TARGET_DURATION - 2:  # Leave some margin at the end
            speedup_factor = speech_duration / (TARGET_DURATION - 2)
            print(f"Speech too long, speeding up by factor of {speedup_factor:.2f}")
            # Use the raw speedx method without importing vfx
            speech_clip = speech_clip.speedx(factor=speedup_factor)
            speech_duration = speech_clip.duration
        
        # Add background music or fallback to silence
        print("Adding audio tracks...")
        if bg_music_path:
            print(f"Loading background music: {bg_music_path}")
            bg_music = AudioFileClip(bg_music_path).volumex(0.2)  # Lower volume
            
            # Make music exactly TARGET_DURATION seconds
            if bg_music.duration < TARGET_DURATION:
                print(f"Music too short ({bg_music.duration}s), creating manual loop...")
                # Create a manually looped music clip
                current_duration = bg_music.duration
                num_loops = int(TARGET_DURATION / current_duration) + 1
                audio_segments = [bg_music] * num_loops
                bg_music = concatenate_audioclips(audio_segments)
                # Trim to exact length
                bg_music = bg_music.subclip(0, TARGET_DURATION)
            elif bg_music.duration > TARGET_DURATION:
                print(f"Music too long ({bg_music.duration}s), trimming...")
                bg_music = bg_music.subclip(0, TARGET_DURATION)
            
            # Mix speech with background music
            final_audio = speech_clip.set_start(speech_start).volumex(1.5)  # Start speech after delay
            composite_audio = CompositeAudioClip([bg_music, final_audio])
            video_clip = video_clip.set_audio(composite_audio)
            print("Speech and background music mixed")
        else:
            # Create silent background track
            from moviepy.audio.AudioClip import AudioClip
            silent_clip = AudioClip(lambda t: 0, duration=TARGET_DURATION)
            final_audio = speech_clip.set_start(speech_start).volumex(1.5)
            composite_audio = CompositeAudioClip([silent_clip, final_audio])
            video_clip = video_clip.set_audio(composite_audio)
            print("Speech added with silent background")
        
        # Create text overlay
        print("Creating text overlay...")
        text_overlay_path = create_text_overlay(quote, author)
        text_overlay = ImageClip(text_overlay_path).set_duration(TARGET_DURATION)
        
        # Add text to video
        print("Adding text overlay to video...")
        final_clip = CompositeVideoClip([video_clip, text_overlay])
        
        # Ensure the final clip is exactly TARGET_DURATION
        final_clip = final_clip.subclip(0, TARGET_DURATION)
        
        # Write final video
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        final_output_path = f"output/motivational_short_{timestamp}.mp4"
        print(f"Writing final video to {final_output_path}...")
        final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=30)
        
        print(f"Video created successfully: {final_output_path}")
        return final_output_path
    
    except Exception as e:
        print(f"Error creating video: {e}")
        import traceback
        traceback.print_exc()  # Print full stack trace
        return None

def main():
    """Main function to run the automation process"""
    print("🚀 Starting YouTube Shorts creation process...")
    
    # Step 1: Generate motivational quote
    print("Step 1: Generating quote...")
    quote, author = generate_quote()
    
    # Step 2: Create the video
    print("Step 2: Creating video...")
    output_path = create_video(quote, author)
    
    if output_path:
        print(f"✅ Process complete! Your motivational Short is ready at: {output_path}")
    else:
        print("❌ Failed to create video. Check the errors above.")

if __name__ == "__main__":
    main()