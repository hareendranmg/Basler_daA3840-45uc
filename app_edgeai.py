#!/usr/bin/python3
#  Copyright (C) 2021 Texas Instruments Incorporated - http://www.ti.com/
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#
#    Neither the name of Texas Instruments Incorporated nor the names of
#    its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import threading
import yaml

from edge_ai_class import EdgeAIDemo
from basler_camera import BaslerCamera
import utils


def grab_images_in_thread(camera_image_grabber):
    camera_image_grabber.acquire_images()

def main(sys_argv):
    args = utils.get_cmdline_args(sys_argv)

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    try:
        camera_image_grabber = BaslerCamera()
        grab_thread = threading.Thread(target=grab_images_in_thread, args=(camera_image_grabber,))
        grab_thread.start()
        demo = EdgeAIDemo(config)
        demo.start()

        if args.verbose:
            utils.print_stdout = True

        if not args.no_curses:
            utils.enable_curses_reports(demo.title)

        demo.wait_for_exit()
    except KeyboardInterrupt:
        demo.stop()
        camera_image_grabber.stop_image_acquisition()
        camera_image_grabber.close_camera()
    finally:
        pass

    utils.disable_curses_reports()

    del demo
    del camera_image_grabber


if __name__ == "__main__":
    main(sys.argv)