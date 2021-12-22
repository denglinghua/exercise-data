ilmerge /lib:..\bin\Debug\ /target:winexe /out:run.exe RunData.exe ICSharpCode.SharpZipLib.dll NPOI.dll NPOI.OOXML.dll NPOI.OpenXml4Net.dll NPOI.OpenXmlFormats.dll
copy ..\bin\Debug\RunData.exe.config run.exe.config
