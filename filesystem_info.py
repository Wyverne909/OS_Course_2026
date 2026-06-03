import os
import stat

def analyze_directory(directory_path):
    print(f"\n=== Analyzing Directory: {directory_path} ===")
    
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print("Error: Invalid directory path.")
        return

    try:
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)

            if os.path.isfile(filepath):
                file_stats = os.stat(filepath)
                
                file_size = file_stats.st_size
                
                file_permissions = stat.filemode(file_stats.st_mode)

                print(f"File: {filename}")
                print(f"  -> Size: {file_size} bytes")
                print(f"  -> Permissions: {file_permissions}")
                print("-" * 30)
                
    except PermissionError:
        print("Error: You do not have permission to read this directory.")

if __name__ == "__main__":
    target_dir = input("Enter a directory path (press Enter for current directory '.'): ")
    if not target_dir:
        target_dir = "."
        
    analyze_directory(target_dir)
