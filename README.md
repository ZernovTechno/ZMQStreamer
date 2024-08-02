[README НА РУССКОМ](./READMERUS.md)
# ZMQStreamer
## Managed by [Zernov](https://www.youtube.com/@zernovtech)

## About
Hey! This is my software used to broadcast the screen via the ZeroMQ protocol. The code runs in Python, and takes a screenshot every N times (As fast as possible) and then sends it through ZMQ, Base64 encoding the string.

## How it works?
Simple. For using on a Windows/in a "Release mode" you can just run .exe files. There are three different resolutions:

```
ServerHighRes.exe - screen resolution.
ServerMedRes.exe - 1024x600 (16:9)
ServerLowRes.exe - 640x360 (16:9)
```

If your screen 21:9 or something else - it just resize it, and compress.

## Basicly it working with my [Unity AR app for Android](https://github.com/ZernovTechno/AR)
