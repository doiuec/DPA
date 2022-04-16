import pyvisa
import numpy
import matplotlib.pyplot as plot
import sys
import time

class MSO:
    def __init__(self):
        rm = pyvisa.ResourceManager() #インスタンス作成
        inst = rm.list_resources() #VISAリソース名の取得
        usb = list(filter(lambda x: "USB" in x, inst)) #inst配列から"USB"とつくものを抽出、usb配列へ

        if len(usb) != 1: #二個以上接続されてたらアカン
            print('Bad instrument list', inst)
            sys.exit(-1)

        self.scope = rm.open_resource(usb[0], timeout=5000, chunk_size=10 * 1024 * 1024) # オシロの型番を特定、渡す

    def get_data(self):
        
        self.scope.write(":WAV:DATA?") #Request the data
        time.sleep(2)
        #while self.scope.query('*OPC?')[0]!="1":
        #    print("Waiting")
        #    time.sleep(1)
        #rawdata = self.scope.read_binary_values()
        #while self.scope.query('*OPC?')[0]!="1":
        #    print("Waiting")
        #    time.sleep(1)
        rawdata = self.scope.read_raw() #Read the block of data
        #print(rawdata)
        rawdata = rawdata[ 10 : ] #Drop the heading
        data_size = len(rawdata)
        #print(rawdata)
        #sample_rate = self.scope.query(':ACQ:SRAT?')[0]
        #print('Data size:', data_size, "Sample rate:", sample_rate)
        return rawdata
        
    def close(self):
        self.scope.close()

    def grapf(self):
        self.scope.write(":STOP")

        # Get the timescale
        timescale = float(self.scope.query(":TIM:SCAL?"))

        # Get the timescale offset
        timeoffset = float(self.scope.query(":TIM:OFFS?")[0])

        voltscale = float(self.scope.query(':CHAN1:SCAL?')[0])

        # And the voltage offset
        voltoffset = float(self.scope.query(":CHAN1:OFFS?")[0])

        self.scope.write(":WAV:DATA? CHAN1") #Request the data
        rawdata = self.scope.read_raw() #Read the block of data
        rawdata = rawdata[ 10 : ] #Drop the heading
        data_size = len(rawdata)
        sample_rate = self.scope.query(':ACQ:SRAT?')[0]
        print('Data size:', data_size, "Sample rate:", sample_rate)

        self.scope.write(":KEY:FORCE")
        self.scope.close()

        data = numpy.frombuffer(rawdata, 'B')

        # Walk through the data, and map it to actual voltages
        # This mapping is from Cibo Mahto
        # First invert the data
        data = data * -1 + 255

        # Now, we know from experimentation that the scope display range is actually
        # 30-229.  So shift by 130 - the voltage offset in counts, then scale to
        # get the actual voltage.
        data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale

        # Now, generate a time axis.
        time = numpy.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data))

        # See if we should use a different time axis
        if (time[-1] < 1e-3):
            time = time * 1e6
            tUnit = "uS"
        elif (time[-1] < 1):
            time = time * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"

        # Plot the data
        plot.plot(time, data)
        plot.title("Oscilloscope Channel 1")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (" + tUnit + ")")
        plot.xlim(time[0], time[-1])
        plot.show()
