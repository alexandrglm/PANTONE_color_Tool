import json
import os

JSON_FILE_PATH = './engine/pantone-html-cmyk.json'
HTML_FILE_PATH = './output/PANTONE-TOOL_0001.html'

def load_pantone_colors(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def generate_html(colors):
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
      <link rel="stylesheet" href="./engine/pantone-colors.scss">
      <link rel="stylesheet" href="./engine/styles.css">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/wingcss/0.1.8/wing.min.css">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/1.5.12/clipboard.min.js"></script>
      <style>
        .color-box {
          width: 50px;
          height: 50px;
          display: inline-block;
          cursor: pointer;
        }
        #selected-color {
          margin-top: 20px;
          padding: 10px;
          border: 1px solid #ccc;
          display: flex;
          align-items: center;
        }
        #color-display {
          width: 50px;
          height: 50px;
          margin-right: 10px;
        }
        #hex-code, #cmyk-code {
          font-size: 18px;
        }
        #search {
          margin-bottom: 20px;
        }
      </style>
    </head>
    <body>
      <h1 class="text-center">Pantone Colors</h1>
      <div class="text-center">
        <input type="text" id="search" placeholder="Search by name, hex code, or CMYK" oninput="filterColors()">
      </div>
      <div class="row">
        <div class="col-3" id="color-list">
    '''

    if isinstance(colors, dict):
        for code, color in colors.items():
            if isinstance(color, dict):
                name = color.get('name', 'Unnamed')
                hex_code = color.get('hex', '#000000')
                cmyk = color.get('cmyk', [0, 0, 0, 0])
                cmyk_str = ', '.join(f'{value:.2f}' for value in cmyk)
                html_content += f'''
                <div class="color-item">
                  <div class="color-box" style="background-color: #{hex_code};" data-hex="{hex_code}" data-cmyk="{cmyk_str}" onclick="selectColor(this)"></div>
                  <span>{name}</span>
                </div>
                '''
            else:
                print(f"Warning: Skipping invalid entry: {color}")
    else:
        print("Error: JSON file does not contain a dictionary of color objects.")

    html_content += '''
        </div>
        <div class="col-3">
          <div id="selected-color">
            <div id="color-display"></div>
            <div id="hex-code">#000000</div>
            <div id="cmyk-code">0, 0, 0, 0</div>
          </div>
        </div>
      </div>

      <script>
        function selectColor(element) {
          const hex = element.getAttribute('data-hex');
          const cmyk = element.getAttribute('data-cmyk');
          document.getElementById('color-display').style.backgroundColor = hex;
          document.getElementById('hex-code').textContent = hex;
          document.getElementById('cmyk-code').textContent = cmyk;
          navigator.clipboard.writeText(hex);
        }

        function filterColors() {
          const search = document.getElementById('search').value.toLowerCase();
          const items = document.querySelectorAll('.color-item');
          items.forEach(item => {
            const name = item.querySelector('span').textContent.toLowerCase();
            const hex = item.querySelector('.color-box').getAttribute('data-hex');
            const cmyk = item.querySelector('.color-box').getAttribute('data-cmyk');
            if (name.includes(search) || hex.includes(search) || cmyk.includes(search)) {
              item.style.display = '';
            } else {
              item.style.display = 'none';
            }
          });
        }
      </script>
    </body>
    </html>
    '''

    with open(HTML_FILE_PATH, 'w') as file:
        file.write(html_content)

def main():
    pantone_colors = load_pantone_colors(JSON_FILE_PATH)
    generate_html(pantone_colors)

if __name__ == '__main__':
    main()
