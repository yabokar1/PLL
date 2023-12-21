import sys
import os

print("Current working directory:", os.getcwd())
sys.path.append(os.getcwd())
print("Updated sys.path:", sys.path)