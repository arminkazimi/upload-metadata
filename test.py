import subprocess

file_path = r'D:\Documents\imp\Morphotect\tecto-metadata-api\8e7102ed-2970-47ce-ad25-896696df5c3e.json'
result = subprocess.run([".venv\\Scripts\\python.exe", "sendFile.py", file_path], capture_output=True, text=True, shell=True)
# print(result.stdout)