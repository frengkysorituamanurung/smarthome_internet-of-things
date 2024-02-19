import time
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

broker = '192.168.43.44'  # Ganti dengan alamat IP broker MQTT Anda
port = 1883
topic_publish = "sensor/"
client_id = 'python-mqtt'
username = 'test'
password = 'test'

GPIO.setmode(GPIO.BCM)
SOUND_PIN = 17  # Pin sensor suara (mikrofon)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Terhubung ke Broker MQTT!")
        else:
            print("Gagal terhubung, kode return %d\n" % rc)

    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def read_sound_sensor():
    GPIO.setup(SOUND_PIN, GPIO.IN)
    sound_value = GPIO.input(SOUND_PIN)
    if sound_value == GPIO.LOW:  # Jika suara terdeteksi
        return "Suara Terdeteksi"
    else:  # Jika suara tidak terdeteksi
        return "Suara Tidak Terdeteksi"

def publish_sound_data(client):
    while True:
        sound_value = read_sound_sensor()

        sound_message = {
            "Sound": sound_value
        }
        sound_msg = json.dumps(sound_message)
        client.publish(topic_publish, sound_msg)
        print(f"Published Sound Data - Value: {sound_value}")

        time.sleep(5)  # Menunggu 5 detik sebelum membaca ulang sensor

def on_message(client, userdata, msg):
    # Fungsi untuk menangani pesan MQTT
    # (tanpa perubahan karena tidak berkaitan dengan sensor suara)
    pass  # Ganti 'pass' dengan logika penanganan pesan jika diperlukan

def run():
    client = connect_mqtt()
    client.on_message = on_message  # Set fungsi on_message untuk handle pesan
    client.loop_start()

    publish_sound_data(client)  # Publish data sensor suara

    try:
        while True:
            # Melakukan apapun yang diperlukan selama program berjalan
            # Implementasi sensor suara di sini (jika diperlukan)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Cleaning up GPIO.")
        GPIO.cleanup()

# Bagian utama kode
if __name__ == '__main__':
    run()
