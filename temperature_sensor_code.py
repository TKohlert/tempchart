import os
import glob
import time
import datetime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
device_files = []
for folder in device_folders:
  device_files.append(folder + '/w1_slave')

output_file = os.path.expanduser('~/temps/sensor1.csv')

 
#def read_temp_raw():
#    f = open(device_file, 'r')
#    lines = f.readlines()
#    f.close()
#    return lines

def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

 
def read_temp(file):
    lines = read_temp_raw(file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c,temp_f
	

out = open(output_file, "w")

while True:
        for file in device_files:
        	ts = str(datetime.datetime.now())
		c,f = read_temp(file)
        #	out.write("{},{},{}\n".format(ts,c,f))
        #out.flush()
		print("{},{},{},{}\n".format(file,ts,c,f))
	time.sleep(1)
