# GuideTracker - Tour Guide Monitoring System
# This is a test to see VS Code Git working!

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# Home route - shows the main page
@app.route('/')
def home():
    return "GuideTracker Backend is running! 🚀"

# Test route - check if server is working
@app.route('/api/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Backend is working!'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**That's the complete file!** 

Just add those two comment lines at the very top, before the `from flask import...` line.

## 🎯 Your app.py should look like:
```
Line 1: # GuideTracker - Tour Guide Monitoring System
Line 2: # This is a test to see VS Code Git working!
Line 3: (blank line)
Line 4: from flask import Flask, render_template, request, jsonify
Line 5: (blank line)
Line 6: app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
... (rest of the code you already have)