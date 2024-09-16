from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import json
import os
from datetime import datetime

def load_pantone_colors(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_colors(image_path, num_colors=9):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_np = np.array(img)
    img_np = img_np.reshape((img_np.shape[0] * img_np.shape[1], 3))

    kmeans = KMeans(n_clusters=num_colors).fit(img_np)
    colors = kmeans.cluster_centers_.astype(int)
    return colors

def color_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

def find_closest_pantone_color(rgb, pantone_colors):
    closest_color = None
    min_distance = float('inf')

    for code, pantone in pantone_colors.items():
        pantone_color = (
            int(pantone['hex'][0:2], 16),
            int(pantone['hex'][2:4], 16),
            int(pantone['hex'][4:6], 16)
        )
        distance = color_distance(rgb, pantone_color)

        if distance < min_distance:
            min_distance = distance
            closest_color = {
                'name': pantone['name'],
                'hex': pantone['hex'],
                'code': code,
                'cmyk': pantone.get('cmyk', [0, 0, 0, 0])
            }

    return closest_color

def rgb_to_hex(rgb):
    return ''.join(f'{c:02x}' for c in rgb)

def save_html(image_path, pantone_matches):
    image_name = os.path.basename(image_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'Results_{image_name}_{timestamp}.html'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Color Analysis/title>
        <style>
            body {{
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 20px;
                font-family: Arial, sans-serif;
            }}
            #image {{
                position: relative;
                margin-bottom: 20px;
            }}
            #image img {{
                max-width: 100%;
                height: auto;
                position: relative;
            }}
            .color-box {{
                position: absolute;
                width: 50px;
                height: 50px;
                border: 2px solid #000;
                pointer-events: none;
            }}
            .color-info {{
                position: absolute;
                background: #fff;
                border: 1px solid #ccc;
                padding: 5px;
                display: none;
                font-size: 12px;
                white-space: nowrap;
            }}
            .color-box:hover + .color-info {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <div id="image">
            <img src="{image_path}" alt="Image">
    """

    for idx, match in enumerate(pantone_matches):
        if match:
            color_hex = match.get('hex', '000000')
            color_name = match.get('name', 'Unknown')
            color_code = match.get('code', 'N/A')
            cmyk_values = match.get('cmyk', [0, 0, 0, 0])
            cmyk_str = ', '.join(f'{value:.2f}' for value in cmyk_values)
            left = idx * 60
            top = 0
            html_content += f"""
                <div class="color-box" style="background-color: #{color_hex}; left: {left}px; top: {top}px;">
                </div>
                <div class="color-info" style="left: {left}px; top: {top + 60}px;">
                    Pantone: {color_name} (Code: {color_code})<br>
                    CMYK: {cmyk_str}
                </div>
            """

    html_content += """
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                const image = document.querySelector('#image img');
                const colorBoxes = document.querySelectorAll('.color-box');
                image.addEventListener('mousemove', function (event) {
                    colorBoxes.forEach(box => {
                        const boxRect = box.getBoundingClientRect();
                        const imageRect = image.getBoundingClientRect();
                        const boxLeft = boxRect.left - imageRect.left;
                        const boxTop = boxRect.top - imageRect.top;
                        if (event.clientX >= boxLeft + imageRect.left &&
                            event.clientX <= boxLeft + imageRect.left + boxRect.width &&
                            event.clientY >= boxTop + imageRect.top &&
                            event.clientY <= boxTop + imageRect.top + boxRect.height) {
                            box.nextElementSibling.style.display = 'block';
                        } else {
                            box.nextElementSibling.style.display = 'none';
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """

    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"Results saved to {output_file}")

def process_image(image_path):
    pantone_colors = load_pantone_colors('./engine/pantone-html-cmyk.json')
    colors = extract_colors(image_path)
    pantone_matches = [find_closest_pantone_color(tuple(color), pantone_colors) for color in colors]
    save_html(image_path, pantone_matches)

if __name__ == "__main__":
    image_path = input("Image PATH?: ").strip()

    if not os.path.isfile(image_path):
        print("Incorrect PATH.")
    else:
        process_image(image_path)
