from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import time
from werkzeug.utils import secure_filename
import video_creator
import threading
import json

app = Flask(__name__)
app.secret_key = 'inspirational_videos_secret_key'

# Configure upload folders
UPLOAD_FOLDER = 'assets'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mp3', 'wav', 'ttf', 'otf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max upload

# Task status tracking
tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Get list of videos in assets folder
    videos = []
    if os.path.exists(os.path.join(UPLOAD_FOLDER, 'videos')):
        videos = [f for f in os.listdir(os.path.join(UPLOAD_FOLDER, 'videos')) 
                if os.path.isfile(os.path.join(UPLOAD_FOLDER, 'videos', f))]
    
    # Get list of music files
    music = []
    if os.path.exists(os.path.join(UPLOAD_FOLDER, 'music')):
        music = [f for f in os.listdir(os.path.join(UPLOAD_FOLDER, 'music')) 
               if os.path.isfile(os.path.join(UPLOAD_FOLDER, 'music', f))]
    
    # Get list of fonts
    fonts = []
    if os.path.exists(os.path.join(UPLOAD_FOLDER, 'fonts')):
        fonts = [f for f in os.listdir(os.path.join(UPLOAD_FOLDER, 'fonts')) 
               if os.path.isfile(os.path.join(UPLOAD_FOLDER, 'fonts', f))]
    
    # Get list of output videos
    output_videos = []
    if os.path.exists('output'):
        output_videos = [f for f in os.listdir('output') 
                         if os.path.isfile(os.path.join('output', f))]
        
    return render_template('index.html', 
                           videos=videos, 
                           music=music, 
                           fonts=fonts,
                           output_videos=output_videos,
                           tasks=tasks)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    file_type = request.form.get('file_type')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Determine the subfolder based on file type
        subfolder = ''
        if file_type == 'video':
            subfolder = 'videos'
        elif file_type == 'music':
            subfolder = 'music'
        elif file_type == 'font':
            subfolder = 'fonts'
        else:
            flash('Invalid file type')
            return redirect(request.url)
        
        # Ensure directory exists
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], subfolder), exist_ok=True)
        
        # Save the file
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
        file.save(save_path)
        
        flash(f'File {filename} uploaded successfully to {subfolder}')
    else:
        flash('File type not allowed')
    
    return redirect(url_for('index'))

def create_video_task(quote, author):
    # Generate a task ID
    task_id = str(int(time.time()))
    tasks[task_id] = {
        "status": "processing",
        "quote": quote,
        "author": author,
        "start_time": time.time(),
        "output_path": None
    }
    
    try:
        # Call the video creation function
        output_path = video_creator.create_video(quote, author)
        
        if output_path:
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["output_path"] = output_path
        else:
            tasks[task_id]["status"] = "failed"
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
    
    tasks[task_id]["end_time"] = time.time()
    return task_id

@app.route('/create_video', methods=['POST'])
def create_video():
    # Extract form data
    quote = request.form.get('quote', '')
    author = request.form.get('author', 'Unknown')
    
    if not quote:
        flash('Please enter a quote')
        return redirect(url_for('index'))
    
    # Start the video creation process in a background thread
    thread = threading.Thread(target=create_video_task, args=(quote, author))
    thread.daemon = True
    thread.start()
    
    flash('Video creation started. This may take a few minutes.')
    return redirect(url_for('index'))

@app.route('/api/create', methods=['POST'])
def api_create_video():
    # Extract form data
    data = request.get_json()
    
    if not data or 'quote' not in data:
        return json.dumps({"error": "Please provide a quote"}), 400, {'ContentType':'application/json'}
    
    quote = data.get('quote', '')
    author = data.get('author', 'Unknown')
    
    # Start the video creation process in a background thread
    task_id = create_video_task(quote, author)
    
    return json.dumps({"task_id": task_id, "status": "processing"}), 200, {'ContentType':'application/json'}

@app.route('/api/status/<task_id>', methods=['GET'])
def task_status(task_id):
    if task_id not in tasks:
        return json.dumps({"error": "Task not found"}), 404, {'ContentType':'application/json'}
    
    return json.dumps(tasks[task_id]), 200, {'ContentType':'application/json'}

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory('output', filename)

@app.route('/generate-random')
def generate_random():
    # Get a random quote using the existing function
    quote, author = video_creator.generate_quote()
    
    # Start the video creation in a background thread
    thread = threading.Thread(target=create_video_task, args=(quote, author))
    thread.daemon = True
    thread.start()
    
    flash(f'Creating video with quote: "{quote}" - {author}')
    return redirect(url_for('index'))

# Create required directories
os.makedirs('assets/videos', exist_ok=True)
os.makedirs('assets/music', exist_ok=True)
os.makedirs('assets/fonts', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('temp', exist_ok=True)
os.makedirs('static', exist_ok=True)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
    
# This is for Vercel serverless deployment
def app_handler(environ, start_response):
    return app.wsgi_app(environ, start_response) 