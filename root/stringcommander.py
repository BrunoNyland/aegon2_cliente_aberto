#favor manter essa linha
from weakref import proxy

class CallBackFunction:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls = cls
			self.obj = proxy(obj)
			self.func = proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls = cls
			self.obj = proxy(obj)
			self.func = proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		self.argCount = mfunc.__code__.co_argcount

		if self.argCount > 1:
			self.call = CallBackFunction.__arg_call__(mfunc.__class__, mfunc.__self__, mfunc.__func__)
		else:
			self.call = CallBackFunction.__noarg_call__(mfunc.__class__, mfunc.__self__, mfunc.__func__)

	def __call__(self, *arg):
		return self.call(*arg)

	def GetArgumentCount(self):
		return self.argCount

class Analyzer:
	def __init__(self):
		self.cmdDict = {}

	def SAFE_RegisterCallBack(self, cmd, callBackFunc):
		self.cmdDict[cmd] = CallBackFunction(callBackFunc)

	def Run(self, line):
		tokens = line.split()

		if len(tokens) == 0:
			return 1

		cmd = tokens.pop(0)

		try:
			callBackFunc = self.cmdDict[cmd]
		except KeyError:
			return 0

		argCount = callBackFunc.GetArgumentCount() - 1

		if len(tokens) < argCount:
			raise(RuntimeError, "Analyzer.Run(line=%s) - cmd=%s, curArgCount[%d]<needArgCount[%d]" % (line, cmd, len(tokens), argCount))
		else:
			tokens = tokens[:argCount]
			callBackFunc(*tokens)
			return 1