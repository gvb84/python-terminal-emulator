import pty, os,  subprocess, fcntl, termios
import struct, select, threading

from . import emulator

class TerminalProcessThread(threading.Thread):
	def __init__(self, rows, cols, cmd="/bin/sh"):
		super(TerminalProcessThread, self).__init__()

		self.pipes = os.pipe()
		self.pid, self.fd = pty.fork()
		if self.pid == 0:
			os.environ["TERM"] = "xterm-256color"
			ret = subprocess.call(cmd, close_fds=True)
			os.write(self.pipes[1], "\x00")
			os._exit(1)
		os.close(self.pipes[1])
		self.stopped = False
		
		self.emulator = emulator.Emulator(rows, cols)
		self.set_rowcol_pty()

	def input(self, data):
		ret = False
		try:
			ret = os.write(self.fd, bytes(data, encoding="utf-8"))
		except Exception as e:
			print(e)

	def stop(self):
		self.stopped = True

	def _run(self):
		timeout = 0.01
		i, o, e = select.select([self.fd, self.pipes[0]], [], [], timeout)
		if self.fd in i:
			try:
				data = os.read(self.fd, 4096)
				self.emulator.input_data(data)
			except:
				pass

		if self.pipes[0] in i:
			try:
				data = os.read(self.pipes[0], 1)
			except:
				pass
			self.stop()

	def run(self):
		while not self.stopped:
			self._run()

		os.close(self.fd)
		os.close(self.pipes[0])

	def set_rowcol_pty(self):
		data = struct.pack("HHHH", self.emulator.rows, self.emulator.cols, 0, 0)
		fcntl.ioctl(self.fd, termios.TIOCSWINSZ, data)
		attribute = termios.tcgetattr(self.fd)
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, attribute)

	def resize(self, rows, cols):
		# prevent unnecessary updates
		if rows == self.emulator.rows and cols == self.emulator.cols:
			return
		self.emulator.resize(rows, cols)
		self.set_rowcol_pty()	
