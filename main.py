from machine import Pin, PWM
from hcsr04 import HCSR04
from drv8833 import DRV8833
from time import sleep

distance_sensor_back = HCSR04(trigger_pin=8, echo_pin=4)
distance_sensor_front = HCSR04(trigger_pin=20, echo_pin=7)

front_ir =  Pin(2, Pin.IN)
back_ir =  Pin(3, Pin.IN)

start_module = Pin(0, Pin.IN)

frequency = 40_000

# Make sure to set the correct pins!
ain1 = PWM(Pin(5, Pin.OUT))
ain2 = PWM(Pin(6, Pin.OUT))
bin1 = PWM(Pin(9, Pin.OUT))
bin2 = PWM(Pin(10, Pin.OUT))
ain1.freq(frequency)
ain2.freq(frequency)
bin1.freq(frequency)
bin2.freq(frequency)

drv = DRV8833(ain1, ain2, bin1, bin2)

drv.stop_a()
drv.stop_b()


def drive_forward(speed):
    drv.throttle_a(speed)
    drv.throttle_b(speed)

def drive_backward(speed):
    drv.throttle_a(-1 * speed)
    drv.throttle_b(-1 * speed)

def drive_left(speed):
    drv.throttle_a(speed)
    drv.throttle_b(-1 * speed)

def drive_right(speed):
    drv.throttle_a(-1 * speed)
    drv.throttle_b(speed)    

def stop_drive():
    drv.stop_a()
    drv.stop_b()    


def init():
    ticks = 5
    while ticks > 0:
        drive_right(1)
        ticks = ticks - 1
        sleep(0.1)
    stop_drive()

def start():
    while True:
        while start_module.value() == 0:
            continue

        distance_front = distance_sensor_front.distance_cm()
        distance_back = distance_sensor_back.distance_cm()

        print('Distance front:', distance_front, 'cm')
        print('Distance back:', distance_back, 'cm')
        print('IR front:', str(front_ir.value()))
        print('IR back:', str(back_ir.value()))

        if front_ir.value() == 0:
            ticks = 5
            while ticks > 0:
                drive_backward(0.8)
                ticks = ticks - 1
                sleep(0.1)
            continue

        if back_ir.value() == 0:
            ticks = 5
            while ticks > 0:
                drive_forward(0.8)
                ticks = ticks - 1
                sleep(0.1)
            continue

        if (distance_front < 50):
            drive_forward(0.8)
            sleep(0.1)
            continue

        if (distance_back < 50):
            drive_backward(0.8) 
            sleep(0.1)
            continue   

        drive_right(0.4)

sleep(0.1)

while start_module.value() == 0:
    continue

init()
start()