;NSIS Modern User Interface
;Multilingual Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "PhanterPS2"
  !define MUI_ICON "setup.ico"
  !define MUI_UNICON "unist.ico"
  !define MUI_HEADERIMAGE
  !define MUI_WELCOMEFINISHPAGE_BITMAP "grande.bmp"
  !define MUI_HEADERIMAGE_BITMAP_RTL "pequeno.bmp"
  !define MUI_HEADERIMAGE_RIGHT
  !define MUI_HEADERIMAGE_BITMAP "pequeno.bmp"

  OutFile "SETUP.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\PhanterPS2"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\PhanterPS2" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Language Selection Dialog Settings

  ;Remember the installer language
  !define MUI_LANGDLL_REGISTRY_ROOT "HKCU" 
  !define MUI_LANGDLL_REGISTRY_KEY "Software\PhanterPS2" 
  !define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"

;--------------------------------
;Pages
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "license.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages
  !insertmacro MUI_LANGUAGE "PortugueseBR" ;first language is the default language
  !insertmacro MUI_LANGUAGE "English" 
  !insertmacro MUI_LANGUAGE "French"
  !insertmacro MUI_LANGUAGE "German"
  !insertmacro MUI_LANGUAGE "Spanish"
  !insertmacro MUI_LANGUAGE "SpanishInternational"
  !insertmacro MUI_LANGUAGE "SimpChinese"
  !insertmacro MUI_LANGUAGE "TradChinese"
  !insertmacro MUI_LANGUAGE "Japanese"
  !insertmacro MUI_LANGUAGE "Korean"
  !insertmacro MUI_LANGUAGE "Italian"
  !insertmacro MUI_LANGUAGE "Dutch"
  !insertmacro MUI_LANGUAGE "Danish"
  !insertmacro MUI_LANGUAGE "Swedish"
  !insertmacro MUI_LANGUAGE "Norwegian"
  !insertmacro MUI_LANGUAGE "NorwegianNynorsk"
  !insertmacro MUI_LANGUAGE "Finnish"
  !insertmacro MUI_LANGUAGE "Greek"
  !insertmacro MUI_LANGUAGE "Russian"
  !insertmacro MUI_LANGUAGE "Portuguese"
  !insertmacro MUI_LANGUAGE "Polish"
  !insertmacro MUI_LANGUAGE "Ukrainian"
  !insertmacro MUI_LANGUAGE "Czech"
  !insertmacro MUI_LANGUAGE "Slovak"
  !insertmacro MUI_LANGUAGE "Croatian"
  !insertmacro MUI_LANGUAGE "Bulgarian"
  !insertmacro MUI_LANGUAGE "Hungarian"
  !insertmacro MUI_LANGUAGE "Thai"
  !insertmacro MUI_LANGUAGE "Romanian"
  !insertmacro MUI_LANGUAGE "Latvian"
  !insertmacro MUI_LANGUAGE "Macedonian"
  !insertmacro MUI_LANGUAGE "Estonian"
  !insertmacro MUI_LANGUAGE "Turkish"
  !insertmacro MUI_LANGUAGE "Lithuanian"
  !insertmacro MUI_LANGUAGE "Slovenian"
  !insertmacro MUI_LANGUAGE "Serbian"
  !insertmacro MUI_LANGUAGE "SerbianLatin"
  !insertmacro MUI_LANGUAGE "Arabic"
  !insertmacro MUI_LANGUAGE "Farsi"
  !insertmacro MUI_LANGUAGE "Hebrew"
  !insertmacro MUI_LANGUAGE "Indonesian"
  !insertmacro MUI_LANGUAGE "Mongolian"
  !insertmacro MUI_LANGUAGE "Luxembourgish"
  !insertmacro MUI_LANGUAGE "Albanian"
  !insertmacro MUI_LANGUAGE "Breton"
  !insertmacro MUI_LANGUAGE "Belarusian"
  !insertmacro MUI_LANGUAGE "Icelandic"
  !insertmacro MUI_LANGUAGE "Malay"
  !insertmacro MUI_LANGUAGE "Bosnian"
  !insertmacro MUI_LANGUAGE "Kurdish"
  !insertmacro MUI_LANGUAGE "Irish"
  !insertmacro MUI_LANGUAGE "Uzbek"
  !insertmacro MUI_LANGUAGE "Galician"
  !insertmacro MUI_LANGUAGE "Afrikaans"
  !insertmacro MUI_LANGUAGE "Catalan"
  !insertmacro MUI_LANGUAGE "Esperanto"

;--------------------------------
;Reserve Files
  
  ;If you are using solid compression, files that are required before
  ;the actual installation should be stored first in the data block,
  ;because this will make your installer start faster.
  
  !insertmacro MUI_RESERVEFILE_LANGDLL

;--------------------------------
;Installer Sections

Section "!PhanterPS2 (Requerido)" SecDummy 
  SectionIn RO

  
  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  File "PhanterPS2\*.*"

  SetOutPath "$INSTDIR\imagens"
  File "PhanterPS2\imagens\*.*"

  SetOutPath "$INSTDIR\Microsoft.VC90.CRT"
  File "PhanterPS2\Microsoft.VC90.CRT\*.*"

  ;Store installation folder
  WriteRegStr HKCU "Software\PhanterPS2" "" $INSTDIR


  ;Create uninstaller
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2" "DisplayName" "PhanterPS2"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2" "DisplayIcon" "$INSTDIR\PhanterPS2.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2" "NoRepair" 1
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\PhanterPS2.exe" "" "$INSTDIR\PhanterPS2.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\PhanterPS2.exe" path $INSTDIR
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Links" SecDummylinks
  SetOutPath "$INSTDIR"

  CreateDirectory "$SMPROGRAMS\PhanterPS2"
  CreateShortCut "$SMPROGRAMS\PhanterPS2\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\PhanterPS2\PhanterPS2.lnk" "$INSTDIR\PhanterPS2.exe" "" "$INSTDIR\PhanterPS2.exe" 0
  CreateShortCut "$SMPROGRAMS\PhanterPS2\PhanterPS2Full.lnk" "$INSTDIR\PhanterPS2Full.exe" "" "$INSTDIR\PhanterPS2Full.exe" 0
  CreateShortCut "$DESKTOP\PhanterPS2.lnk" "$INSTDIR\PhanterPS2.exe" "" "$INSTDIR\PhanterPS2.exe" 0
  
SectionEnd

Section "Sourcer code" SecDummysource

  SetOutPath "$INSTDIR\src"
  
  ;ADD YOUR OWN FILES HERE...

  File "PhanterPS2\src\*.*"

SectionEnd

Section "idioma es-ES" SecDummyespanhol

  SetOutPath "$APPDATA\phanterps2\linguagem"
  
  ;ADD YOUR OWN FILES HERE...

  File "es-ES\*.*"
  File "sample.lng"
  SetOutPath "$APPDATA\phanterps2"
  File "es-ES\phanterps2.cfg"


SectionEnd

Section "en-US language" SecDummyingles

  SetOutPath "$APPDATA\phanterps2\linguagem"
  
  ;ADD YOUR OWN FILES HERE...

  File "en-US\en-US.lng"
  File "sample.lng"
  SetOutPath "$APPDATA\phanterps2"
  File "en-US\phanterps2.cfg"

SectionEnd
Section
  AccessControl::GrantOnFile "$INSTDIR" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR\imagens" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR\src" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR\library.zip" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR\PhanterPS2FULL.exe.log" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$APPDATA\phanterps2" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$APPDATA\phanterps2\linguagem" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$APPDATA\phanterps2\phanterps2.cfg" "(S-1-5-32-545)" "FullAccess"
  AccessControl::GrantOnFile "$APPDATA\phanterps2\imagemcheck.cfg" "(S-1-5-32-545)" "FullAccess"
SectionEnd


;--------------------------------
;Installer Functions

Function .onInit

  !insertmacro MUI_LANGDLL_DISPLAY


FunctionEnd

;--------------------------------
;Descriptions

  ;USE A LANGUAGE STRING IF YOU WANT YOUR DESCRIPTIONS TO BE LANGAUGE SPECIFIC

  ;Assign descriptions to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} "Instala o programa PhanterPS2 - Install the program PhanterPS2"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummylinks} "Cria links no desktop e no Menu  Iniciar - Create Desktop links and Start Menu links"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummysource} "Copiar source-code - Copy source-code"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummyespanhol} "Suporte ao Espanhol - Apoyo en el idioma español"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummyingles} "Suporte ao Inglês - English suport"
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

 
;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...
  Delete "$INSTDIR\*.*"
  Delete "$APPDATA\phanterps2\linguagem\*.*"
  Delete "$APPDATA\phanterps2\*.*"
  Delete "$INSTDIR\imagens\*.*"
  Delete "$INSTDIR\src\*.*"
  Delete "$INSTDIR\Microsoft.VC90.CRT\*.*"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$DESKTOP\PhanterPS2\PhanterPS2.lnk"
  Delete "$DESKTOP\PhanterPS2\PhanterPS2FULL.lnk"
  Delete "$SMPROGRAMS\PhanterPS2\Uninstall.lnk"
  Delete "$SMPROGRAMS\PhanterPS2\PhanterPS2.lnk"
  Delete "$SMPROGRAMS\PhanterPS2\PhanterPS2FULL.lnk"
  Delete "$DESKTOP\PhanterPS2.lnk"
  RMDir "$APPDATA\phanterps2\linguagem"
  RMDir "$APPDATA\phanterps2"
  RMDir "$INSTDIR\imagens"
  RMDir "$INSTDIR\src"
  RMDir "$INSTDIR\Microsoft.VC90.CRT"
  RMDir "$INSTDIR"

  RMDir "$SMPROGRAMS\PhanterPS2"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PhanterPS2"
  DeleteRegKey /ifempty HKCU "Software\PhanterPS2"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\PhanterPS2.exe"
SectionEnd

;--------------------------------
;Uninstaller Functions

Function un.onInit

  !insertmacro MUI_UNGETLANGUAGE
  
FunctionEnd