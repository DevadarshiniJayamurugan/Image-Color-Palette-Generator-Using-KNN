from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'

def get_palette(image_path, n_colors=5):
    image = Image.open(image_path)
    image = image.resize((100, 100))
    image = np.array(image)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_
    hex_colors = ['#%02x%02x%02x' % tuple(map(int, color)) for color in colors]
    return hex_colors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            colors = get_palette(file_path)
            return render_template('index.html', colors=colors)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
