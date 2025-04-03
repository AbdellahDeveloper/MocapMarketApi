from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

TARGET_URL = "https://mafia-ejg.pages.dev"

# Read the injection code from file
with open('code_to_inject.js', 'r') as file:
    INJECTION_CODE = file.read()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # Construct the target URL
    url = f"{TARGET_URL}/{path}"
    
    # Get the response from the target website
    response = requests.get(url)
    
    # Get the content type from the original response
    content_type = response.headers.get('Content-Type', 'text/html')
    
    # If it's a JavaScript file, return with correct MIME type
    if path.endswith('.js'):
        return Response(
            response.content,
            content_type='application/javascript',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': response.headers.get('Cache-Control', 'no-cache')
            }
        )
    
    # Inject JavaScript if we're at root path or in a room page and it's HTML
    if ('text/html' in content_type) and (not path or path.startswith('room/')):
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create a new script tag
        script_tag = soup.new_tag('script')
        script_tag.string = INJECTION_CODE
        
        # Insert the script tag before the closing </body> tag
        body_tag = soup.find('body')
        if body_tag:
            body_tag.append(script_tag)
        else:
            soup.append(script_tag)
            
        return Response(
            str(soup),
            content_type=content_type,
            headers={
                'Access-Control-Allow-Origin': '*'
            }
        )
    
    # For other paths, return the original content with original headers
    return Response(
        response.content,
        content_type=content_type,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': response.headers.get('Cache-Control', 'no-cache')
        }
    )

if __name__ == '__main__':
    app.run()
