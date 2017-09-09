import os, pty, select, threading, signal
import queue
import multiprocessing
import termios, struct, fcntl

START = 0x1
EXITED = 0x2
DATA = 0x3
RESIZE = 0x4

class TerminalDriverProcess(multiprocessing.Process):
	def __init__(self, transport, queue, daemon=True):
		multiprocessing.Process.__init__(self, daemon=daemon)
		self.transport = transport
		self.queue = queue
		self.terminals = {}
		self.todelete = []
		self.stopped = False

	def sigchild(self, sig, frame):
		todelete = []
		for pid in self.terminals:
			ret = os.waitpid(pid, os.WNOHANG)
			if ret[0] == pid and ret[0] != 0:
				self.queue.put((pid, EXITED, None))
				self.todelete.append(pid)

	def startTerminal(self, cmd, args=[]):
		signal.signal(signal.SIGCHLD, self.sigchild)
		pid, fd = pty.fork()
		if pid == 0:
			args = [cmd] if len(args) == 0 else args
			os.execv(cmd, args)
			os._exit(1)
		
		self.terminals[pid] = fd
		return pid

	def resizeTerminal(self, pid, rows, cols):
		data = struct.pack("HHHH", rows, cols, 0, 0)
		fd = self.terminals[pid]
		fcntl.ioctl(fd, termios.TIOCSWINSZ, data)
		attr = termios.tcgetattr(fd)
		termios.tcsetattr(fd, termios.TCSAFLUSH, attr)

	def _run(self):
		for pid in self.todelete:
			del self.terminals[pid]
		self.todelete = []
		fds = [x for x in self.terminals.values()]
		transport_fd = self.transport.fileno()
		fds.append(transport_fd)

		i, o, e = select.select(fds, [], [], 0.01)

		if transport_fd in i:
			msg, cmd, args = self.transport.recv()
			if msg == START:
				pid = self.startTerminal(cmd, args)
				self.transport.send(pid)
			if cmd not in self.terminals:
				pass
			elif msg == DATA:
				fd = self.terminals[cmd]
				os.write(fd, args)
			elif msg == RESIZE:
				self.resizeTerminal(cmd, *args)

		for pid in self.terminals:
			fd = self.terminals[pid]
			if fd in i:
				try:
					data = os.read(fd, 4096)
					if len(data) == 0:
						continue
					self.queue.put((pid, DATA, data))
				except OSError:
					pass

	def run(self):
		while not self.stopped:
			self._run()

class TerminalCallbackThread(threading.Thread):
	def __init__(self, queue, queue2):
		threading.Thread.__init__(self)
		self.proc_queue = queue
		self.thread_queue = queue2
		self.callbacks = {}
		self.stopped = False

	def _run(self):
		try:
			pid, msg, data = self.proc_queue.get(0.01)
			if msg == EXITED:
				self.thread_queue.put((pid, EXITED, data))
			elif msg == DATA:
				if pid in self.callbacks:
					#$self.callbacks[pid].data(data)
					self.thread_queue.put((pid, DATA, data))
		except queue.Empty:
			pass

		try:
			pid, msg, data = self.thread_queue.get(0.01)
			if pid not in self.callbacks:
				if msg == START:
					self.callbacks[pid] = data	
					return
			if msg == EXITED:
				self.callbacks[pid].exited(data)
				del self.callbacks[pid]
			elif msg == DATA:
				if pid in self.callbacks:
					self.callbacks[pid].data(data)
		except queue.Empty:
			pass

	def run(self):
		while not self.stopped:
			self._run()

class TerminalDriver:
	def __init__(self):
		self.pipe = multiprocessing.Pipe()
		self.queue = multiprocessing.Queue()
		self.proc = TerminalDriverProcess(self.pipe[0], self.queue)
		self.proc.start()
		self.queue2 = queue.Queue()
		self.cb = TerminalCallbackThread(self.queue, self.queue2)
		self.cb.start()

	def startTerminal(self, cmd, args, cb):
		p = self.pipe[1]
		p.send((START, cmd, args))
		pid = int(p.recv())
		self.queue2.put((pid, START, cb))
		return pid

	def sendInput(self, terminal_id, data):
		p = self.pipe[1]
		if not data:
			data = ""
		data = data.encode("utf8")
		p.send((DATA, terminal_id, data))

	def resizeTerminal(self, terminal_id, rows, cols):
		p = self.pipe[1]
		p.send((RESIZE, terminal_id, (rows,cols)))

"""
class Test:
	def __init__(self):
		pass

	def exited(self, data):
		print("CALLBACK exited", data)

	def data(self, data):
		print("CALLBACK data", data)

test1 = Test()

td = TerminalDriver()
terminal_id = td.startTerminal("/bin/sh", [], test1)
td.sendInput(terminal_id, "ls -lha\n")
td.resizeTerminal(terminal_id, 30, 100)

import time
time.sleep(10)
print("done")
"""
