# Instructions
*Detailed step by step instructions and a video tutorial are coming soon.*

I will be writing more detailed instructions as I develop this project. Below is a brief overview on how you can build an OSCA machine.

<!-- 
### Parts
| Name        | Price | Link |
| ----------- | ----- ------ | ----------- |
| Pyramid APEX 7000       | $200       |  |
| Paragraph   | Text        |  |

### Tools
| Name        | Price | Link |
| ----------- | ----------- | ----------- |
| Pyramid APEX 7000       | $200       |  |
| Paragraph   | Text        |  | -->


### Phase 1
I recommend that you build OSCA using the same three phase approach I developed it. First buy the electronics and test the software, second build the cast and pour the concrete, finally mount the electronics and paint.

#### Arduino and Bill Acceptor
First load the provided Arduino sketch onto the Arduino nano. Connect the button  and the Apex 7000 bill acceptor as shown in the provided schematic.

Using the Arduino IDE serial monitor test that the Arduino is outputting the expected strings. Insert a bill into the bill acceptor and you should see the dollar amount display on the serial monitor. When you press the button the serial monitor should display the string “RESET”

![Arduino IDE serial monitor](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/arduino-ide-serial-monitor.jpeg?raw=true)

#### Pi
Run the provided bash commands provided in [App.md](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/software/app/App.md) to set up your Pi and make the python script auto-run.

#### Printer/CUPS
Install cups and install the provided rollo Linux driver. Do a test print using the CLI and an example 4x6 label pdf to confirm that the printer is correctly set-up.
`lp -h localhost:631 ~/test.pdf`

#### Cellular Router
Insert a sim into the cellular router and connect the LAN 2 port to the raspberry Pi’s Ethernet port. Confirm that you have a internet connection by visiting a website using the pi’s browser.


![Cellular router and Pi](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/cellular-router.jpg?raw=true)

*I will be addressing the need for a 4G device in a upcoming project*

#### Battery
Connect all of the electronics to the battery and test that the system can power up, connect to the internet, boot the python GUI and it can successfully make a transaction.

### Phase 2
Go to your local hardware store and buy 3/4 lined 8x4 wood sheets. Have the store cut the wood as shown in the [provided designs](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/instructions/case.png). 

![Harware Store](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/hardware-store.jpeg?raw=true)

Using a 3D printer print the casting parts for the machine. Use a hot glue gun to stick the molds to the internal side of the UI face.

![3D Printed Molds](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/molds.jpg?raw=true)

Screw the wood together to form the outer cast. 

![Outer Cast](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/outer-cast.jpg?raw=true)


Screw the interior mold together and glue on the polystyrene foam insert.

![Interior Mold](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/interior-mold.jpg?raw=true)

Mix the concrete, start by packing the concrete into the small areas between the 3d printed molds. Wait an hour for the UI face to begin to set then lay the concrete for the front face.

![First Concrete](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/laying-concrete.jpg?raw=true)

Finally insert the interior mold into the exterior mold and fill the remainiung space with concrtete. Wait 24 hours for the cast to dry.


![Cast Final](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/cast-final.jpg?raw=true)

### Phase 3
Finally paint and mount the optional LED strips. Place the electronics inside the case. Power up the ATM and lock the door, Do a test run.

Congratulations you have build a Open-Source Crypto ATM.

![Cellular router and Pi](https://github.com/anthonybudd/Open-Source-Crypto-ATM/blob/master/misc/complete.jpg?raw=true)
