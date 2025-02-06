import ctypes  # For interacting with Windows API
import sys     # For graceful program exit
import psutil  # For managing system processes (install using: pip install psutil)

# Load Windows API libraries
k_handle = ctypes.WinDLL("Kernel32.dll")  # Kernel32.dll for process management
u_handle = ctypes.WinDLL("User32.dll")    # User32.dll for window handling

# Process access rights (provides full control over the process)
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0x0FFF)

# List of applications to terminate (update window titles or process names)
apps_to_kill = [
    {"name": "WhatsApp", "process_name": "WhatsApp.exe"},
    {"name": "Microsoft Edge", "process_name": "msedge.exe"},
    {"name": "File Explorer", "process_name": "explorer.exe"},
    {"name": "Internet Explorer", "process_name": "iexplore.exe"},  # Added Internet Explorer
]

def terminate_by_window(window_title):
    """Terminate process using the window title (for apps with GUI)."""
    print(f"\n🔍 Trying to terminate: {window_title}")

    # Convert window title to bytes
    window_name = ctypes.c_char_p(window_title.encode('utf-8'))

    # Step 1: Find the window handle (HWND)
    hWnd = u_handle.FindWindowA(None, window_name)
    if hWnd == 0:
        print(f"⚠️ Could not find window '{window_title}'. Trying process name instead...")
        return False  # Try terminating by process name
    else:
        print(f"✅ Window handle obtained for '{window_title}'.")

    # Step 2: Get the Process ID (PID)
    lpdwProcessId = ctypes.c_ulong()
    response = u_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

    if response == 0:
        print(f"❌ Error: Could not retrieve process ID for '{window_title}'. Error Code: {k_handle.GetLastError()}")
        return False

    print(f"✅ Process ID for '{window_title}': {lpdwProcessId.value}")

    # Step 3: Open the process with full access
    hProcess = k_handle.OpenProcess(PROCESS_ALL_ACCESS, False, lpdwProcessId.value)
    if not hProcess:
        print(f"❌ Error: Could not open process for '{window_title}'. Error Code: {k_handle.GetLastError()}")
        return False

    print(f"✅ Successfully obtained process handle for '{window_title}'.")

    # Step 4: Terminate the process
    terminate_response = k_handle.TerminateProcess(hProcess, 0x1)

    if not terminate_response:
        print(f"❌ Error: Could not terminate '{window_title}'. Error Code: {k_handle.GetLastError()}")
    else:
        print(f"✅ '{window_title}' terminated successfully.")

    # Step 5: Close the process handle
    k_handle.CloseHandle(hProcess)
    return True


def terminate_by_process_name(process_name):
    """Terminate process directly by its process name (for background apps)."""
    print(f"🔍 Trying to terminate process: {process_name}")
    terminated_any = False

    # Loop through all running processes
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == process_name.lower():
            try:
                process.terminate()  # Attempt to terminate the process
                process.wait(timeout=5)  # Wait to confirm it's terminated
                print(f"✅ Process '{process_name}' (PID: {process.info['pid']}) terminated successfully.")
                terminated_any = True
            except Exception as e:
                print(f"❌ Error terminating '{process_name}' (PID: {process.info['pid']}): {e}")

    if not terminated_any:
        print(f"⚠️ No active processes found for '{process_name}'.")

    return terminated_any


# Loop through each application and attempt to terminate
for app in apps_to_kill:
    if not terminate_by_window(app['name']):
        terminate_by_process_name(app['process_name'])
