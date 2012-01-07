# -*- coding: utf-8 -*-
"""
    wificamera.wificamera
    ~~~~~~~~~~~~~~~~~~~~~

    WifiCamera class can be used to controll the network camera CS-W07G-CY.

    :copyright: (c) 2012 lanius
    :license: MIT, see LICENSE for more details.
"""

from urllib import urlencode
from urllib2 import urlopen
from time import sleep


class WifiCamera(object):
    RESOLUTION = ['VGA', 'QVGA', 'QQVGA']
    COMPRESSION_MODE = ['standard', 'high']

    def __init__(self, host='192.168.111.200', timeout=15):
        self.url_root = ''.join(['http://', host, '/'])
        self.timeout = timeout
        self._resolution = None
        self._compression = None
        self._brightness = None
        self._contrast = None

    @property
    def resolution(self):
        return None

    @resolution.setter
    def resolution(self, value):
        if self._resolution == value:
            return
        self._set_resolution(value)
        self._resolution = value

    @resolution.getter
    def resolution(self):
        if self._resolution is None:
            self._resolution = self._get_resolution()
        return self._resolution

    @property
    def compression(self):
        return None

    @compression.setter
    def compression(self, value):
        if self._compression == value:
            return
        self._set_compression(value)
        self._compression = value

    @compression.getter
    def compression(self):
        if self._compression is None:
            self._compression = self._get_compression()
        return self._compression

    @property
    def brightness(self):
        return None

    @brightness.setter
    def brightness(self, value):
        if self._brightness == value:
            return
        self._set_brightness(value)
        self._brightness = value

    @brightness.getter
    def brightness(self):
        if self._brightness is None:
            self._brightness = self._get_brightness()
        return self._brightness

    @property
    def contrast(self):
        return None

    @contrast.setter
    def contrast(self, value):
        if self._contrast == value:
            return
        self._set_contrast(value)
        self._contrast = value

    @contrast.getter
    def contrast(self):
        if self._contrast is None:
            self._contrast = self._get_contrast()
        return self._contrast

    def snapshot(self):
        return self._get({'action': 'snapshot'})

    def stream(self, on_data, is_continued=None, interval=0):
        if not is_continued:
            is_continued = lambda: True  # forever
        r = self._open({'action': 'stream'})
        count = 0
        while is_continued():
            line = r.readline()
            if 'Content-Length' in line:
                count = int(line.split(':')[1].strip())
            if count and len(line.strip()) == 0:
                on_data(r.read(count))
                count = 0
                sleep(interval)

    def _set_resolution(self, _resolution):
        resolution = _resolution.upper()
        if resolution not in self.RESOLUTION:
            raise WifiCameraError("specification is not supported.")
        if resolution == self.RESOLUTION[0]:  # VGA
            command = 'VGA640_480'
        elif resolution == self.RESOLUTION[1]:  # QVGA
            command = 'QVGA320_240'
        elif resolution == self.RESOLUTION[2]:  # QQVGA
            command = 'QQVGA160_120'
        self._command(command)

    def _set_compression(self, _mode):
        mode = _mode.lower()
        if mode not in self.COMPRESSION_MODE:
            raise WifiCameraError("specification is not supported.")
        if mode == self.COMPRESSION_MODE[0]:  # 'standard'
            command = 'standard_compress'
        elif mode == self.COMPRESSION_MODE[1]:  # 'high'
            command = 'high_compress'
        self._command(command)

    def _set_brightness(self, brightness):
        if not 0 <= brightness <= 8:
            raise WifiCameraError("value must be specified between 0 and 8.")
        diff = brightness - self._brightness
        if diff > 0:
            [self._up_brightness() for _ in xrange(diff)]
        elif diff < 0:
            [self._down_brightness() for _ in xrange(abs(diff))]

    def _set_contrast(self, contrast):
        if not 0 <= contrast <= 8:
            raise WifiCameraError("value must be specified between 0 and 8.")
        diff = contrast - self._contrast
        if diff > 0:
            [self._up_contrast() for _ in xrange(diff)]
        elif diff < 0:
            [self._down_contrast() for _ in xrange(abs(diff))]

    def _up_brightness(self):
        self._command('brightness_plus')

    def _down_brightness(self):
        self._command('brightness_minus')

    def _up_contrast(self):
        self._command('contrast_plus')

    def _down_contrast(self):
        self._command('contrast_minus')

    def _get_resolution(self):
        value = self._export_value(self._command('value_resolution'))
        return self.RESOLUTION[value]

    def _get_compression(self):
        value = self._export_value(self._command('value_compression'))
        return self.COMPRESSION_MODE[value]

    def _get_brightness(self):
        return self._export_value(self._command('value_brightness'))

    def _get_contrast(self):
        return self._export_value(self._command('value_contract'))

    def _command(self, command):
        return self._get({'action': 'command', 'command': command})

    def _get(self, params):
        return self._open(params).read()

    def _open(self, params):
        try:
            r = urlopen('?'.join([self.url_root, urlencode(params)]),
                        timeout=self.timeout)
        except IOError:
            raise WifiCameraError("device is not found.")
        return r

    def _export_value(self, line):
        return int(line.split(':')[1].strip())


class WifiCameraError(Exception):
    pass
