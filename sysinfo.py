import os
import platform
import getpass

print("=== Basic System Info ===")

print(f"OS Name & Kernel: {platform.system()} {platform.release()} - {platform.version()}")

print(f"Current User: {getpass.getuser()}")

print(f"Current Directory: {os.getcwd()}")
