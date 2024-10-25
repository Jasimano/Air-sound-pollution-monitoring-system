# Import necessary libraries
import machine
import time
import dht
import urequests  # For sending data to cloud storage via HTTP
from machine import Pin, ADC
from umqtt.simple import MQTTClient  # If using MQTT for cloud communication

# Wi-Fi connection details
WIFI_SSID = 'your_ssid'
WIFI_PASSWORD = 'your_password'
CLOUD_ENDPOINT = 'http://your_cloud_endpoint.com/data'

# Initialize DHT11 sensor (Temperature & Humidity)
dht_pin = Pin(14)
dht_sensor = dht.DHT11(dht_pin)

# Initialize MQ135 sensor (Air Quality)
mq135_pin = ADC(Pin(32))  # Adjust according to your board
mq135_pin.atten(ADC.ATTN_11DB)  # Configure ADC range

# Initialize LM393 sensor (Sound Level)
lm393_pin = ADC(Pin(34))  # Adjust according to your board
lm393_pin.atten(ADC.ATTN_11DB)

# Initialize MQ-6 sensor (CO2 sensor)
mq6_pin = ADC(Pin(33))  # Adjust pin number
mq6_pin.atten(ADC.ATTN_11DB)

# Initialize Servo Motor (SG90)
servo_pin = Pin(13)
servo = machine.PWM(servo_pin, freq=50)  # PWM for controlling Servo

# Function to connect to Wi-Fi
def connect_wifi(ssid, password):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi')

# Function to send data to cloud storage
def send_data_to_cloud(data):
    response = urequests.post(CLOUD_ENDPOINT, json=data)
    print('Data sent to cloud:', response.text)

# Reading data from sensors
def read_sensors():
    # Read temperature and humidity
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    # Read air quality (MQ135)
    air_quality = mq135_pin.read()  # Returns ADC value
    
    # Read sound level (LM393)
    sound_level = lm393_pin.read()  # Returns ADC value
    
    # Read CO2 level (MQ-6)
    co2_level = mq6_pin.read()  # Returns ADC value
    
    return temp, humidity, air_quality, sound_level, co2_level

# Main loop
def main():
    # Connect to Wi-Fi
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    
    while True:
        # Read sensor data
        temp, humidity, air_quality, sound_level, co2_level = read_sensors()
        print('Temperature:', temp)
        print('Humidity:', humidity)
        print('Air Quality (MQ135):', air_quality)
        print('Sound Level (LM393):', sound_level)
        print('CO2 Level (MQ-6):', co2_level)
        
        # Create a dictionary with sensor data
        sensor_data = {
            'temperature': temp,
            'humidity': humidity,
            'air_quality': air_quality,
            'sound_level': sound_level,
            'co2_level': co2_level
        }
        
        # Send data to cloud storage
        send_data_to_cloud(sensor_data)
        
        # Delay before the next reading
        time.sleep(10)

# Run the main loop
main()
