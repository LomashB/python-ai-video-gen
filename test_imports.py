print("Testing imports...")

try:
    import os
    print("✓ os")
except ImportError as e:
    print(f"✗ os: {e}")

try:
    import random
    print("✓ random")
except ImportError as e:
    print(f"✗ random: {e}")

try:
    import textwrap
    print("✓ textwrap")
except ImportError as e:
    print(f"✗ textwrap: {e}")

try:
    import time
    print("✓ time")
except ImportError as e:
    print(f"✗ time: {e}")

try:
    import requests
    print("✓ requests")
except ImportError as e:
    print(f"✗ requests: {e}")

try:
    import json
    print("✓ json")
except ImportError as e:
    print(f"✗ json: {e}")

try:
    from PIL import Image, ImageDraw, ImageFont
    print("✓ PIL (Pillow)")
except ImportError as e:
    print(f"✗ PIL: {e}")

try:
    import moviepy
    print("✓ moviepy")
    
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
        print("✓ moviepy.editor")
    except ImportError as e:
        print(f"✗ moviepy.editor: {e}")
    
except ImportError as e:
    print(f"✗ moviepy: {e}")

try:
    from gtts import gTTS
    print("✓ gtts")
except ImportError as e:
    print(f"✗ gtts: {e}")

try:
    import google.generativeai as genai
    print("✓ google.generativeai")
except ImportError as e:
    print(f"✗ google.generativeai: {e}")

try:
    from dotenv import load_dotenv
    print("✓ dotenv")
except ImportError as e:
    print(f"✗ dotenv: {e}")

print("Import tests complete!") 