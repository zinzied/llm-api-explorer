from flask import Flask, render_template, jsonify
import requests
import re
import os
from markdown import markdown

app = Flask(__name__, 
            template_folder=os.path.abspath('src/templates'),
            static_folder=os.path.abspath('src/static'))

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/cheahjs/free-llm-api-resources/main/README.md'

def parse_readme():
    response = requests.get(GITHUB_RAW_URL)
    response.raise_for_status()
    lines = response.text.split('\n')
    
    providers = []
    current_provider = None
    in_models_section = False
    
    for line in lines:
        line = line.strip()
        
        # Handle provider headers
        if line.startswith('## '):
            if current_provider:
                providers.append(current_provider)
            current_provider = {
                'name': line.replace('## ', '').strip(),
                'details': '',
                'models': [],
                'link': '',
                'limits': ''
            }
            in_models_section = False
            
        elif current_provider:
            # Handle models section
            if line.startswith('- **Models**:'):
                in_models_section = True
                continue
                
            elif line.startswith('- ') and in_models_section:
                model_info = line.replace('- ', '').strip()
                model_name = model_info
                model_limits = ''
                
                # Extract model limits from parentheses or after colon
                if '(' in model_info and ')' in model_info:
                    model_name = model_info[:model_info.find('(')].strip()
                    model_limits = model_info[model_info.find('(')+1:model_info.find(')')].strip()
                elif ':' in model_info:
                    parts = model_info.split(':', 1)
                    model_name = parts[0].strip()
                    model_limits = parts[1].strip()
                
                current_provider['models'].append({
                    'name': model_name,
                    'limits': model_limits
                })
                
            # Handle provider details and links
            elif line:
                if '://' in line:  # Contains URL
                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                    if urls:
                        current_provider['link'] = urls[0]
                if 'free' in line.lower() or 'limit' in line.lower() or 'credit' in line.lower():
                    current_provider['limits'] += line.strip() + ' '
                else:
                    current_provider['details'] += line + ' '
    
    if current_provider:
        providers.append(current_provider)
    
    return providers

@app.route('/')
def index():
    providers = parse_readme()
    return render_template('index.html', providers=providers)

@app.route('/provider/<name>')
def provider_details(name):
    providers = parse_readme()
    provider = next((p for p in providers if p['name'] == name), None)
    if provider:
        return render_template('provider.html', provider=provider)
    return "Provider not found", 404

if __name__ == '__main__':
    app.run(debug=True)