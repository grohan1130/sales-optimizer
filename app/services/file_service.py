import os
import pandas as pd
import numpy as np
from flask import current_app

class FileService:
    def __init__(self):
        self.allowed_extensions = {'csv', 'xlsx', 'xls'}

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def process_file(self, file):
        filename = file.filename
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read the file based on its extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
            
        # Calculate monthly averages (excluding the product name column)
        monthly_averages = df.iloc[:, 1:].mean().round().astype(int).tolist()
        
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'monthly_averages': monthly_averages
        } 