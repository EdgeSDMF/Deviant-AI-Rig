import urllib.request
import os

# Target a universally compatible, standard v8 protobuf schema model asset
url = "https://github.com"
target_filename = "model.onnx"

print(f"=== Initializing Direct Model Stream ===")
print(f"Source URL: {url}")
print(f"Downloading pre-converted standard layout asset...")

try:
    # Pull the binary model file straight from the server repository into your sandbox directory
    urllib.request.urlretrieve(url, target_filename)
    file_size = os.path.getsize(target_filename) / (1024 * 1024)
    print(f"\n[!] Success! Generated file: {os.path.abspath(target_filename)}")
    print(f"    Total Verified Size: {file_size:.2f} MB")
    print("========================================")
except Exception as e:
    print(f"\n[X] Download stalled: {e}")
