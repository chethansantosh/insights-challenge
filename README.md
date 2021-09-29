# insights-challenge

## Problem Statement

#### Given the folder structure of image frames captured by a camera:
```
/node
    /images
		/frames
			/farm-xxx
				/camera-1
					/images
						/2020-11-02
							/00  (hour)
								farm-xxx_barn-3_camera-1_2020-11-02T00h00m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T00h01m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T00h02m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T00h03m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T00h04m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T00h05m00s+0000.png
							/01
								farm-xxx_barn-3_camera-1_2020-11-02T01h00m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T01h01m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T01h02m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T01h03m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T01h04m00s+0000.png
								farm-xxx_barn-3_camera-1_2020-11-02T01h05m00s+0000.png
							...
							...
							/23
```
Create a class that receives **path** at the initialization
* Create a method that returns the date range available on the **path**
* Create a method that receives {timezone_tz} as parameter and
   returns a list of dict that aggregates the <Absolute path>/files by timezone-aware date in which the UTC file belongs (per camera)

@return:
```
[
   {
      "date_tz" str: "2020-10-31",
      "files" list: [
        "absolute_file_path"
      ]
   },
]
```

### Prerequisites
  * Python installed (Tested on version 3.9)
  * Below Python Libraries installed
    * pip
    * mock
    * pytz
    * setuptools 
     

### Assumptions
  * Image file types - **.png** and **.jpg**
  * Image file name starts with **farm-xxx**
  * Timezone input is given as per **pytz** timezone list
  

## Usage

```
python run.py -h
usage: run.py [-h] -p PATH -o OPERATION [-t TIMEZONE] [-l LOGFILEPATH]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Absolute directory path containing Camera image files
  -o OPERATION, --operation OPERATION
                        Operation to perform - Choices 1 or 2 1.Return Date
                        Range of image files present in the path 2.Return List
                        of Dict with files by timezone-aware date
  -t TIMEZONE, --timeZone TIMEZONE
                        Timezone to list the files.
  -l LOGFILEPATH, --logFilePath LOGFILEPATH
                        File path to Log the information. Default it logs in
                        current working directory

```
  
```
python run.py -p '/input' -o 1
2021-09-29 12:17:13,698 [INFO]: File names in the path /input are of date range - 
2021-09-29 12:17:13,730 [INFO]: Date Range: 20201102000000 - 20201104230500
```
  
```
python run.py -p 'parent' -o 2 -t 'Pacific/Enderbury'
2021-09-29 12:19:27,082 [INFO]: List of Dictionaries with files by timezone Pacific/Enderbury aware date
2021-09-29 12:19:27,107 [INFO]: [
    {
        "date_tz": "2020-09-02", 
        "files": [
            "parent/child3/farm-xxx_barn-3_camera-1_2020-09-02T00h00m00s+0000.png"
        ]
    }, 
    {
        "date_tz": "2020-11-02", 
        "files": [
            "parent/child1/farm-xxx_barn-3_camera-1_2020-11-02T00h00m00s+0000.png"
        ]
    }, 
    {
        "date_tz": "2020-12-02", 
        "files": [
            "parent/child2/farm-xxx_barn-3_camera-1_2020-12-02T00h00m00s+0000.png"
        ]
    }
]

```
