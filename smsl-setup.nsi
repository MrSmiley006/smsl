!include LogicLib.nsh
!include nsDialogs.nsh
!include "winmessages.nsh"

!define env_hklm 'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
!define env_hkcu 'HKCU "Environment"'

Name "SmSL"
Icon "smsl_logo.ico"
UninstallIcon "smsl_logo.ico"

LicenseData LICENSE
InstallDir "$PROGRAMFILES64\SmSL"

RequestExecutionLEvel highest

Unicode True

Page license
Page directory
Page instfiles
Page custom nsDialogsPage nsDialogsPageEnd
UninstPage uninstConfirm
UninstPage instfiles

Var Dialog
Var Label_SMSL_H
Var Text_SMSL_H
Var Label_SMSL_STDLIB
Var Text_SMSL_STDLIB

Function .onInit
  Var /GLOBAL is_system
  MessageBox MB_YESNO "Chcete nainstalovat SmSL pro v¹echy u¾ivatele?" IDYES system IDNO user
  system:
    StrCpy $INSTDIR "$PROGRAMFILES64\SmSL"
    StrCpy $is_system "Yes"
  user:
    ${If} $is_system == "Yes"
     goto end
   ${EndIf}
    StrCpy $INSTDIR "$PROFILE\AppData\Roaming\SmSL"
    end:
FunctionEnd

Function nsDialogsPage
  nsDialogs::Create 1018
  Pop $Dialog

  ${If} $Dialog == error
    Abort
  ${EndIf}

  Var /GLOBAL path
  ${If} $is_system == 'Yes'
    StrCpy $path "$PROGRAMFILES64\SmSL"
  ${Else}
    StrCpy $path "$PROFILE\AppData\Roaming\SmSL"
  ${EndIf}
  
  ${NSD_CreateLabel} 0 0 100% 12u "SMSL_H"
  Pop $Label_SMSL_H
  ${NSD_CreateText} 0 13u 100% 10% "$path"
  Pop $Text_SMSL_H
  ${NSD_CreateLabel} 0 27u 100% 10% "SMSL_STDLIB"
  Pop $Label_SMSL_STDLIB
  ${NSD_CreateText} 0 41u 100% 10% "$path\stdlib"
  Pop $Text_SMSL_STDLIB
  nsDialogs::Show
FunctionEnd

Function nsDialogsPageEnd
  ${NSD_GetText} $Text_SMSL_H $0
  ${NSD_GetText} $Text_SMSL_STDLIB $1
  ${If} is_system == 'Yes'
    WriteRegExpandStr ${env_hklm} "SMSL_H" "$path"
    WriteRegExpandStr ${env_hklm} "SMSL_STDLIB" "$path\stdlib"
  ${Else}
    WriteRegExpandStr ${env_hkcu} "SMSL_H" "$path"
    WriteRegExpandStr ${env_hkcu} "SMSL_STDLIB" "$path\stdlib"
  ${EndIf}
  SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
FunctionEnd

section Installer
  EnVar::Check "NULL" "NULL"
  Pop $0
  ${If}  $0 > '0'
    Abort
  ${EndIf}
  EnVar::SetHKLM
  EnVar::Check "NULL" "NULL"
  Pop $0
  ${If} $0 > '0'
    StrCpy $INSTDIR "$PROFILE\AppData\Roaming\SmSL"
  ${EndIf}
  SetOutPath $INSTDIR
  File "smsl.exe"
  File "smsl.h"
  File /r "examples"
  File /r "stdlib"
  File "smsl_docs-cs.odt"
  File "smsl_docs-cs.pdf"
  File "LICENSE"
  WriteUninstaller $INSTDIR\unins000.exe
  EnVar::AddValue "path" $INSTDIR
SectionEnd

section "un.Uninstaller"
  Delete "smsl.exe"
  Delete "smsl.h"
  Delete "examples"
  Delete "stdlib"
  Delete "smsl_docs-cs.odt"
  Delete "smsl_docs-cs.pdf"
  Delete "LICENSE"
  ${If} is_system == "Yes"
    DeleteRegValue ${env_hklm} SMSL_H
    DeleteRegValue ${env_hklm} SMSL_STDLIB
  ${Else}
    DeleteRegValue ${env_hkcu} SMSL_H
    DeleteRegValue ${env_hkcu} SMSL_STDLIB
  ${EndIf}
  SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
SectionEnd
