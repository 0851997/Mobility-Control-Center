import mysql.connector as mysqlconn
import modules.timer as tm
import modules.services as sv
import modules.testservices as tsv

username = ''
password = ''
server_address = ''

#SSHTunnel connection
timer = tm.Timer()
ssh_conn = tsv.SSHTunnel(server_address, 22, username, password, 'localhost', 3306)
ssh_conn.createSSHTunnelForwarder()
ssh_conn.startTunnel()
timer.postpone(5, f'ssh connection status: {ssh_conn.tunnelForwarder.local_is_up((server_address, 22))} ')

#MySql connection
mysql_conn = sv.MySQLConnector(username, password, 'smarterdam_parking', 'localhost', ssh_conn.tunnelForwarder.local_bind_port)
mysql_conn.startConnection()
print(f'db connection status: {mysql_conn.connection.is_connected()} \n')

#Wiegand scanner
rfid_scanner = sv.Wiegand()

#create parking lot and parking block
mysql_conn.insertLot('proofOfConcept', 1, 0)
mysql_conn.insertWing('NORTH', 3, 3, 0, 'proofOfConcept')
mysql_conn.insertWing('EAST', 4, 4, 0, 'proofOfConcept')
mysql_conn.insertWing('WEST', 4, 4, 0, 'proofOfConcept')
mysql_conn.insertWing('SOUTH', 3, 3, 0, 'proofOfConcept')

#logic
isRunning = True
while isRunning:
    print('Scan your card: ')
    rfid_parking_space = rfid_scanner.run()
    if rfid_parking_space == '5b35866e':
        isRunning = False
    elif rfid_parking_space != None:
        space_number = input('Space number: ')
        id_parking_wing = input('Parking wing: ')
        print('Rfid parking space tag: ', rfid_parking_space)
        mysql_conn.insertSpace(rfid_parking_space, space_number, 1, id_parking_wing)

#closing all connections
print('\nabout to close connections')
mysql_conn.closeConnection()
ssh_conn.closeTunnel()