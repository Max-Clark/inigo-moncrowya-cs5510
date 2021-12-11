import object_detection
from detect_person import analyze_images


object_detection.run_detection()
print(f"IS A PERSON FOUND: {analyze_images()}")
