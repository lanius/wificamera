What is this?
=============
WifiCamera is a Python module for controlling the network camera CS-W07G-CY. About the device, see http://www.planex.co.jp/product/camera/cs-w07g-cy/.


Getting started
===============
WifiCamera can be installed with pip or easy_install::

    pip install wificamera

Create WifiCamera object, and you can take and save a snapshot::

    from wificamera import WifiCamera
    camera = WifiCamera(host='192.168.111.200')
    data = camera.snapshot()
    with open('snapshot.jpg', 'wb') as f:
        f.write(data)

You can get/set some kinds of parameters for the camera::

    print(camera.resolution)        # 'VGA'
    camera.resolution = 'QQVGA'     # set resolution 'QQVGA'
    
    print(camera.compression)       # 'standard'
    camera.compression = 'high'     # set compression 'high'
    
    print(camera.brightness)        # 4
    camera.brightness = 7           # set brightness 7
    
    print(camera.contrast)          # 2
    camera.contrast = 4             # set contrast 4

To load a snapshot as a PIL object, use StringIO module::

    from cStringIO import StringIO 
    import Image
    data = camera.snapshot()
    img = Image.open(StringIO(data))
    img.save('snapshot.jpg')

To use streaming, define callback and call 'stream' method::

    count = 0
    
    def on_data(data):  # callback
        global count
        with open('streaming.jpg', 'wb') as f:
            f.write(data)
        count += 1
    
    def is_continue():  # stop condition
        global count
        if count < 100:
            return True
        else:
            return False

    camera.stream(on_data, is_continue)


License
=======
WifiCamera is licensed under the MIT Licence. See LICENSE for more details.
