import os 
import glob 
import time 
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 
base_dir = '/sys/bus/w1/devices/' 
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave' 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines 
def read_ext_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp = float(temp_string) / 1000.0
        return temp
def read_cpu_temp():
  f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
  cpu_temp_raw = f.read()
  f.close()
  return float(cpu_temp_raw) / 1000.0	
while True:
	print "EXTERNAL: Temp C: {0}".format(read_ext_temp())
	print "CPU: Temp C: {0}\n".format(read_cpu_temp())
	time.sleep(0.5)
