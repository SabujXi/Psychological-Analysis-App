import serial


# def send_data_to_device(self, temp_value=32):
#     #    Call without arg for resetting to 32
#     # print("Sending value to device")
#     # self.controller.device.set_temperature(temps_value)
#     pass
class Device:
    def __init__(self, config, manager):
        self.manager = manager
        self.config = config
        if not self.config.EXPERIMENT['DEV']:
            self.ser = serial.Serial(config.SERIAL['port'], config.SERIAL['baudrate'])
            line3 = self.ser.readline()
            print line3
            self.ser.write("$CMD,0000,07")
            self.ser.readline()

    def set_neutral_temperature(self):
        print 'DEVICE SAYS: set neutral temperature'
        self.reset_temperature()

    def reset_temperature(self):
        print 'DEVICE SAYS: reset temperature to 32'
        if not self.config.EXPERIMENT['DEV']:
            self.set_temperature(32)
            return

    def set_temperature(self, temperature):
        """
            ROC(rate of change of temperature) is 3degree/second.
        """
        print 'DEVICE SAYS: set temperature to', temperature
        #  return
        #  return for now, device is not connected. remove it after we're connecting to the device
        #  self.ser = serial.Serial(config.SERIAL['port'], config.SERIAL['baudrate'])

        if not self.config.EXPERIMENT['DEV']:
            if(self.ser):
                self.ser.write("$CMD,0000,08")
                self.ser.readline()
                print("Serial port" + self.ser.portstr + " opened.")
                self.ser.write("$CMD," + hex(temperature * 10)[2:].zfill(4) + ",01")
                line1 = self.ser.readline()
                print line1
                self.ser.write("$CMD," + hex(temperature * 10)[2:].zfill(4) + ",02")
                #  line2=self.ser.readline()
                #  print line2
