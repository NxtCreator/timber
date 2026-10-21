import random
from datetime import datetime
import time

log_levels = ["WARN", "ERROR", "DEBUG", "INFO", "CRITICAL"]


log_messages = {
    "ERROR": [
        'Database connection failed',
        'File not found',
        'Authentication failed'
    ],

    "INFO": [
        'Application started',
        'User logged in successfully'
    ],

    "WARN": [
        'High memory usage detected',
        'API response time exceeded threshold',
        'Disk space running low',
        'Connection is unstable',
        'Request rate approaching limit'
    ],

    "CRITICAL": [
        'Database server is unreachable',
        'Application crashed unexpectedly',
        'System resources exhausted',
        'Critical service has stopped responding',
        'Data corruption detected',
        'Unable to recover from fatal error'
    ],

    "DEBUG": [
        "Initializing database connection",
        "Processing incoming request",
        "Loading configuration settings",
        "Validating user input",
        "Executing database query",
        "Cache lookup completed"
    ]
}

try:
    logs_to_gen = input('How many logs: ')
    if not logs_to_gen.strip():
        logs_to_gen = None
    else:
        logs_to_gen = int(logs_to_gen)
except ValueError:
    print("Please enter a valid positive integer")
else:
    if logs_to_gen is not None and logs_to_gen <= 0:
         print('You must only enter positive integers')
    else:
        if logs_to_gen is not None:
            print(f"Generating {logs_to_gen} logs...\n")
        else:
            print("Generating logs")
        time.sleep(1)
        

        try:
            gen_logs = 0
                
            while True:
                if logs_to_gen is not None and gen_logs >= logs_to_gen:
                    break
                timestamp = datetime.now()
                formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                log_level = random.choice(log_levels)
                log_message = random.choice(log_messages[log_level])
                log = f"{formatted_timestamp} | {log_level} | {log_message}"

                with open("app.log", "a") as file:
                    file.write(log + "\n")

                print(f"[+] {log}")
                gen_logs += 1
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Stopped")


