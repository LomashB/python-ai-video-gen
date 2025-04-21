# AI Motivational Video Generator

![Screenshot](static/img/screenshot_placeholder.jpg)

A powerful Python application with a beautiful web interface that automatically generates high-quality, 15-second motivational videos perfect for social media. The application uses AI to generate inspirational quotes and combines them with background videos, music, and professional text overlays.

## 🎬 Features

- **AI-Powered Quote Generation**: Uses Google's Gemini 1.5 Pro to create inspiring quotes
- **Automatic Video Creation**: Generates 15-second clips optimized for social platforms
- **Beautiful Web Interface**: Glassmorphism design with intuitive controls
- **Custom Asset Management**: Upload your own videos, music, and fonts
- **Responsive Design**: Works across desktop and mobile devices
- **Preview Functionality**: Watch and listen to your assets before using them
- **Background Processing**: Create videos without blocking the UI

## 🚀 Demo

https://github.com/yourusername/python-ai-video-gen

## 📋 Requirements

- Python 3.8+
- Flask
- moviepy
- Google Generative AI API key
- PIL (Pillow)
- gTTS (Google Text-to-Speech)

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-ai-video-gen.git
   cd python-ai-video-gen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. Prepare the assets folders (optional - will be created automatically if they don't exist):
   ```bash
   mkdir -p assets/videos assets/music assets/fonts output temp
   ```

5. Start the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📝 Usage

### Web Interface

1. **Create Videos**: Enter your custom quote or generate one with AI
2. **Upload Assets**: Add your background videos, music, and custom fonts
3. **Manage Files**: Browse and preview your uploaded assets
4. **Download Videos**: Access your generated videos from the "Output" tab

### Python Module

You can also use the video creator as a standalone Python module:

```python
import video_creator

# Generate a video with a custom quote
quote = "Dream big, work hard, stay focused."
author = "Unknown"
output_path = video_creator.create_video(quote, author)
print(f"Video created at: {output_path}")

# Or generate a video with an AI-created quote
quote, author = video_creator.generate_quote()
output_path = video_creator.create_video(quote, author)
```

## 🎨 Customization

### Video Settings

The video generator creates 15-second clips optimized for vertical video platforms. You can modify settings in `video_creator.py`:

- **TARGET_DURATION**: Change the video length (default: 15 seconds)
- **Resolution**: Adjust dimensions (default: 1080×1920)
- **Font Styles**: Custom text rendering options

### Web Interface

The web interface uses a modern glassmorphism design. Customize colors and styles in `static/css/style.css`.

## 🤖 How It Works

1. **Quote Generation**: 
   - Uses Google's Gemini 1.5 Pro AI to create original inspirational quotes
   - Falls back to a curated list of quotes if API is unavailable

2. **Text-to-Speech**: 
   - Converts the quote to natural-sounding speech using gTTS

3. **Video Processing**:
   - Takes background videos and crops them to vertical format
   - Applies text overlay with stylized typography
   - Adds background music and syncs it with speech
   - Ensures exact 15-second duration for consistency

4. **Web Interface**:
   - Flask backend handles file uploads and video processing
   - Modern UI built with HTML, CSS, and JavaScript
   - Background processing to avoid UI blocking

## 📊 Technical Architecture

```
python-ai-video-gen/
│
├── app.py                  # Flask web application
├── video_creator.py        # Core video generation logic
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
│
├── assets/                 # Asset storage
│   ├── videos/             # Background videos
│   ├── music/              # Background music
│   └── fonts/              # Custom fonts
│
├── static/                 # Web assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── img/                # Images for UI
│
├── templates/              # HTML templates
│   └── index.html          # Main application page
│
├── output/                 # Generated videos
└── temp/                   # Temporary files
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Google Gemini API](https://ai.google.dev/) for quote generation
- [MoviePy](https://zulko.github.io/moviepy/) for video processing
- [gTTS](https://github.com/pndurette/gTTS) for text-to-speech
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request