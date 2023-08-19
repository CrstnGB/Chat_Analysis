import schedule
import time
import subprocess

def  ejecutar_script():
    subprocess.run(["python", "main.py"])

# Programar la ejecución cada 15 minutos
schedule.every(30).minutes.do(ejecutar_script)

while True:
    schedule.run_pending()
    time.sleep(1)