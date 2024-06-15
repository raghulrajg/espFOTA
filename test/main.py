import espFOTA

#Avoid the GPIO pin number 2 because of predefine pin(Network status indicator)

#server connection config
host = "package.xyz.com/newversion"

#WiFI Network connection config
SSID = "YOUR_APN_NAME"
Password = "YOUR_APN_PASSWORD"

OTAUpdate = espFOTA.espFOTA(SSID, Password, host)

def loop():
    while True:
        #Put your code here
        OTAUpdate.run()

if __name__ == '__main__':
    loop()