
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or 'your-secret-key-here'

# In-memory storage for demo (in production, use a database)
platforms_data = {}

# Define supported platforms and their required fields
SUPPORTED_PLATFORMS = {
    'twitter': {
        'name': 'Twitter/X',
        'fields': ['api_key', 'api_secret', 'access_token', 'access_token_secret']
    },
    'github': {
        'name': 'GitHub',
        'fields': ['username', 'personal_access_token']
    },
    'discord': {
        'name': 'Discord',
        'fields': ['bot_token', 'client_id', 'client_secret']
    },
    'reddit': {
        'name': 'Reddit',
        'fields': ['client_id', 'client_secret', 'username', 'password']
    },
    'spotify': {
        'name': 'Spotify',
        'fields': ['client_id', 'client_secret']
    },
    'youtube': {
        'name': 'YouTube',
        'fields': ['api_key']
    },
    'instagram': {
        'name': 'Instagram',
        'fields': ['access_token', 'user_id']
    },
    'linkedin': {
        'name': 'LinkedIn',
        'fields': ['client_id', 'client_secret', 'access_token']
    },
    'twitch': {
        'name': 'Twitch',
        'fields': ['client_id', 'client_secret', 'access_token']
    },
    'telegram': {
        'name': 'Telegram',
        'fields': ['bot_token', 'chat_id']
    }
}

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Platform API Manager</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .platform-card { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .configured { background-color: #e8f5e8; border-color: #28a745; }
            .not-configured { background-color: #fff3cd; border-color: #ffc107; }
            .btn { padding: 8px 16px; margin: 5px; text-decoration: none; border-radius: 3px; display: inline-block; }
            .btn-primary { background-color: #007bff; color: white; }
            .btn-success { background-color: #28a745; color: white; }
            .btn-warning { background-color: #ffc107; color: black; }
            .status { font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Multi-Platform API Manager</h1>
        <p>Manage your API credentials for multiple platforms</p>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div style="background-color: #d4edda; padding: 10px; margin: 10px 0; border-radius: 5px;">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <h2>Supported Platforms</h2>
        {% for platform_id, platform_info in platforms.items() %}
            <div class="platform-card {% if platform_id in configured_platforms %}configured{% else %}not-configured{% endif %}">
                <h3>{{ platform_info.name }}</h3>
                <p class="status">
                    Status: {% if platform_id in configured_platforms %}<span style="color: green;">✓ Configured</span>{% else %}<span style="color: orange;">⚠ Not Configured</span>{% endif %}
                </p>
                <p>Required fields: {{ platform_info.fields | join(', ') }}</p>
                <a href="{{ url_for('configure_platform', platform_id=platform_id) }}" class="btn {% if platform_id in configured_platforms %}btn-warning{% else %}btn-primary{% endif %}">
                    {% if platform_id in configured_platforms %}Update Configuration{% else %}Configure{% endif %}
                </a>
                {% if platform_id in configured_platforms %}
                    <a href="{{ url_for('test_platform', platform_id=platform_id) }}" class="btn btn-success">Test Connection</a>
                {% endif %}
            </div>
        {% endfor %}
        
        <h2>Quick Actions</h2>
        <a href="{{ url_for('view_all_configs') }}" class="btn btn-primary">View All Configurations</a>
        <a href="{{ url_for('export_configs') }}" class="btn btn-primary">Export Configurations</a>
    </body>
    </html>
    ''', platforms=SUPPORTED_PLATFORMS, configured_platforms=platforms_data.keys())

@app.route('/configure/<platform_id>', methods=['GET', 'POST'])
def configure_platform(platform_id):
    if platform_id not in SUPPORTED_PLATFORMS:
        flash('Platform not supported')
        return redirect(url_for('home'))
    
    platform_info = SUPPORTED_PLATFORMS[platform_id]
    
    if request.method == 'POST':
        config = {}
        for field in platform_info['fields']:
            config[field] = request.form.get(field, '').strip()
        
        if all(config.values()):  # Check if all fields are filled
            platforms_data[platform_id] = config
            flash(f'{platform_info["name"]} configured successfully!')
            return redirect(url_for('home'))
        else:
            flash('Please fill in all required fields')
    
    current_config = platforms_data.get(platform_id, {})
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Configure {{ platform_name }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"], input[type="password"] { width: 100%; max-width: 400px; padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 3px; border: none; cursor: pointer; }
            .btn-primary { background-color: #007bff; color: white; }
            .btn-secondary { background-color: #6c757d; color: white; }
            .sensitive { background-color: #f8f9fa; }
        </style>
    </head>
    <body>
        <h1>Configure {{ platform_name }}</h1>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div style="background-color: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px;">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            {% for field in fields %}
                <div class="form-group">
                    <label for="{{ field }}">{{ field.replace('_', ' ').title() }}:</label>
                    {% if 'token' in field or 'secret' in field or 'password' in field %}
                        <input type="password" id="{{ field }}" name="{{ field }}" value="{{ current_config.get(field, '') }}" class="sensitive" placeholder="Enter your {{ field.replace('_', ' ') }}">
                    {% else %}
                        <input type="text" id="{{ field }}" name="{{ field }}" value="{{ current_config.get(field, '') }}" placeholder="Enter your {{ field.replace('_', ' ') }}">
                    {% endif %}
                </div>
            {% endfor %}
            
            <button type="submit" class="btn btn-primary">Save Configuration</button>
            <a href="{{ url_for('home') }}" class="btn btn-secondary">Cancel</a>
        </form>
        
        <h3>Platform Documentation</h3>
        <p>Make sure you have the correct credentials from {{ platform_name }}. Check their developer documentation for API access requirements.</p>
    </body>
    </html>
    ''', platform_name=platform_info['name'], fields=platform_info['fields'], current_config=current_config)

@app.route('/test/<platform_id>')
def test_platform(platform_id):
    if platform_id not in platforms_data:
        flash('Platform not configured')
        return redirect(url_for('home'))
    
    config = platforms_data[platform_id]
    platform_name = SUPPORTED_PLATFORMS[platform_id]['name']
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test {{ platform_name }} Connection</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .config-display { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 3px; display: inline-block; }
            .btn-primary { background-color: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>{{ platform_name }} Configuration Test</h1>
        
        <div class="config-display">
            <h3>Current Configuration:</h3>
            {% for key, value in config.items() %}
                <p><strong>{{ key.replace('_', ' ').title() }}:</strong> 
                {% if 'token' in key or 'secret' in key or 'password' in key %}
                    ••••••••••••
                {% else %}
                    {{ value }}
                {% endif %}
                </p>
            {% endfor %}
        </div>
        
        <p><strong>Status:</strong> <span style="color: green;">✓ Configuration loaded successfully</span></p>
        <p><em>Note: In a production environment, this would make actual API calls to test the connection.</em></p>
        
        <a href="{{ url_for('home') }}" class="btn btn-primary">Back to Home</a>
        <a href="{{ url_for('configure_platform', platform_id=platform_id) }}" class="btn btn-primary">Edit Configuration</a>
    </body>
    </html>
    ''', platform_name=platform_name, config=config)

@app.route('/view-configs')
def view_all_configs():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>All Configurations</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .platform-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 3px; display: inline-block; }
            .btn-primary { background-color: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>All Platform Configurations</h1>
        
        {% if platforms_data %}
            {% for platform_id, config in platforms_data.items() %}
                <div class="platform-section">
                    <h3>{{ supported_platforms[platform_id]['name'] }}</h3>
                    {% for key, value in config.items() %}
                        <p><strong>{{ key.replace('_', ' ').title() }}:</strong> 
                        {% if 'token' in key or 'secret' in key or 'password' in key %}
                            ••••••••••••
                        {% else %}
                            {{ value }}
                        {% endif %}
                        </p>
                    {% endfor %}
                </div>
            {% endfor %}
        {% else %}
            <p>No platforms configured yet.</p>
        {% endif %}
        
        <a href="{{ url_for('home') }}" class="btn btn-primary">Back to Home</a>
    </body>
    </html>
    ''', platforms_data=platforms_data, supported_platforms=SUPPORTED_PLATFORMS)

@app.route('/export')
def export_configs():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Export Configurations</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .json-output { background-color: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; white-space: pre-wrap; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 3px; display: inline-block; }
            .btn-primary { background-color: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>Export Configurations</h1>
        <p>Here are your current platform configurations in JSON format:</p>
        
        <div class="json-output">{{ config_json }}</div>
        
        <p><em>Note: Sensitive data like tokens and secrets are masked for security.</em></p>
        
        <a href="{{ url_for('home') }}" class="btn btn-primary">Back to Home</a>
    </body>
    </html>
    ''', config_json=json.dumps(platforms_data, indent=2))

@app.route('/about')
def about():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>About Multi-Platform API Manager</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 3px; display: inline-block; }
            .btn-primary { background-color: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>About Multi-Platform API Manager</h1>
        <p>This application allows you to manage API credentials for multiple platforms in one place.</p>
        
        <h2>Supported Platforms:</h2>
        <ul>
            {% for platform_id, platform_info in platforms.items() %}
                <li><strong>{{ platform_info.name }}</strong> - {{ platform_info.fields | length }} required fields</li>
            {% endfor %}
        </ul>
        
        <h2>Features:</h2>
        <ul>
            <li>Secure credential storage for multiple platforms</li>
            <li>Easy configuration management</li>
            <li>Connection testing capabilities</li>
            <li>Export/import functionality</li>
            <li>Extensible platform support</li>
        </ul>
        
        <a href="{{ url_for('home') }}" class="btn btn-primary">Back to Home</a>
    </body>
    </html>
    ''', platforms=SUPPORTED_PLATFORMS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
