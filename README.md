graphite-schema-util
====================
This utility prints storage-schema and aggregation settings matching a given metric name by using carbon methods and configuration directly. This ensures results equal to the carbon behavior and should help debugging metric resolution issues.

## Installation:

This is a pybuilder project. You will need to install pybuilder by:
```bash
pip install pybuilder
```

### Verify project (unittests and coverage)
```bash
pyb verify
```

### Install project dependencies
```bash
pyb install_dependencies
```

### Build project
```bash
pyb publish
```


## usage

There is a default configuration assuming the following paths:
- CARBON_CONF_DIR: /etc/carbon
- CARBON_LIB_DIR: /opt/graphite/lib

### simply print schema info for given metric name
```bash
user@graphite-host ~ $ whisper-schema-info gis.devgis30.icinga.ntp_time.offset
STORAGE CONFIG:
(Using first matching pattern: ^\w{3}\.\w+\.icinga\.)
Archive 0: Seconds per point: 300, Datapoints to save: 2016
Archive 1: Seconds per point: 900, Datapoints to save: 5760
Archive 2: Seconds per point: 3600, Datapoints to save: 8760

AGGREGATION CONFIG:
(Using first matching pattern: .*)
xFilesFactor: 0.3
Aggregation method: average
```

### print detailed usage info
```bash
whisper-schema-info --help
```

### overwrite configuration
```bash
whisper-schema-info --carbonconfdir /opt/graphite/conf --carbonlibdir /opt/graphite/lib <metric name>
```
