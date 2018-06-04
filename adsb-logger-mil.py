import sys
import signal
import glob
import RPi.GPIO as GPIO
import time
import re

RED_LED = 19
YELLOW_LED = 13
GREEN_LED = 26
BLINK_DURATION = 0.01 

def enableLED(theLED, flag):
    GPIO.output(theLED, flag)

def setupIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(YELLOW_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    enableLED(RED_LED, False)
    enableLED(YELLOW_LED, False)
    enableLED(GREEN_LED, False)

def blinkLED(theLED, duration):
    enableLED(theLED, True)
    time.sleep(duration)
    enableLED(theLED, False)

def cycleLEDs(count):
    enableLED(RED_LED, False)
    enableLED(YELLOW_LED, False)
    enableLED(GREEN_LED, False)
    for x in range(0, count):
        blinkLED(RED_LED, 0.10)
        blinkLED(YELLOW_LED, 0.10)
        blinkLED(GREEN_LED, 0.10)

def shutdownEvent(signal, frame):
    enableLED(RED_LED, True)
    enableLED(YELLOW_LED, False)
    enableLED(GREEN_LED, False)
    print("Shutting down cleanly...")
    sys.exit(0)

def getCallsign(adsbdata):
    dataVals = adsbdata.split(",")
    return(dataVals[10])

def writeADSBHeader(filename):
    theFile = open(filename, "a")
    theFile.write("ICACO ID,Date,Time,Callsign,Altitude,Ground Speed,Ground Track Angle,Lat,Lon,Vertical Rate,Squawk\n")
    theFile.close()

def getDateTime(adsbdata):
    dataVals = adsbdata.split(",")
    theDate = dataVals[6]
    theTime = dataVals[7]
    return theDate.replace("/","") + "-" + theTime[:8].replace(":","")

def writeADSBData(filename, adsbdata, idx):
    dataVals = adsbdata.split(",")
    hex_ident = dataVals[4]
    generated_date = dataVals[6]
    generated_time = dataVals[7]
    callsign = dataVals[10]
    altitude = dataVals[11]
    ground_speed = dataVals[12]
    track = dataVals[13]
    lat = dataVals[14]
    lon = dataVals[15]
    vertical_rate = dataVals[16]
    squawk = dataVals[17]
    theFile = open(filename, "a")
    dataRow = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n"
    theFile.write(dataRow.format(hex_ident,generated_date,generated_time,callsign,
                                 altitude,ground_speed,track,lat,lon,vertical_rate,squawk))
    theFile.close()
    idx += 1
    if idx % 5 == 0:
        print "{0} : {1} ADS-B rows".format(getDateTime(adsbdata), idx)
        flushOut()
    if idx % 1 == 0:
        blinkLED(YELLOW_LED, BLINK_DURATION)
    return idx

def writeCallsigns(filename, callsigns, idx, adsbdata):
    theFile = open(filename, "w")
    for cs in callsigns:
        theFile.write(cs + "\n")
    theFile.close()
    idx += 1
    if idx % 10 == 0:
        print "{0} : {1} callsigns".format(getDateTime(adsbdata), idx)
        flushOut()
    return idx 

def flushOut():
    sys.stdout.flush()

def isValidRec(rec):
    cnt = rec.count(',')
    if cnt == 21:
        return 1
    return 0

def isMilCallsign(cs):
    match = re.search(r'(^[A-Z]{4})|(^RCH)', cs)
    if match:
        return 1
    else:
        return 0


signal.signal(signal.SIGTERM, shutdownEvent)
signal.signal(signal.SIGINT, shutdownEvent)
signal.signal(signal.SIGTSTP, shutdownEvent)

setupIO()
cycleLEDs(3)

callsigns = set()
firstRow = 1
adsbIdx = 0
csIdx = 0

for adsbdata in sys.stdin:
    if not isValidRec(adsbdata):
        blinkLED(RED_LED, BLINK_DURATION)
        print "Bad ADS-B data: <{0}>".format(adsbdata)
        flushOut()
    else:
        if (firstRow):
            dt = getDateTime(adsbdata)
            print "{0} : Starting new log".format(dt)
            flushOut();
            csfn = "callsign-" + dt + ".txt"
            adsbfn = "adsbdata-" + dt + ".txt"
            writeADSBHeader(adsbfn)
            firstRow = 0

        cs = getCallsign(adsbdata)
        if isMilCallsign(cs):
            adsbIdx = writeADSBData(adsbfn, adsbdata, adsbIdx)
            oldLen = len(callsigns)
            callsigns.add(cs)
            newLen = len(callsigns)
            if newLen > oldLen:
                blinkLED(GREEN_LED, BLINK_DURATION)
                csIdx = writeCallsigns(csfn, sorted(callsigns), csIdx, adsbdata)
