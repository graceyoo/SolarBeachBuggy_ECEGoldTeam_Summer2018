########################################################################
# Author: Grace Yoo, CpE
# File Name: autonomousTest.py
# Team: Group 3, GOLD Team
# Group Members: Cecilie Barreto, CpE
#                Drew Curry, EE
# Project: Florida Solar Beach Buggy Challenge
# Sponsor: Duke Energy
# Professors: Dr. Samuel Richie
#             Dr. Lei Wei
########################################################################

# Motor serial information:
# RIGHT MOTOR : 1 reverse, 64 stop, 127 forward
# LEFT MOTOR : 128 reverse, 192 stop, 255 forward

import time
import serial
import threading

# Port addresses to decipher which sensor is reporting data
portJOne   = "1010"
portJTwo   = "1110"
portJThree = "0110"
portJFour  = "0010"

# Set default signal flags
global sideCheck
global leftSensor
global leftFrontSensor
global rightFrontSensor
global rightSensor
global lookingFromLeft
global lookingFromRight

signalGo         = True
startUp          = True
sideCheck        = False
leftFrontSensor  = False
leftSensor       = False
rightFrontSensor = False
rightSensor      = False
lookingFromLeft  = False
lookingFromRight = False

# Serial port for sensors and motors
serialSensors = serial.Serial('/dev/ttyACM0', 9600)
serialMotors  = serial.Serial('/dev/ttyS0'  , 9600, timeout = 10)


class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadLock = threading.Lock()
        
        global corner
        corner = threading.Event()
        
        
        processingData = threading.Thread(target = self.grabData, args=(corner,))
        moveFlipper = threading.Thread(target = self.moveVehicle, args=(corner,4,))
        
        processingData.start()
        moveFlipper.start()
        
        #processingData.join()
        #moveFlipper.join()
        
    #def run(self):
 
        

    ########################################################################
    # Function Name : stop
    # Description   : Command to stop the vehicle
    ########################################################################
    global stop
    def stop():
        serialMotors.write(chr(int('0')))	# Stop both motors
        serialMotors.flush()
        print "STOP!"


    ########################################################################
    # Function Name : left
    # Description   : Command vehicle to turn left
    ########################################################################
    global left
    def left():
        serialMotors.write(chr(int('127')))	# Right Motor, Full Speed
        serialMotors.write(chr(int('192')))	# Left Motor , Stopped
        serialMotors.flush()
        print "LEFT!"


    ########################################################################
    # Function Name : veerLeft
    # Description   : Command vehicle to turn slightly to the left
    ########################################################################
    global veerLeft
    def veerLeft():
        serialMotors.write(chr(int('127'))) # Right Motor, Full Speed
        serialMotors.write(chr(int('218')))	# Left Motor , Half Speed
        serialMotors.flush()
        print "Veer Left!"


    ########################################################################
    # Function Name : right
    # Description   : Command vehicle to turn right
    ########################################################################
    global right
    def right():
        serialMotors.write(chr(int('64'))) 	# Right Motor, Stopped
        serialMotors.write(chr(int('255')))	# Left Motor , Full Speed
        serialMotors.flush()
        print "RIGHT!"


    ########################################################################
    # Function Name : veerRight
    # Description   : Command vehicle to turn slightly to the right
    ########################################################################
    global veerRight
    def veerRight():
        serialMotors.write(chr(int('90'))) 	# Right Motor, Half Speed
        serialMotors.write(chr(int('255')))	# Left Motor , Full Speed
        serialMotors.flush()
        print "Veer Right!"

    ########################################################################
    # Function Name : slowDownHalfSpeed
    # Description   : Command vehicle to slow down forward movement
    ########################################################################
    global slowDownHalfSpeed
    def slowDownHalfSpeed():
        serialMotors.write(chr(int('82'))) 	# Right Motor, Half Speed
        serialMotors.write(chr(int('218')))	# Left Motor , Half Speed
        serialMotors.flush()
        print "Slow Down!"


    ########################################################################
    # Function Name : moveStraightFullSpeed
    # Description   : Command to move vehicle forward at full speed
    ########################################################################
    global moveStraightFullSpeed
    def moveStraightFullSpeed():
        serialMotors.write(chr(int('110')))	# Right Motor, Full Speed
        serialMotors.write(chr(int('255')))	# Left Motor , Full Speed
        serialMotors.flush()
        print "GO!"

    ########################################################################
    # Function Name : reverseHalfSpeed
    # Description   : Check if there are objects detected from side sensors
    ########################################################################
    global reverseHalfSpeed
    def reverseHalfSpeed():
        serialMotors.write(chr(int('33')))	 # Right Motor, Reverse Half Speed
        serialMotors.write(chr(int('160')))	# Left Motor , Reverse Half Speed
        serialMotors.flush()
        print "Reverse Half Speed!"

    ########################################################################
    # Function Name : reverseFullSpeed
    # Description   : Check if there are objects detected from side sensors
    ########################################################################
    global reverseFullSpeed
    def reverseFullSpeed():
        serialMotors.write(chr(int('1')))	  # Right Motor, Reverse Full Speed
        serialMotors.write(chr(int('128')))	# Left Motor , Reverse Full Speed
        serialMotors.flush()
        print "Reverse!"


    ########################################################################
    # Function Name : rotateHalfSpeedLeft
    # Description   : Command vehicle to rotate at half speed to the left
    ########################################################################
    global rotateHalfSpeedLeft
    def rotateHalfSpeedLeft():
        serialMotors.write(chr(int('90')))  # Right Motor, Half Speed
        serialMotors.write(chr(int('160'))) # Left Motor , Reverse Half Speed
        serialMotors.flush()
        print "Rotate Left!"


    ########################################################################
    # Function Name : rotateHalfSpeedRight
    # Description   : Command vehicle to rotate at half speed to the right
    ########################################################################
    global rotateHalfSpeedRight
    def rotateHalfSpeedRight():
        serialMotors.write(chr(int('33')))  # Right Motor, Reverse Half Speed
        serialMotors.write(chr(int('218'))) # Left Motor , Half Speed
        serialMotors.flush()
        print "Rotate Right!"


    ########################################################################
    # Function Name : checkMirrors
    # Description   : Check if there are objects detected from side sensors
    ########################################################################
    global checkMirrors
    def checkMirrors():

        if leftSensor == True and rightSensor == True:
            reverseHalfSpeed()
            time.sleep(2)
            rotateHalfSpeedLeft()
            time.sleep(1)
            #slowDownHalfSpeed()
            print"Check Mirror 1"
            #self.threadLock.release()

        elif leftSensor == True and rightSensor == False:
            reverseHalfSpeed()
            time.sleep(2)
            rotateHlafSpeedRight()
            time.sleep(1)
            #slowDownHalfSpeed()
            print "Check Mirror 2"
            #self.threadLock.release()

        elif leftSensor == False and rightSensor == True:
            reverseHalfSpeed()
            time.sleep(2)
            rotateHalfSpeedLeft()
            time.sleep(1)
            #slowDownHalfSpeed()
            print "Check Mirror 3"
            #self.threadLock.release()
        
        elif leftSensor == False and rightSensor == False:
            reverseHalfSpeed()
            time.sleep(2)
            rotateHalfSpeedRight()
            time.sleep(1)
            #slowDownHalfSpeed()
            print "Check Mirror 4"
            #self.threadLock.release()


    ########################################################################
    # Function Name : checkFrontSensors
    # Description   : Check if there are objects detected from front sensors
    ########################################################################
    global checkFrontSensors
    def checkFrontSensors():
        
        if lookingFromLeft == True:
            lookingFromLeft = False
            
            if signalGo == False:
                
                if rightSensor == True:
                    reverseHalfSpeed()
                    time.sleep(2)
                    rotateHalfSpeedLeft()
                    time.sleep(1)
                    slowDownHalfSpeed()
            
                if rightSensor == False:
                    right()
                    time.sleep(1)
                    slowDownHalfSpeed()
                signalGo = True
            else:
                moveStraightFullSpeed()
                    
        if lookingFromRight == True:
            lookingFromRight = False
            
            if signalGo == False:
                
                if leftSensor == True:
                    reverseHalfSpeed()
                    time.sleep(2)
                    rotateHalfSpeedLeft()
                    time.sleep(1)
                    slowDownHalfSpeed()
            
                if leftSensor == False:
                    left()
                    time.sleep(1)
                    slowDownHalfSpeed()
                signalGo = True
            else:
                moveStraightFullSpeed()
    
    ########################################################################
    # Function Name : grabData
    # Description   : Thread 1
    ########################################################################
    def grabData(self, corner):
        
        while True:
            self.threadLock.acquire()
            print "Lock acquired in grabData"
            if serialSensors.in_waiting > 0:
            
                try:
                    sensorData = serialSensors.readline()
                    port = sensorData[0:4].strip('\r\n')
                    print "Port: ", port
                    rawDistance = sensorData[5:7].strip('\r\n')
                    print "Raw Distance: ", rawDistance
                    try:
                        distance = int(rawDistance) * 10
                        print "Distance: ", distance
                    except ValueError:
                        pass

                    # Differentiate the distance detected by ports
                    # Process distances to determine appropriate response
                    # J1 is Left, J2 is Front Left, J3 is Front Right, J4 is Right
                    if port == portJOne:
                        global jOneDis
                        jOneDis = distance
                        print "Port J1: ", jOneDis

                        if jOneDis >= 40:
                            leftSensor = False

                        elif jOneDis <= 30:
                            leftSensor = True
                            lookingfromLeft = True

                    if port == portJTwo:
                        global jTwoDis
                        jTwoDis = distance
                        print "Port J2: ", jTwoDis

                        if jTwoDis > 70:
                            signalGo = True
                            if corner.isSet():
                                corner.clear()

                        elif 40 <= jTwoDis <= 70:
                            signalGo = True
                            leftFrontSensor = False
                            if corner.isSet():
                                corner.clear()

                        elif jTwoDis <= 30:
                            signalGo = False
                            leftFrontSensor = True
                            pass

                    if port == portJThree:
                        global jThreeDis
                        jThreeDis = distance
                        print "Port J3: ", jThreeDis

                        if jThreeDis > 70:
                            signalGo = True
                            rightFrontSensor = False
                            if corner.isSet():
                                corner.clear()

                        elif 40 <= jThreeDis <= 70:
                            signalGo = True
                            rightFrontSensor = False
                            if corner.isSet():
                                corner.clear()

                        elif jThreeDis <= 30:
                            signalGo = False
                            rightFrontSensor = True

                    if port == portJFour:
                        global jFourDis
                        jFourDis = distance
                        print "Port J4: ", jFourDis

                        if jFourDis >= 40:
                            rightSensor = False

                        elif jFourDis <= 30:
                            rightSensor = True
                            lookingFromRight = True
                        
                except serial.serialutil.SerialException:
                    print("No obstacle detected.")
                    jTwoDis   = 250
                    jThreeDis = 250
            self.threadLock.release()
            print "Lock released in grabData"
            
    ########################################################################
    # Function Name : moveVehicle
    # Description   : Thread 2
    ########################################################################            
    def moveVehicle(self, corner, timeout):
        global signalGo
        global startUp
        while True:
            if signalGo == True and startUp == True:
                startUp = False
                moveStraightFullSpeed()
                pass
            # Differentiate the distance detected by ports
            # Process distances to determine appropriate response
            # J1 is Left, J2 is Front Left, J3 is Front Right, J4 is Right
            while corner.wait(4):
                self.threadLock.acquire()
                print "Lock acquired in Move Vehicle"
                print "Waiting for updated distance after turn!"
                
                if leftSensor == True and rightSensor == True:
                    reverseHalfSpeed()
                    time.sleep(1)
                    rotateHalfSpeedRight()
                    time.sleep(1)
                    stop()
                    time.sleep(3)
                    self.threadLock.release()

                elif leftSensor == True:
                    rotateHalfSpeedRight()
                    time.sleep(1)
                    stop()
                    time.sleep(3)
                    self.threadLock.release()
                    
                elif rightSensor == True:
                    rotateHalfSpeedLeft()
                    time.sleep(1)
                    stop()
                    time.sleep(3)
                    self.threadLock.release()
                else:
                    rotateHalfSpeedLeft()
                    time.sleep(1)
                    stop()
                    time.sleep(3)
                    self.threadLock.release()
                
            while not corner.isSet():
                try:
                    self.threadLock.acquire()
                    print "Lock acquired in Move Vehicle"
                    print"jTwoDis :", jTwoDis
                    print"jThreeDis :", jThreeDis
                    if jTwoDis > 70:
                        moveStraightFullSpeed()

                    elif 30 <= jTwoDis <= 70:
                        slowDownHalfSpeed()

                    elif jTwoDis == 0:
                        stop()
                        time.sleep(2)
                        checkMirrors()
                        #stop()
                        time.sleep(3)
                        corner.set()
                        

                    elif jThreeDis > 70:
                        moveStraightFullSpeed()

                    elif 30 <= jThreeDis <= 70:
                        slowDownHalfSpeed()

                    elif jThreeDis == 0:
                        stop()
                        time.sleep(2)
                        checkMirrors()
                        time.sleep(3)
                        stop()
                        corner.set()
                        
                except NameError:
                    pass
                self.threadLock.release()
                print "Lock Released in Move Vehicle"
            
       

pleaseWork = Thread()
print "Thread 1 Alive:", processingData.is_alive()
print "Thread 2 Alive:", moveFlipper.is_alive()

