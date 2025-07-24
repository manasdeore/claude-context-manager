# Project: Kinben Electronics Embedded Systems Repository

## Project ID
kinben-electronics-code-004

## Description
Comprehensive embedded systems codebase containing 6 industrial sensor measurement and data acquisition projects built on Teensy 4.1 and Raspberry Pi Pico platforms with professional documentation standards.

## Status
- **Current Status**: in_progress
- **Priority**: high
- **Created**: 2025-07-22 (tracking started)
- **Last Updated**: 2025-07-22

## Context
- **Claude Instance**: Desktop - Primary Windows PC
- **Working Directory**: C:\Users\manas\OneDrive - KINBEN INNOVATION PRIVATE LIMITED\Documents\Kinben Electronics Repo Folder\Code
- **GitHub Repo**: Multiple repositories under Kinben Electronics Team
- **Documentation Status**: 5 out of 6 projects have complete standardized wikis

## Progress Tracking

### Completed Tasks ✅
- [x] **5 Production-Ready Projects Completed** (83% overall completion)
- [x] **CSB Central Sync Board V1.0** - Teensy 4.1 data acquisition hub
- [x] **HUB Master Board V1.0** - RP2040 HUB control system
- [x] **HUB Slots Board V1.0** - 5-channel data acquisition with PSRAM
- [x] **INAV Inertial Navigation V1.0** - Teensy 4.1 navigation system
- [x] **ODO Odometer Board V1.0** - RP2040 odometer data logging
- [x] **Standardized Documentation** - 5 complete wiki deployments
- [x] **Shared Library Ecosystem** - Common components across projects
- [x] **Performance Optimization** - SD card and sensor timing optimized

### Current Task 🔄
**Sensor Head Test Jig Completion** (90% complete)
- 4 remaining wiki pages to be completed
- Final documentation and deployment preparation

### Next Tasks 📋
- [ ] **Complete Test Jig Documentation** - 4 remaining wiki pages
- [ ] **GitHub Wiki Deployment** - Deploy all completed wikis  
- [ ] **Production Testing** - Final validation of test jig system
- [ ] **Repository Organization** - Final code cleanup and structure
- [ ] **Performance Documentation** - Benchmark results compilation

## Technology Stack & Architecture

### Microcontroller Platforms
- **Teensy 4.1**: ARM Cortex-M7 @ 600MHz (CSB, INAV boards)
- **Raspberry Pi Pico**: RP2040 @ 133MHz (HUB, ODO, Test Jig)
- **Development Framework**: Arduino Framework with PlatformIO

### Communication Protocols
- **I2C**: Sensor and IO expander communication
- **SPI**: High-speed sensor data acquisition
- **UART/Serial**: Debug and data transfer (115200, 921600 baud)
- **LVDS**: High-speed differential communication  
- **EasyTransfer**: Structured data exchange protocol

### Key Libraries & Components
- **EasyTransfer**: Inter-board communication
- **SdFat**: High-performance SD card operations
- **Adafruit NeoPixel**: Status indication systems
- **LiquidCrystal_I2C**: Display interfaces
- **Custom Libraries**: High_Speed_ADC, IOEX, MFLSensorHead, Shift Register

## Individual Project Breakdown

### 1. CSB Central Sync Board V1.0 ✅ **COMPLETE**
**Platform**: Teensy 4.1 (ARM Cortex-M7 @ 600MHz)
**Purpose**: Central data acquisition and communication hub

**Key Features**:
- Multi-board communication (up to 4 communication boards)
- High-speed data logging (20MB/s write, ~23MB/s read)
- Ring buffer architecture (128MB file limits)
- Five operational states with hardware switch control
- I2C communication board detection with sequential addressing

### 2. HUB Master Board V1.0 ✅ **COMPLETE**
**Platform**: Raspberry Pi Pico (RP2040 @ 133MHz)
**Purpose**: HUB control and sensor management

**Key Features**:
- I2C master functionality for HUB communication
- Channel selection and triggering system
- ADC data acquisition (22μs read, 30μs broadcast)
- Mode detection and switching capability
- NeoPixel status indication

### 3. HUB Slots Board V1.0 ✅ **COMPLETE** 
**Platform**: Raspberry Pi Pico (RP2040 @ 133MHz)
**Purpose**: 5-channel data acquisition with PSRAM buffering

**Key Features**:
- Dual-core RP2040 architecture utilization
- 8MB PSRAM buffer (34-71μs performance range)
- EGP/MFL sensor support with configurable types
- SD card logging with SdFat library
- I2C slave communication (address 0x01)

### 4. INAV Inertial Navigation V1.0 ✅ **COMPLETE**
**Platform**: Teensy 4.1 (ARM Cortex-M7)
**Purpose**: Inertial navigation and sensor data processing

**Key Features**:
- Temperature monitoring (dual TMP461 sensors, 206μs read)
- RTC integration (fast time reading, 18μs)
- InertialSense SDK integration
- MTP (Media Transfer Protocol) support
- High-precision timing and navigation calculations

### 5. ODO Odometer Board V1.0 ✅ **COMPLETE**
**Platform**: Raspberry Pi Pico (RP2040 @ 133MHz)  
**Purpose**: Odometer sensor data acquisition and logging

**Key Features**:
- Dual-core RP2040 with 8MB PSRAM buffer
- 6 ODO sensors with LVDS communication (921600 baud)
- SD card logging (128MB file limits)
- EasyTransfer protocol implementation
- Power switching and sensor management

### 6. Sensor Head Test Jig 🔄 **IN PROGRESS** (90% complete)
**Platform**: Raspberry Pi Pico (RP2040 @ 133MHz)
**Purpose**: Automated sensor testing system

**Key Features**:
- LDC1101 and TMAG5170 sensor testing
- 4 test modes: SENSOR_TEST, MFL_TEST, EGP_TEST, EGP_STRING_TEST
- LCD interface (16x2, I2C 0x27) with 3-button control
- 2 NeoPixel status LEDs
- Shift register sensor selection
- Complete KiCad hardware design with 3D models

## Common Library Ecosystem

### High_Speed_ADC
- SPI-based ADC control with register-level access
- Optimized for high-speed data acquisition across projects

### IOEX (I/O Expander) 
- MyI2CDeviceKT class for I2C IO expander management
- Shared across multiple projects for GPIO expansion

### MFLSensorHead
- **LDC1101**: Inductive sensor driver with DMA support
- **TMAG5170**: Magnetic sensor driver  
- Shift register integration (LVC595) for sensor multiplexing

### Shift Register
- LVC595 shift register driver for output expansion
- Used in sensor selection and control systems

## Documentation Quality & Standards

### Current Achievement ⭐
**Professional embedded systems development practices**:
- Standardized project structure across all repositories
- Comprehensive documentation following `WIKI_STANDARDS.md`
- Performance testing and optimization results
- Modular design with shared libraries
- Hardware-software co-design with KiCad integration
- Version control and collaborative development

### Documentation Status
- **Completed**: 5 out of 6 standardized wikis (83%)
- **In Progress**: Sensor Head Test Jig (4 pages remaining)
- **Deployment**: INAV deployed to GitHub, 4 others pending

## Performance Metrics

### System Performance Achievements
- **CSB Data Logging**: 20MB/s write, 23MB/s read performance
- **HUB ADC Timing**: 22μs read time, 30μs broadcast time
- **PSRAM Buffer**: 34-71μs performance (160-304 bytes)
- **Temperature Sensor**: 206μs read time (dual TMP461)
- **RTC Operations**: 18μs fast time reading
- **LVDS Communication**: 921600 baud stable operation

## Commands to Remember
```bash
# PlatformIO Build
pio run -e teensy41
pio run -e rpipico

# Upload to Hardware  
pio run -e teensy41 --target upload
pio run -e rpipico --target upload

# Serial Monitor
pio device monitor --port COM3 --baud 115200

# Library Management
pio lib install "library-name"
```

## Issues & Current Status
- **Production Systems**: 5 out of 6 projects fully operational
- **Test Jig**: 90% complete, 4 wiki pages remaining
- **Documentation**: High-quality standards maintained
- **GitHub Deployment**: INAV deployed, others pending
- **Performance**: All optimization targets met

## Development Standards
- **Code Quality**: Professional embedded C++ practices
- **Documentation**: Comprehensive wiki system
- **Testing**: Hardware-in-the-loop validation
- **Version Control**: Git-based collaborative development
- **Modular Design**: Shared library ecosystem
- **Performance**: Timing-critical optimization completed

## Business Impact
- **Industrial Sensor Platform**: Complete measurement ecosystem
- **Production Readiness**: 83% of projects deployable
- **Standardization**: Consistent development practices
- **Scalability**: Modular architecture for expansion
- **Quality Assurance**: Comprehensive testing and documentation

## Files & Resources
- **Documentation**: `WIKI_CREATION_STATE.md`, `WIKI_STANDARDS.md`, `RESUME_PROMPT.md`
- **Project Folders**: 6 individual project directories with complete source
- **Shared Libraries**: Common components across projects
- **Hardware Integration**: KiCad designs with 3D models and fabrication files

---
*This represents a mature, production-quality embedded systems codebase demonstrating professional development practices and comprehensive industrial sensor platform capabilities.*

*Last updated by Claude instance: Desktop Primary on 2025-07-22*