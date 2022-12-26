###########################################################
# Python files must be in utf-8 encoding to work properly #
###########################################################

# imports from client binary
import enszxc3467hc3kokdueq as app
import xoFVEO7sP3AEkPgBSpnZ as pack
import dbg

# imports from dll
import sys
import builtins
import marshal

# imports from lib folder
import imp
import os
from typing import TextIO
from io import IOBase

###########################################
# Definições dos arquivos de logs e erros #
###########################################
class TraceFile(TextIO):
	def write(self, msg:str) -> None:
		dbg.Trace(msg)

	def flush(self) -> None:
		pass

class TraceErrorFile(TextIO):
	def write(self, msg:str) -> None:
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)

	def flush(self) -> None:
		pass

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()

########################################################
# Definição das funções de abrir arquivos: open e pack #
########################################################
class pack_file_iterator(IOBase):
	def __init__(self, packfile:IOBase) -> None:
		self.pack_file = packfile

	def __next__(self) -> str:
		tmp = self.pack_file.readline()
		if tmp:
			return tmp
		raise StopIteration

_chr = builtins.chr

class pack_file(IOBase):
	def __init__(self, filename:str, mode:str='rb') -> None:
		if not mode in ('r', 'rb'):
			raise(IOError, 'system.py:pack_file: Invalid mode: %s' % (mode))
		if not pack.Exist(filename):
			raise(IOError, 'system.py:pack_file: No file or directory [%s]' % (filename))

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
def open_modified(filename:str, mode:str='rb'):
	if pack.Exist(filename):
		if not mode in ('r', 'rb'):
			raise(IOError, 'system.py:open: Invalid mode: %s' % (mode))
		dbg.TraceError('Carregando arquivo via pack: %s' % filename)
		return pack_file(filename, mode)
	else:
		return old_open(filename, mode)

builtins.open = open_modified

_ModuleType = type(sys)

old_import = builtins.__import__

def _process_result(code, fqname):
	is_module = isinstance(code, _ModuleType)

	if is_module:
		module = code
	else:
		module = imp.new_module(fqname)

	sys.modules[fqname] = module

	if not is_module:
		exec(code, module.__dict__)

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
		raise BaseException('__LoadCompiledFile__')

	kFile.read(4)

	kData = kFile.read()
	return marshal.loads(kData)

def execfile(fileName, dict):
	if __IsCompiledFile__(fileName):
		code = __LoadCompiledFile__(fileName)
	else:
		code = __LoadTextFile__(fileName)
		exec(code, dict)

__import__ = __hybrid_import
builtins.__import__ = __hybrid_import

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

def RunMainScript(name):
	try:
		execfile(name, __main__.__dict__)
	except RuntimeError as msg:
		msg = str(msg)

		import localeinfo
		if localeinfo.error:
			msg = localeinfo.error.get(msg, msg)

		dbg.LogBox(msg)
		app.Abort()

	except BaseException:
		msg = GetExceptionString("Run")
		dbg.LogBox(msg)
		app.Abort()

import debuginfo
debuginfo.SetDebugMode(__DEBUG__)



if __USE_CYTHON__:
	import __main__
	__hybrid_import('Prototype', __main__.__dict__)
else:
	RunMainScript("root/prototype.py")
