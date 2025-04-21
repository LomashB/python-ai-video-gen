document.addEventListener('DOMContentLoaded', () => {
    // Handle tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // Add active class to the clicked button
            btn.classList.add('active');
            
            // Show the corresponding pane
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Handle file drop area
    const fileDropArea = document.querySelector('.file-drop-area');
    const fileInput = document.querySelector('.file-input');
    
    if (fileDropArea && fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            fileDropArea.classList.add('highlight');
        }
        
        function unhighlight() {
            fileDropArea.classList.remove('highlight');
        }
        
        fileDropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length) {
                fileInput.files = files;
                updateFileMessage(files[0].name);
            }
        }
        
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updateFileMessage(fileInput.files[0].name);
            }
        });
        
        function updateFileMessage(filename) {
            const fileMessage = fileDropArea.querySelector('.file-message');
            if (fileMessage) {
                fileMessage.textContent = `Selected: ${filename}`;
            }
        }
    }
    
    // Handle video preview modal
    const videoModal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modalVideo');
    const previewBtns = document.querySelectorAll('.preview-btn');
    
    previewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const videoSrc = btn.getAttribute('data-video');
            if (videoSrc && modalVideo) {
                modalVideo.querySelector('source').src = videoSrc;
                modalVideo.load();
                openModal(videoModal);
            }
        });
    });
    
    // Handle audio preview modal
    const audioModal = document.getElementById('audioModal');
    const modalAudio = document.getElementById('modalAudio');
    const previewAssetBtns = document.querySelectorAll('.preview-asset');
    
    previewAssetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const assetType = btn.getAttribute('data-type');
            const fileName = btn.getAttribute('data-file');
            
            if (assetType === 'video') {
                const videoSrc = `/assets/videos/${fileName}`;
                if (modalVideo) {
                    modalVideo.querySelector('source').src = videoSrc;
                    modalVideo.load();
                    openModal(videoModal);
                }
            } else if (assetType === 'audio') {
                const audioSrc = `/assets/music/${fileName}`;
                if (modalAudio) {
                    modalAudio.querySelector('source').src = audioSrc;
                    modalAudio.load();
                    openModal(audioModal);
                }
            }
        });
    });
    
    // Close modal buttons
    const closeModalBtns = document.querySelectorAll('.close-modal');
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            closeModal(modal);
            
            // Pause media when modal is closed
            const video = modal.querySelector('video');
            const audio = modal.querySelector('audio');
            
            if (video) video.pause();
            if (audio) audio.pause();
        });
    });
    
    // Close modal when clicking outside content
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target);
            
            // Pause media when modal is closed
            const video = e.target.querySelector('video');
            const audio = e.target.querySelector('audio');
            
            if (video) video.pause();
            if (audio) audio.pause();
        }
    });
    
    function openModal(modal) {
        if (modal) modal.style.display = 'block';
    }
    
    function closeModal(modal) {
        if (modal) modal.style.display = 'none';
    }
    
    // Handle flash message closing
    const closeFlashBtns = document.querySelectorAll('.close-flash');
    closeFlashBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const flash = btn.closest('.flash');
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.remove();
            }, 300);
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.remove();
            }, 300);
        }, 5000);
    });
    
    // Add task status polling functionality
    function pollTaskStatus() {
        const taskItems = document.querySelectorAll('.task-item');
        
        taskItems.forEach(item => {
            const statusElement = item.querySelector('.task-status');
            
            if (statusElement && statusElement.textContent === 'processing') {
                const taskId = item.dataset.taskId;
                
                if (taskId) {
                    fetch(`/api/status/${taskId}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.status !== 'processing') {
                                // Refresh the page when task completes
                                window.location.reload();
                            }
                        })
                        .catch(error => console.error('Error polling task status:', error));
                }
            }
        });
    }
    
    // Poll for task status every 5 seconds
    const hasProcessingTasks = document.querySelector('.task-status.status-processing');
    if (hasProcessingTasks) {
        setInterval(pollTaskStatus, 5000);
    }
});