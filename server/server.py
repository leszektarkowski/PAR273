import gpib

class PARWriteError(Exception):
    pass

class PARReadError(Exception):
    pass

class PARCellWorking(Exception):
    pass

class Poll:
    COMMAND_DONE  = 1
    COMMAND_ERROR = 2
    CURVE_DONE    = 4
    OVERLOAD      = 16
    SWEEP_DONE    = 32
    SRQ           = 64
    OUTPUT_READY  = 128

class PAR(object):
    def __init__(self, addres):
        self.dev = gpib.dev(*addres)
        self.write('DD 13')
        self.write('TYPE Succesfull init"')

    def write(self, cmd):		
        while True:            
            status = ord(gpib.serial_poll(self.dev))
            #print '.',
            if status & Poll.COMMAND_DONE != 0:
                break
            elif status & Poll.OUTPUT_READY != 0:
                raise PARWriteError("Data is ready, can't write")
        gpib.write(self.dev, cmd)

    def read(self):
        while True:            
            status = ord(gpib.serial_poll(self.dev))
            #print ':', status,
            if status & Poll.OUTPUT_READY != 0:
                break
            elif status & Poll.COMMAND_DONE != 0:
                raise PARReadError("Nothing to read")
        return gpib.read(self.dev, 1024)

    def ask(self, cmd):
        self.write(cmd)
        return self.read()

    def wait_for_relay(self):        
        cell_hw_switch = int(p.ask("CS").split()[0])
        cell_relay = int(p.ask("CELL").split()[0])
        if cell_hw_switch and cell_relay:
            raise PARCellWorking("Both cell switches enabled")
        elif cell_hw_switch == False and cell_relay:
            raise PARCellWorking("Cell relay in waiting status...")
        elif cell_hw_switch == True and cell_relay == False:
            raise PARCellWorking("Previous measurement not finished!")
        elif cell_hw_switch == False and cell_relay == False:
            for i in range(100):
                print "Press Cell Switch!"
                import time
                time.sleep(0.2)
                cell_hw_switch = int(p.ask("CS").split()[0])
                if cell_hw_switch:
                    p.write("CELL 1")
                    print "Measurement started"
                    return True
            return False


p = PAR( (0,14) )




