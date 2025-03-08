# HoverBoard module for M5Stack's UIFlow

This repository contains the M5Stack's UIFlow v1 Micropython code blocks for driving a Hoverboard from an M5Stack controller using an UART port.

The hoverboard has to be running this firmware:

https://github.com/EFeru/hoverboard-firmware-hack-FOC

compiled with the VARIANT_USART: https://github.com/EFeru/hoverboard-firmware-hack-FOC?tab=readme-ov-file#example-variants

This micropython code is based on the code example: https://github.com/EFeru/hoverboard-firmware-hack-FOC/blob/main/Arduino/hoverserial/hoverserial.ino

TODO: Improve this readme.
TODO: Validate the feedback using the checksum (currently it accepts all the feedback).
