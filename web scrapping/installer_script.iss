; Inno Setup Script for PU PYQ Downloader (OneDir Build)

[Setup]
AppName=PU PYQ Downloader
AppVersion=1.0
DefaultDirName={pf}\PU_PYQ_Downloader
DefaultGroupName=PU PYQ Downloader
OutputBaseFilename=PU_PYQ_Installer
SetupIconFile=download_arrow_14460.ico
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
Source: "C:\py_programs\app\dist\new_pyq_ext_app\new_pyq_ext_app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\py_programs\app\dist\new_pyq_ext_app\*"; Excludes: "new_pyq_ext_app.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
Name: "{group}\PU PYQ Downloader"; Filename: "{app}\new_pyq_ext_app.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall PU PYQ Downloader"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\new_pyq_ext_app.exe"; Description: "Launch PU PYQ Downloader"; Flags: nowait postinstall skipifsilent
