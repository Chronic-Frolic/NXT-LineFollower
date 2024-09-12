import bluetooth as bluez
import nxt.backend.bluetooth
import nxt.locator
import nxt.sensor
import nxt.sensor.generic

from time import sleep

linea = 260
concreto = 320

setpoint = (linea + concreto)/2

Kp = 1/15
Kd = 0.01

base_action=50
prev_error = 0
timestep = 0.015

brick = nxt.backend.bluetooth.BluetoothSock(
    bluetooth=bluez, host='00:16:53:11:13:4D')
with brick.connect() as b:
    # Conectar el motor al puerto B
    motorDerecha   = b.get_motor(nxt.motor.Port.C)
    # Conectar el motor al puerto C
    motorIzquierda = b.get_motor(nxt.motor.Port.B)
    # Conectar el sensor de Luz al puerto 2
    sensorLuz = b.get_sensor(nxt.sensor.Port.S3, nxt.sensor.generic.Light)
    print("Presiona Ctrl-C para interrumpir el programa")
    while True:
        # Tomar la medida del sensor de Luz
        medida = sensorLuz.get_sample()
        print(medida)
        # Calcular error
        error = setpoint - medida
        # Calcular derivada del error
        derivative = (error - prev_error) / timestep
        prev_error = error
        # Calcular una accion dependiendo del valor de la Luz
        action = Kp * error + Kd * derivative
        # Enviar acciones a cada motor
        motorDerecha.run(max(-127,min(int(-base_action + action),127)), regulated=True)
        motorIzquierda.run(max(-127,min(int(-base_action - action),127)), regulated=True)
        # Esperar timestep segundos
        sleep(timestep)