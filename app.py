from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# File to store the actions
actions_file = 'actions.json'

def load_actions():
    try:
        with open(actions_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file doesn't exist or is empty

def save_actions(actions):
    with open(actions_file, 'w') as file:
        json.dump(actions, file, indent=4)

def calculate_pwm(brightness):
    # Placeholder for PWM calculation logic
    # For example, scale brightness (0-255) to PWM range (0-100%)
    return int((brightness / 255) * 100)

# Load existing actions on server start
actions = load_actions()

@app.route('/')
def index():
    return render_template('index.html', actions=actions)

@app.route('/set_schedule', methods=['POST'])
def set_schedule():
    global actions
    actions = request.json
    save_actions(actions)
    return jsonify({"status": "success", "data": actions})

@app.route('/calculate_pwm', methods=['POST'])
def get_pwm_value():
    brightness = request.json.get('brightness', 0)
    pwm_value = calculate_pwm(int(brightness))
    return jsonify({"pwm": pwm_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
