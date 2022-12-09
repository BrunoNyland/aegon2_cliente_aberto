@echo off
del Metin2_releaseMode.exe
echo Binario Antigo Removido!
copy /y C:\Desenvolvimento\_Cliente_Source_\client\out\Metin2_releaseMode.exe Metin2_releaseMode.exe
copy /y C:\Desenvolvimento\_Cliente_Source_\client\out\Metin2_DebugMode.exe Metin2_DebugMode.exe
copy /y C:\Desenvolvimento\_Cliente_Source_\client\out\Metin2_DebugMode.map Metin2_DebugMode.map
copy /y C:\Desenvolvimento\_Cliente_Source_\client\out\Metin2_DebugMode.pdb Metin2_DebugMode.pdb
echo Binario Novo Copiado!