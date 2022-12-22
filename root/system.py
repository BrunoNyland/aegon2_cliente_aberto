#favor manter essa linha
import enszxc3467hc3kokdueq as app
import os
import sys
import dbg


# sys.path = []
# sys.path.append("lib")

class TraceFile:
	def write(self, msg):
		dbg.Trace(msg)

class TraceErrorFile:
	def write(self, msg):
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)

class LogBoxFile:
	def __init__(self):
		self.stderrSave = sys.stderr
		self.msg = ""

	def __del__(self):
		self.restore()

	def restore(self):
		sys.stderr = self.stderrSave

	def write(self, msg):
		self.msg = self.msg + msg

	def show(self):
		dbg.LogBox(self.msg, "Error")

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()

import marshal
import imp
import xoFVEO7sP3AEkPgBSpnZ as pack

class pack_file_iterator(object):
	def __init__(self, packfile):
		self.pack_file = packfile

	def next(self):
		tmp = self.pack_file.readline()
		if tmp:
			return tmp
		raise StopIteration

_chr = builtins.chr

class pack_file(object):
	def __init__(self, filename, mode = 'rb'):
		assert mode in ('r', 'rb')
		if not pack.Exist(filename):
			raise(IOError, 'No file or directory')
		self.data = pack.Get(filename)
		if mode == 'r':
			self.data = _chr(10).join(self.data.split(_chr(13) + _chr(10)))

	def __iter__(self):
		return pack_file_iterator(self)

	def read(self, len = None):
		if not self.data:
			return ''
		if len:
			tmp = self.data[:len]
			self.data = self.data[len:]
			return tmp
		else:
			tmp = self.data
			self.data = ''
			return tmp

	def readline(self):
		return self.read(self.data.find(_chr(10))+1)

	def readlines(self):
		return [x for x in self]

old_open = open
def open(filename, mode = 'rb'):
	if pack.Exist(filename) and mode in ('r', 'rb'):
		return pack_file(filename, mode)
	else:
		return old_open(filename, mode)

builtins.open = open
builtins.old_open = old_open
builtins.new_open = open
builtins.pack_open = open
_ModuleType = type(sys)

old_import = __import__
def _process_result(code, fqname):
	is_module = isinstance(code, _ModuleType)

	if is_module:
		module = code
	else:
		module = imp.new_module(fqname)

	sys.modules[fqname] = module

	if not is_module:
		exec(code , module.__dict__)

	module = sys.modules[fqname]
	module.__name__ = fqname
	return module

module_do = lambda x:None

if __USE_CYTHON__:
	import rootlib

if app.BLOCK_CHANGE_NAME_BIN:
	if str(sys.executable)[-14:] != "mt2supremo.bin":
		try:
			os.Execute("start Mt2Supremo.exe")
		except BaseException:
			pass

		app.Abort()

def __hybrid_import(name, globals = None, locals = None, fromlist = None, level = -1):
	if __USE_CYTHON__ and rootlib.isExist(name):
		if name in sys.modules:
			dbg.Tracen('importing from sys.modules %s' % name)
			return sys.modules[name]
		dbg.Tracen('importing from rootlib %s' % name)
		newmodule = rootlib.moduleImport(name)
		module_do(newmodule)
		sys.modules[name] = newmodule
		return newmodule
	else:
		filename = 'root/' + name + '.py'
		if not __USE_CYTHON__ and pack.Exist(filename):
			if name in sys.modules:
				dbg.Tracen('importing from sys.modules %s' % name)
				return sys.modules[name]

			dbg.Tracen('importing from pack %s' % name)
			newmodule = _process_result(compile(pack_file(filename,'r').read(), filename, 'exec'), name)
			module_do(newmodule)
			return newmodule
		else:
			dbg.Tracen('importing from lib %s' % name)
			return old_import(name, globals, locals, fromlist)

def splitext(p):
	root, ext = '', ''
	for c in p:
		if c in ['/']:
			root, ext = root + ext + c, ''
		elif c == '.':
			if ext:
				root, ext = root + ext, c
			else:
				ext = c
		elif ext:
			ext = ext + c
		else:
			root = root + c
	return root, ext

def __IsCompiledFile__(sFileName):
	sBase, sExt = splitext(sFileName)
	sExt = sExt.lower()
	if sExt == ".pyc" or sExt == ".pyo":
		return 1
	else:
		return 0

def __LoadTextFile__(sFileName):
	sText = open(sFileName,'r').read()
	return compile(sText, sFileName, "exec")

def __LoadCompiledFile__(sFileName):
	kFile = open(sFileName)
	if kFile.read(4) != imp.get_magic():
		raise

	kFile.read(4)

	kData = kFile.read()
	return marshal.loads(kData)

def execfile(fileName, dict):
	if __IsCompiledFile__(fileName):
		code = __LoadCompiledFile__(fileName)
	else:
		code = __LoadTextFile__(fileName)
		exec(code , dict)

__import__ = __hybrid_import
# builtins.old_execfile = builtins.execfile
# builtins.execfile = execfile

def GetExceptionString(excTitle):
	(excType, excMsg, excTraceBack) = sys.exc_info()
	excText = ""
	excText += _chr(10)

	import traceback
	traceLineList = traceback.extract_tb(excTraceBack)

	for traceLine in traceLineList:
		if traceLine[3]:
			excText += "%s(line:%d) %s - %s" % (traceLine[0], traceLine[1], traceLine[2], traceLine[3])
		else:
			excText += "%s(line:%d) %s" % (traceLine[0], traceLine[1], traceLine[2])
		excText += _chr(10)

	excText += _chr(10)
	excText += "%s - %s:%s" % (excTitle, excType, excMsg)
	excText += _chr(10)

	return excText


def ShowException(excTitle):
	excText = GetExceptionString(excTitle)
	dbg.TraceError(excText)
	app.Abort()
	return 0

def RunMainScript(name):
	# try:
	execfile(name, __main__.__dict__)
	# except RuntimeError as msg:
		# msg = str(msg)

		# import localeinfo
		# if localeinfo.error:
			# msg = localeinfo.error.get(msg, msg)

		# dbg.LogBox(msg)
		# app.Abort()

	# except BaseException:
		# msg = GetExceptionString("Run")
		# dbg.LogBox(msg)
		# app.Abort()

import debuginfo
debuginfo.SetDebugMode(__DEBUG__)
dbg.TraceError("passei aqui fora do if")

loginMark = "-cs"

if __USE_CYTHON__:
	dbg.TraceError("passei aqui")
	import __main__
	__hybrid_import('Prototype', __main__.__dict__)
else:
	dbg.TraceError("passei aqui")
	RunMainScript("root/prototype.py")
dbg.TraceError("passei aqui depois do if")
	