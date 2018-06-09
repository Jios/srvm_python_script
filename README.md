### Introduction
This is a python script that sends a GET request with [parameters](required-environment-variables) to the SRVM API.  If success, it will return 0, otherwise -1.

### Run Command
Run the srvm.py script under srvm/ path
```shell
python srvm/srvm.py
# with a properties file input argument
python srvm/srvm.py 'env1.properties'
# with multiple properties files input argument
python srvm/srvm.py 'env1.properties,env2.properties'
```

### Properties File (optional)
Environment varialbes used in the script can be stored in one or multiple properties files.  
For the current stage, the script only supports the following syntax:
```
ENV_VARIABLE_NAME=VALUE
```

### Git Branches
The following git branches are supported:
```
master
release
release/branch_name
```

### Required Environment Variables <a id="required-environment-variables"></a>
```
# git info
GIT_BRANCH=master

# SRVM info
SRVM_CUSTOMER_IDS=5000,5001
SRVM_RELEASE_FOR=pm
SRVM_RELEASE_BY=jian_li
SRVM_PRODUCT_CATALOG=kalay cam

# build info
BUILD_PLATFORM=ios

BUILD_OUTPUT_FILENAME=vsaas.ipa
BUILD_OUTPUT_PATH=output
or
OUTPUT_FILE_PATH=output/vsaas.ipa
```

### Optional Environment Variables
```
# force release if true
RELEASE_TO_SRVM=true or false

# deadline: YYYY-mm-DD
SRVM_DEADLINE=2016-08-05

# notes
RD_NOTES=

# build info
BUILD_VERSION=1.0.0
BUILD_BUNDLE_ID=com.tutk.vsaas 	# for iOS
BUILD_SUMMARY=

# SDK info
SDK_IOTC_VERSION=
SDK_AV_VERSION=
SDK_RDT_VERSION=
SDK_TUNNEL_VERSION=
```

### SRVM API @alvin
```
https://srvm.tutk.com/ci/?[params1=value1]&[params2=value2]&.......[paramsX=valueX]

* is required

KEY				  | ENV
------------------+--------------------------------------------------------------------
release_for 	  | SRVM_RELEASE_FOR 		* required
release_by		  | SRVM_RELEASE_BY  		* required
product_catalog	  | SRVM_PRODUCT_CATALOG    * required
platform		  | BUILD_PLATFORM          * required

program_file	  | OUTPUT_FILE_PATH or (BUILD_OUTPUT_PATH and BUILD_OUTPUT_FILENAME) * required

app_version		  | BUILD_VERSION		# app version    * or
sdk_version 	  | BUILD_VERSION		# sdk version    * or
server_version    | BUILD_VERSION		# server version * required

customer_ids	  | SRVM_CUSTOMER_IDS
generic			  | IS_FOR_GENERIC_VERSION

summary			  | BUILD_SUMMARY
rd_notes		  | RD_NOTES

# app
api_IOTC 		  | SDK_IOTC_VERSION
api_AV 			  | SDK_AV_VERSION
api_RDT 		  | SDK_RDT_VERSION
api_Tunnel 		  | SDK_TUNNEL_VERSION

# iOS
bundle-identifier | BUILD_BUNDLE_ID
bundle-version	  | BUILD_VERSION


SRVM_RELEASE_FOR (support lower case):
	- RD
	- QA
	- PM
	- Sales
	- FAE
	- Customer (PM, Sales, FAE)


SRVM_PRODUCT_CATALOG (support lower case):
# App
	- P2PDVRLive
	- Kalay Box
	- PCX Inside
	- P2PPlug
	- Kalay Home
	- P2PCamLive
	- P2PCamCEO
	- Kalay Cam
	- VSaaS
	- DoorPhone
	- DVR/NVR
	- Kalay Car
	- Test Tools

# SDK
	- IOTC Release Package
	- IOTC RC Package
	- IOTC New SOC Support
	- IOTC Test Build
	- Partial Source Code
	- Kalay Box
	- UI Material
	- IOTC New SOC Customization
	- PCX Inside
	- Firmware
	- Alcatel
	- KPNS
	- MQTT SDK

# server
	- P2P
	- Master
	- TPNS
	- Command Server
	- Watchdog
	- Athena
	- VSaaS
	- SPI

```
