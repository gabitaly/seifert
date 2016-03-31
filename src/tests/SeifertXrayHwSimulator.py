import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Then bind() is used to associate the socket with the server address.
#In this case, the address is localhost, referring to the current server, and the port number is 10001.
# Bind the socket to the port
server_address = ('localhost', 10001)
print ("starting up on %s port %s") % server_address
sock.bind(server_address)

#Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    #accept() returns an open connection between the server and client, along with the address of the client.
    #The connection is actually a different socket on another port (assigned by the kernel).
    #Data is read from the connection with recv() and transmitted with sendall().
    #When communication with a client is finished, the connection needs to be cleaned up using close().
    #This example uses a try:finally block to ensure that close() is always called, even in the event of an error.
    try:
        print ("connection from", client_address)

        reply = ""
        command = ""
        currentTarget = "*0000017000\n"
        currentActual = "*0000017000\n"
        voltageTarget = "*0000019000\n"
        voltageActual = "*0000019000\n"

        exposureTimerSec = "*0000045246\n"

        statusWord12Code = "*0000000076\n" #Shutter not connected
        statusWord1 = "*0000000032\n" #0100 0000 Bit6=1 High Voltage ON
        statusWord2 = "*0000000032\n"
        statusWord3 = "*0000000016\n"
        statusWord4 = "*0000000008\n"
        statusWord6 = "*0000000004\n"
        statusWord14 = "*0000000100\n" #Water flow rate operating point
        statusWord15 = "*0000000090\n" #Current Water flow rate point

        warmUpTimeLeft = "*0000000999\n"
        anodeMaterial = "*Co\n"

        focus = "*0.15 x 8 mm\n"            

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)                                                        
            
            if data:
                #Here we have to consider all commands received from the Karabo device regardless of their parameters
                command = data[:2]

                # HIGH VOLTAGE
                if command == "HV":
                    print ("\n\nReceived %s") % data
                    if (data.rstrip() == "HV:1"):
                        print "High Voltage ON"
                        statusWord1 = "*0000000064\n"
                    elif (data.rstrip() == "HV:0"):
                        print "High Voltage OFF"
                        statusWord1 = "*0000000032\n"

                #CURRENT SETPOINT
                elif command == "SC":
                    print ("\n\nReceived %s") % data                    
                    currentTarget = "*00000"+data[3:5]+"000\n"
                    currentActual = currentTarget
                    print currentTarget, currentActual
                    print ("Setting Current Target to %s and Actual Current to %s" % (currentTarget, currentActual))

                elif command == "CN":
                    print ("\n\nReceived %s") % data                    
                    reply = currentTarget
                    print ("Sending Current Target Setpoint %s") % reply
                    
                elif command == "CA":
                    print ("\n\nReceived %s") % data                    
                    reply = currentActual
                    print ("Sending Current Actual Setpoint %s") % reply

                #VOLTAGE SETPOINT
                elif command == "SV":
                    print ("\n\nReceived %s") % data                    
                    voltageTarget = "*00000"+data[3:5]+"000\n"
                    voltageActual = voltageTarget
                    print ("Setting Voltage Target to %s and Actual Voltage to %s" % (voltageTarget.rstrip(), voltageActual.rstrip())) 

                elif command == "VN":
                    print ("\n\nReceived %s") % data                    
                    reply = voltageTarget
                    print ("Sending Voltage Target Setpoint %s") % reply

                elif command == "VA":
                    print ("\n\nReceived %s") % data                    
                    reply = voltageActual
                    print ("Sending Voltage Actual Setpoint %s") % reply

                #EXPOSURE TIMERS
                elif command == "TN":
                    print ("\n\nReceived %s") % data                    
                    reply = exposureTimerSec
                    print ("Sending Exposure Timer 3 Setpoint value (sec) %s") % reply

                elif command == "TP":
                    print ("\n\nReceived %s") % data
                    print ("Setting Exposure Timer3 values...")
                    values = data.split(",")
                    hhSec = int(values[1]) * 3600
                    mmSec = int(values[2]) * 60
                    ss = int(values[3])                   
                    #exposureTimerSec = str(hhSec + mmSec + ss)+"\n"
                    print ("Esposure Timer3 %s hh, %s mm, %s ss") % values[1] % values[2] % values[3]
                     
                elif command == "TS":
                    print ("\n\nReceived %s") % data
                    print ("Setting Exposure Timer 3 ON...")
                       
                elif command == "TE":
                    print ("\n\nReceived %s") % data
                    print ("Setting Exposure Timer 3 OFF...")

                elif command == "TA":
                    print ("\n\nReceived %s") % data                    
                    reply = exposureTimerSec
                    print ("Sending Exposure Timer3 value (sec) %s") % reply
                    

                elif command == "SR":
                    if (data.rstrip() == "SR:12"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord12Code
                        print ("Sending Status Word 12 code %s") % reply
                    elif (data.rstrip() == "SR:01"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord1
                        print ("Sending Status Word 1 %s") % reply
                    elif (data.rstrip() == "SR:02"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord2
                        print ("Sending Status Word 2 %s") % reply
                    elif (data.rstrip() == "SR:03"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord3
                        print ("Sending Status Word 3 %s") % reply
                    elif (data.rstrip() == "SR:04"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord4
                        print ("Sending Status Word 4 %s") % reply
                    elif (data.rstrip() == "SR:06"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord6
                        print ("Sending Status Word 6 %s") % reply
                    elif (data.rstrip() == "SR:14"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord14
                        print ("Sending Status Word 14 %s") % reply
                    elif (data.rstrip() == "SR:15"):
                        print ("\n\nReceived %s") % data                        
                        reply = statusWord15
                        print ("Sending Status Word 15 %s") % reply
                        

                elif command == "SW":
                    print ("\n\nReceived %s") % data                    
                    values = data.split(":")
                    flowRate = values[2]
                    statusWord14 = "*0000000"+flowRate[4]
                    print ("Setting Water Flow rate %s") % values[2]
                    
                elif command == "CL":
                    print ("\n\nReceived %s") % data
                    print ("Acknowledge Error (does nothing)...")
                    
                elif command == "WU":
                    print ("\n\nReceived %s") % data
                    print ("Setting Warm-up Program... (does nothing)")
                    
                elif command == "WT":
                    print ("\n\nReceived %s") % data                    
                    reply = warmUpTimeLeft
                    print ("Sending Warm-up time left %s") % reply

                elif command == "KB":
                    print ("\n\nReceived %s") % data
                    if (data.rstrip() == "KB:0"):
                        print ("Keypad DISABLED!")
                    elif (data.rstrip() == "KB:1"):
                        print ("Keypad ENABLED!")  
                          
                elif command == "FR":
                    print ("\n\nReceived %s") % data
                    reply = focus
                    print ("Sending focus ASCII String %s") % focus                    

                elif command == "MR":
                    print ("\n\nReceived %s") % data                    
                    reply = anodeMaterial
                    print ("Send Anode material %s ") % reply

                elif command == "CC":
                    print ("\n\nReceived %s") % data
                    print ("Beam Shutter Control (does nothing)...")
                         
                elif command == "OS":
                    print ("\n\nReceived %s") % data
                    print ("Open Beam Shutter...")

                elif command == "CS":
                    print ("\n\nReceived %s") % data
                    print ("Close Beam Shutter...")        

                #Eventually send reply to client device
                connection.sendall(reply)

            else:
                print ("no more data from", client_address)
                break
                
    finally:
        # Clean up the connection
        connection.close()    

