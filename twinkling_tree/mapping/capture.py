import sys
import time

import picamera


def log(message):
    print(message, file=sys.stderr, flush=True)


def setup(camera):
    """
    Fix settings so that image sequence has consistent gain etc.
    """
    log("Setup started")
    camera.resolution = (1280, 720)
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    log("Setup complete")


def capture_loop(camera, filepaths):
    """
    Consume an iterable of filepaths, capturing an image for each.
    """
    print("Enter filepaths one line at a time. Use Ctrl+D to finish.", flush=True)
    for filepath in filepaths:
        camera.capture(filepath)
        print(f"Captured {filepath}", flush=True)


def main():
    """
    Read filepaths from the stdin and save an image for each.
    """
    with picamera.PiCamera() as camera:
        setup(camera)
        filepaths = (line.rstrip("\n") for line in sys.stdin)
        capture_loop(camera, filepaths)
    log("Received EOF. Exiting.")


if __name__ == "__main__":
    main()
