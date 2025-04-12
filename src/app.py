import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import html

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/cheahjs/free-llm-api-resources/main/README.md'

def clean_text(text):
    # Remove HTML tags and decode HTML entities
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_readme():
    response = requests.get(GITHUB_RAW_URL)
    response.raise_for_status()
    content = response.text
    
    # Clean HTML content first
    soup = BeautifulSoup(content, 'html.parser')
    lines = [clean_text(line) for line in content.split('\n')]
    
    providers = []
    current_provider = None
    in_models_section = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('## '):
            if current_provider:
                providers.append(current_provider)
            current_provider = {
                'name': clean_text(line.replace('## ', '')),
                'details': '',
                'models': [],
                'link': '',
                'limits': ''
            }
            in_models_section = False
            
        elif current_provider:
            if '**Models**:' in line:
                in_models_section = True
                continue
                
            elif line.startswith('-') and in_models_section:
                model_info = clean_text(line.replace('- ', ''))
                model_name = model_info
                model_limits = ''
                
                # Extract model name and limits from various formats
                if '(' in model_info and ')' in model_info:
                    model_name = clean_text(model_info[:model_info.find('(')])
                    model_limits = clean_text(model_info[model_info.find('(')+1:model_info.find(')')])
                elif ':' in model_info:
                    parts = model_info.split(':', 1)
                    model_name = clean_text(parts[0])
                    model_limits = clean_text(parts[1])
                
                current_provider['models'].append({
                    'name': model_name,
                    'limits': model_limits
                })
                
            elif line:
                if '://' in line:
                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                    if urls:
                        current_provider['link'] = clean_text(urls[0])
                if any(keyword in line.lower() for keyword in ['free', 'limit', 'credit']):
                    current_provider['limits'] += clean_text(line) + ' '
                else:
                    current_provider['details'] += clean_text(line) + ' '
    
    if current_provider:
        providers.append(current_provider)
    
    return providers

def main():
    st.set_page_config(page_title="LLM API Explorer", layout="wide")
    st.title("LLM API Explorer")

    providers = parse_readme()

    # Sidebar for provider selection
    st.sidebar.title("Provider List")
    selected_provider = st.sidebar.selectbox(
        "Select a provider",
        options=[p['name'] for p in providers]
    )

    # Main content area
    if selected_provider:
        provider = next((p for p in providers if p['name'] == selected_provider), None)
        
        if provider:
            st.header(provider['name'])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if provider['details']:
                    st.subheader("Details")
                    st.write(provider['details'])

                if provider['models']:
                    st.subheader("Available Models")
                    for model in provider['models']:
                        with st.expander(model['name']):
                            if model['limits']:
                                st.write(f"**Limits:** {model['limits']}")
            
            with col2:
                if provider['link']:
                    st.markdown(f"[Visit Provider]({provider['link']})")
                
                if provider['limits']:
                    st.subheader("Usage Limits")
                    st.write(provider['limits'])

if __name__ == '__main__':
    main()