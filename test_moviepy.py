print("Testing moviepy imports...")

try:
    import moviepy
    print("✓ moviepy base import successful")
    
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        print("✓ VideoFileClip import successful")
    except ImportError as e:
        print(f"✗ VideoFileClip import failed: {e}")
    
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        print("✓ AudioFileClip import successful")
    except ImportError as e:
        print(f"✗ AudioFileClip import failed: {e}")
    
    try:
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        print("✓ CompositeVideoClip import successful")
    except ImportError as e:
        print(f"✗ CompositeVideoClip import failed: {e}")
    
    try:
        from moviepy.video.VideoClip import ImageClip
        print("✓ ImageClip import successful")
    except ImportError as e:
        print(f"✗ ImageClip import failed: {e}")
    
    try:
        from moviepy.video.tools.drawing import TextClip
        print("✓ TextClip import successful")
    except ImportError as e:
        print(f"✗ TextClip import failed: {e}")
        
except ImportError as e:
    print(f"✗ moviepy base import failed: {e}")

print("Testing complete") 