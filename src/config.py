neutral_stimuli = init_temp = 32      # 32'c

port = "COM40"

#  If developer mode is on then remove the hash mark from <developer_mode = True> and put hash mark before
#  <developer_mode = True> and vice versa.

# developer_mode = False
developer_mode = True

'''
TEMP    - Temperature only page show time
TEMP_TEXT - Text shown in temperature only page
IMAGE   - mage showing time, in seconds and should >=1
SAM     - SAM page displaying showing time , in seconds, and shuld >=1
EMOTION - Emotional wheel page displaying showing time , in seconds, and should >=1
NUMBER  - The number of images to be displayed in one experiment, and should >=1 and <=136
DEV 	- Indicate if the running mode is development mode(in development mode, temperature setting on device will not happen), change back to False when deliver to customer
INFORMATION_TEXT - Text to before showing the image view.
INFORMATION_DISPLAY_TIME - Information page display tie, in seconds, and should >=1
'''
EXPERIMENT = {
    'DEV': developer_mode,
}

'''
port 	  - The device name. Depending on operating system. e.g. COM3 on Windows or /dev/ttyUSB0 on GNU/Linux(Now, the application is only verified on Windows)

baudrate  - According to the device doc, it should be 460800. Change it if it's not the case
'''
SERIAL = {
    'port': port,
    'baudrate': 460800
}

'''
Temprautes to be shown for each folder, combining the display size
0: Small
1: Medium
2: Large 
'''
TEMPRATURES = [
    [26 * 2, 0], [29 * 2, 0], [32 * 2, 0], [35 * 2, 0], [38 * 2, 0],
    [26 * 2, 1], [29 * 2, 1], [32 * 2, 1], [35 * 2, 1], [38 * 2, 1],
    [26 * 2, 2], [29 * 2, 2], [32 * 2, 2], [35 * 2, 2], [38 * 2, 2]
]

'''
Image Display size text to be stored in experiement result.
0: Small
1: Medium
2: Large 
'''
DISPLAY = {
    0: 'small',
    1: 'medium',
    2: 'large'
}

'''
Image Display size
0: Small size
1: Medium size
2: Large  size
'''
DISPLAY_SIZE = {
    0: [522, 267],
    1: [822, 514],
    2: [1292, 735]
}


DISPLAY_DURATIONS = {
    'default': -1
}
