from time import sleep
import serial
import sys

port = "COM43"

# print(sys.argv)
port = sys.argv[1]

sys.stdout.write("==== STM32Trigger by ArtronShop CO.,LTD. ====\n")

sys.stdout.write("Serial port {}\n".format(port))
serialPort = serial.Serial(port, baudrate=115200, bytesize=8, timeout=0.1, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_EVEN)

enter_bootloader_ok = False
sys.stdout.write("Connect")
for i in range(100000):
    sys.stdout.write("-")
    sys.stdout.flush()
    
    # Enter to Bootloader
    serialPort.rts = 1
    serialPort.dtr = 0
    sleep(0.02)
    serialPort.dtr = 1
    serialPort.rts = 0
    sleep(0.02)
    serialPort.rts = 0
    serialPort.dtr = 0

    # Try to get Chip ID
    for i in range(5):
        sleep(0.3)
        sys.stdout.write(".")
        sys.stdout.flush()

        # Clear old data
        serialPort.reset_input_buffer()

        # USARTx selected
        serialPort.write(bytes([ 0x7F ]))
        sleep(0.1)
        while serialPort.in_waiting:
            got = serialPort.read(1)
            if len(got) > 0 :
                if got[0] == 0x79:
                    # sys.stdout.write("Get ACK\n")
                    sys.stdout.write(" Connected\n")
                    sys.stdout.flush()
                    enter_bootloader_ok = True
                # elif got[0] == 0x1F:
                #     sys.stdout.write("Get NACK\n")
            else:
                continue

        # Clear old data
        serialPort.reset_input_buffer()
        """
        # Get Chip ID
        
        serialPort.write(bytes([ 0x02, 0xFD ]))
        got = serialPort.read(1)
        if len(got) > 0 :
            if got[0] == 0x79:
                # sys.stdout.write("Get ACK")
                got = serialPort.read(4)
                if got[0] == 1: # N = the number of bytes – 1
                    if got[3] == 0x79: # ACK
                        sys.stdout.write("\nChip ID: 0x{}".format(got[1:3].hex()))
                        enter_bootloader_ok = True
                        
            elif got[0] == 0x1F:
                sys.stdout.write("Get NACK\n")
        """
        
        if enter_bootloader_ok:
            break
    if enter_bootloader_ok:
        break

if not enter_bootloader_ok:
    sys.stdout.write(" FAIL!\n")

serialPort.close()



"""    
try:
    serialPort = serial.Serial(port = "COM7", baudrate=19200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    sys.stdout.write("OK the port is opened!")
    v_text = "R \n"
    serialPort.write(v_text.encode())
    sys.stdout.write("Writing "+v_text)
    sleep(2)
    while(1):
 
        if(serialPort.in_waiting > 0):
            serialString = serialPort.readline()
            # convert bytes to string
            captured_data = serialString.decode('Ascii')
            sys.stdout.write("Reading "+captured_data)
            break
        else:
            sys.stdout.write("no data yet")
        sleep(1)
 
except  serial.SerialException as error:
    sys.stdout.write("Failed  {}".format(error))
"""
