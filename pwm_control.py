#import pigpio
import time
from datetime import datetime
import json
import os

# Configuration
PWM_GPIO = 12
PWM_FREQUENCY = 22000  # Frequency for hardware PWM
MAX_DUTY_CYCLE = 1000000  # Maximum value for duty cycle
SCHEDULE_FILE = 'actions.json'

# Initialize pigpio
#pi = pigpio.pi()
#if not pi.connected:
#    exit()

def time_to_milliseconds(t):
    return ((t.hour * 3600 + t.minute * 60 + t.second) * 1000) + (t.microsecond // 1000)

def get_interpolated_pwm_duty_cycle(current_time_str, schedule):
    # Updated to handle milliseconds
    time_str, ms_str = current_time_str.split('.')
    current_time = datetime.strptime(time_str, '%H:%M:%S').time()
    current_ms = time_to_milliseconds(current_time) + int(ms_str)

    for i in range(len(schedule) - 1):
        start_event = schedule[i]
        end_event = schedule[i + 1]

        # Append ':00' for seconds if not present
        start_time_str = start_event['time'] + ':00' if len(start_event['time']) == 5 else start_event['time']
        end_time_str = end_event['time'] + ':00' if len(end_event['time']) == 5 else end_event['time']

        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        start_ms = time_to_milliseconds(start_time)
        end_ms = time_to_milliseconds(end_time)

        if start_ms <= current_ms < end_ms:
            start_brightness = int(start_event['brightness'])
            end_brightness = int(end_event['brightness'])

            progress = (current_ms - start_ms) / (end_ms - start_ms)
            interpolated_brightness = start_brightness + (end_brightness - start_brightness) * progress
            pwm_value = int((interpolated_brightness / 255) * MAX_DUTY_CYCLE)
            return pwm_value
    
    return 0

def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_file_modification_time(filename):
    return os.path.getmtime(filename)

try:
    last_mod_time = get_file_modification_time(SCHEDULE_FILE)
    schedule = load_schedule()

    while True:
        current_mod_time = get_file_modification_time(SCHEDULE_FILE)
        if current_mod_time != last_mod_time:
            schedule = load_schedule()
            last_mod_time = current_mod_time

        now_str = datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Includes milliseconds
        duty_cycle = get_interpolated_pwm_duty_cycle(now_str, schedule)
        #pi.hardware_PWM(PWM_GPIO, PWM_FREQUENCY, duty_cycle)
        print(f"Current time: {now_str}, PWM Duty Cycle: {duty_cycle}")

        time.sleep(0.1)  # Run the loop every 0.1 seconds

except KeyboardInterrupt:
    print("\nProgram interrupted by the user.")
except Exception as e:
    print(f"An error occurred: {e}")
#finally:
#    pi.hardware_PWM(PWM_GPIO, PWM_FREQUENCY, 0)
#    pi.stop()
