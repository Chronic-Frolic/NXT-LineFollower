import bluetooth as bluez
import nxt.backend.bluetooth
import nxt.locator
import nxt.sensor
import nxt.sensor.generic

from time import sleep

linea = 399
concreto = 465

setpoint = 440 #(linea + concreto)/2

base_action=50

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
        # Calcular una accion dependiendo del valor de la Luz
        action =  (1/15)*(setpoint - medida)
        # Enviar acciones a cada motor
        motorDerecha.run(max(-127,min(int(-base_action + action),127)), regulated=True)
        motorIzquierda.run(max(-127,min(int(-base_action - action),127)), regulated=True)
        # Esperar 0.2 segundos
        sleep(0.015)

        ## linea: 399
        ## concreto: 465