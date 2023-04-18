import os
import shutil
import cv2
from pypylon import pylon

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.Open()
camera.Width=2100
camera.Height=2100
camera.ExposureTime.SetValue(40000)
camera.Gain.SetValue(0)
# camera.PixelFormat.SetValue('BGR8')

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

output_dir = 'output'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)  # Delete the folder and its contents recursively

os.makedirs(output_dir)

image_counter = 1

while True:
    grab_result = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
    image_data = grab_result.GetArray()
    image_file = os.path.join(output_dir, f"{image_counter:02d}.jpg")
    cv2.imwrite(image_file, image_data)
    grab_result.Release()

    image_counter += 1
    if image_counter > 12:
        image_counter = 1

# camera.StopGrabbing()
# camera.Close()
