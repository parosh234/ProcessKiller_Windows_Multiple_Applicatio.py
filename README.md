# ProcessKiller_Windows_Multiple_Application

Requires psutil:

•	Install if not already installed:

pip install psutil

Smaple Output:

🔍 Trying to terminate: WhatsApp

✅ Window handle obtained for 'WhatsApp'.

✅ Process ID for 'WhatsApp': 3668

✅ Successfully obtained process handle for 'WhatsApp'.

✅ 'WhatsApp' terminated successfully.

🔍 Trying to terminate: Microsoft Edge

⚠️ Could not find window 'Microsoft Edge'. Trying process name instead...

🔍 Trying to terminate process: msedge.exe

✅ Process 'msedge.exe' (PID: 4776) terminated successfully.

🔍 Trying to terminate: File Explorer

⚠️ Could not find window 'File Explorer'. Trying process name instead...

🔍 Trying to terminate process: explorer.exe

✅ Process 'explorer.exe' (PID: 2624) terminated successfully.

🔍 Trying to terminate: Internet Explorer

⚠️ Could not find window 'Internet Explorer'. Trying process name instead...

🔍 Trying to terminate process: iexplore.exe

✅ Process 'iexplore.exe' (PID: 4120) terminated successfully.

✅ Process 'iexplore.exe' (PID: 5680) terminated successfully.



