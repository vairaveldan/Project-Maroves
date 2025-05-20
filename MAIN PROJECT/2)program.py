import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
input_pin = 17      
output_pin = 18
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(output_pin, GPIO.OUT)
GPIO.output(output_pin, GPIO.LOW)  # Start with output LOW

try:
    while True:
        if GPIO.input(input_pin) == GPIO.HIGH:
            GPIO.output(output_pin, GPIO.HIGH)
        else:
            GPIO.output(output_pin, GPIO.LOW)

        time.sleep(3)  # Small delay to avoid bouncing

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    GPIO.cleanup()