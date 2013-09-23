import gpib

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
		write('DD 13')
		write('TYPE Succesfull init"')

	def write(cmd):		
		while(true):
			status = gpib.serial_poll(self.dev)
			if (status & Poll.COMMAND_DONE != 0)
				break
		gpib.write(self.dev, cmd)

	def read():
		while(true):
			status = gpib.serial_poll(self.dev)
			if (status & Pool.OUTPUT_READY != 0)
				break
		return gpib.read(self.dev)







