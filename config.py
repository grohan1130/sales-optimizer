import os

class Config:
    # Base directory of the project
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True) 