import os
import shutil
import cv2
from pypylon import pylon

class BaslerCamera:
    def __init__(self):
        self.output_dir = 'output'
        self.camera = None
        self.image_counter = 1
        self.initialize_camera()
        self.create_output_directory()

    def initialize_camera(self):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.Width=1600
        self.camera.Height=1600
        self.camera.ExposureTime.SetValue(40000)
        self.camera.PixelFormat.SetValue('BGR8')
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def create_output_directory(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)  # Delete the folder and its contents recursively
        os.makedirs(self.output_dir)

    def acquire_images(self):
        while True:
            grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            image_data = grab_result.GetArray()
            image_file = os.path.join(self.output_dir, f'{self.image_counter:02d}.jpg')
            cv2.imwrite(image_file, image_data)
            grab_result.Release()
            self.image_counter += 1
            if self.image_counter > 12:
                self.image_counter = 1

    def stop_image_acquisition(self):
        self.camera.StopGrabbing()

    def close_camera(self):
        self.camera.Close()

    def __del__(self):
        self.stop_image_acquisition()
        self.close_camera()
