import serial


class Device:
    def __init__(self, config, manager):
        self.manager = manager
        self.config = config
        if not self.config.EXPERIMENT['DEV']:
            self.ser = serial.Serial(config.SERIAL['port'], config.SERIAL['baudrate'])
            line3 = self.ser.readline()
            self.manager.info(line3)
            self.ser.write("$CMD,0000,07")
            self.ser.readline()

    def set_neutral_temperature(self):
        self.manager.info('DEVICE SAYS: set neutral temperature')
        self.reset_temperature()

    def reset_temperature(self):
        self.manager.info('DEVICE SAYS: reset temperature to 32')
        if not self.config.EXPERIMENT['DEV']:
            self.set_temperature(32)
            return

    def set_temperature(self, temperature):
        """
            ROC(rate of change of temperature) is 3degree/second.
        """
        self.manager.info('DEVICE SAYS: set temperature to', temperature)

        if not self.config.EXPERIMENT['DEV']:
            if(self.ser):
                self.ser.write("$CMD,0000,08")
                self.ser.readline()
                self.manager.info("Serial port" + self.ser.portstr + " opened.")
                self.ser.write("$CMD," + hex(temperature * 10)[2:].zfill(4) + ",01")
                line1 = self.ser.readline()
                self.manager.info(line1)
                self.ser.write("$CMD," + hex(temperature * 10)[2:].zfill(4) + ",02")
