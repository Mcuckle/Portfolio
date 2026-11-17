### Overview
This project engineered and deployed a scalable environmental telemetry and Internet of Things (IoT) data subsystem for a 1:8 scale spacecraft habitat module. By integrating multi-sensor hardware suites with a Raspberry Pi host using I2C and SPI communication protocols, the system successfully bridges local crewed situational awareness via custom OLED dashboards with remote cloud-based data logging.

### Engineering Problem & Requirements
Reliable data handling and environmental monitoring are paramount in crewed spaceflight to ensure crew safety and mission success. The NEXUS habitat module required a robust onboard telemetry architecture capable of simultaneously tracking temperature, humidity, pressure, tri-axial magnetic fields, and acceleration without sensor offset or packet loss.

### Approach & Architecture
* **Hardware Selection & Integration:** Evaluated and integrated a Raspberry Pi 4B host with Adafruit sensor suites utilizing robust JST Qwiic connectors.
* **Protocol Distribution:** Implemented tiered data handling by combining half-duplex I2C for sensor acquisition with high-speed full-duplex SPI across dedicated chip-select lines to drive multiple Waveshare 1.3-inch OLED displays.
* **IoT Data Pipeline:** Developed automated Python logging scripts managed via systemd to record continuous CSV data locally while simultaneously mirroring live metrics to the ThingSpeak cloud platform.

### Results & Validation
* **Continuous Acquisition:** Achieved stable, continuous multi-sensor logging at a 0.5 Hz sampling cadence over 24-hour periods without packet loss.
* **Real-Time Display & Cloud Sync:** Successfully drove a 3D-printed physical OLED dashboard array with negligible latency while maintaining synchronized remote tracking via ThingSpeak IoT dashboards.