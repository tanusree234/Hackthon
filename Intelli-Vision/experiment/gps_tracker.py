import serial
import time
import string
import pynmea2
from http.server import BaseHTTPRequestHandler, HTTPServer


class GPSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse GPS data
        newdata = self.ser.readline()
        if newdata[0:6] == b"$GPRMC":
            newmsg = pynmea2.parse(newdata.decode("utf-8"))
            lat = newmsg.latitude
            lng = newmsg.longitude

            # Update marker on the map
            update_command = "window.updateMarker({}, {});".format(lat, lng)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(update_command, "utf-8"))


if __name__ == "__main__":
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    # Start the HTTP server
    handler = GPSHandler
    handler.ser = ser
    httpd = HTTPServer(("localhost", 8000), handler)
    print("Server running on port 8000...")
    httpd.serve_forever()
