# Barcode

![Current Version](https://img.shields.io/badge/version-v1-blue)
![Language](https://img.shields.io/badge/Language-Python-purple)
![GitHub contributors](https://img.shields.io/github/contributors/charnim/barcode)
![GitHub stars](https://img.shields.io/github/stars/charnim/barcode?style=social)
![GitHub forks](https://img.shields.io/github/forks/charnim/barcode?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/charnim5?style=social)

```
						.______        ___      .______        ______   ______    _______   _______ 
						|   _  \      /   \     |   _  \      /      | /  __  \  |       \ |   ____|
						|  |_)  |    /  ^  \    |  |_)  |    |  ,----'|  |  |  | |  .--.  ||  |__   
						|   _  <    /  /_\  \   |      /     |  |     |  |  |  | |  |  |  ||   __|  
						|  |_)  |  /  _____  \  |  |\  \----.|  `----.|  `--'  | |  '--'  ||  |____ 
						|______/  /__/     \__\ | _| `._____| \______| \______/  |_______/ |_______|
```                                                                         

An IP reverse lookup script that accepts IP ranges and resolves them and their adjacent addresses to hostnames(PTR)<br>
and then greps all the hostnames to detect additional IP addresses that may belong to the company.

## Table of Contents
- [Getting Started](#getting-started)
	- [Tools Required](#tools-required)
	- [Installation](#installation)
- [Usage](#Usage)
- [Authors](#authors)
- [License](#License)

## Getting Started

### Tools Required

* python3

### Installation

All installation steps go here.

* git clone https://github.com/charnim/Barcode.git
* cd Barcode
* python3 barcode.py

## Running the App

* Example steps:
  ```
    python3 barcode.py -l 200 -d search_keywords.txt -i ipv4_ranges.txt
  ```


Where: 

-l is how much ip's to look forward and backwards<br>
-d is a keyword file containing all keywords the script will look for in the resolved name. <br>
Example: Clientname com, clientname,clientname.org etc. <br>
-i is the IP list to scan. Can be in each of the following formats, multiline supported:

1.1.1.1<br>
1.1.1.1/28<br>
1.1.1.1-1.1.1.100

## Authors

#### @charnim
* [GitHub]
* [LinkedIn]

You can also see the complete [list of contributors][contributors] who participated in this project.

## License

`Barcode` is open source software [licensed as MIT][license].

[//]: # (HyperLinks)

[GitHub Repository]: https://github.com/charnim/barcode
[GitHub Pages]: https://madhur-taneja.github.io/README-Template
[CONTRIBUTING.md]: https://github.com/charnim/barcode/blob/master/CONTRIBUTING.md
[tags]: https://github.com/charnim/barcode/tags

[GitHub]: https://github.com/charnim
[LinkedIn]: https://www.linkedin.com/in/charnim/

[contributors]: https://github.com/charnim/barcode/contributors
[license]: https://github.com/charnim/barcode/blob/master/LICENSE.md
