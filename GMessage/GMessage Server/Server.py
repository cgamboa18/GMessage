import socket
from _thread import *
import sys
import mysql.connector

# Database connection details
db_config = {
    'user': 'root',
    'password': 'cg18database',
    'host': 'localhost',
    'database': 'chatdb'
}

# Initialize the table
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        address TEXT,
                        content TEXT)''')
    conn.commit()
    cursor.close()
    conn.close()

# Add a message to the table
def add_message(address, content):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (address, content) VALUES (%s, %s)', (address, content))#need to find better way to split
    conn.commit()

    cursor.close()
    conn.close()

# Get a message from the table
def get_message(index):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = f'SELECT address FROM messages ORDER BY id DESC LIMIT 1 OFFSET {index}'
    cursor.execute(query)
    address = cursor.fetchone()

    query = f'SELECT content FROM messages ORDER BY id DESC LIMIT 1 OFFSET {index}'
    cursor.execute(query)
    content = cursor.fetchone()

    cursor.close()
    conn.close()

    return f"{address[0]}{content[0]}" if content else ": "

# Server setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "0.0.0.0"
port = 9999

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    sys.exit()

s.listen(2)
print("Waiting for a connection")

def threaded_client(conn, addr):
    global numClientsConnected
    global numCLientsUpdated

    conn.send(str.encode("Sending Message"))
    numClientsConnected += 1
    
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                message = data.decode('utf-8')
                print(f"Received: {addr[0]}-{message}")
                
                if message.split(":")[0] == "LOAD_DATA_REQ":
                    requestIndex = message.split(":")[1]

                    #This will answer request for loading data
                    if(numCLientsUpdated < numClientsConnected):
                        reply = get_message(requestIndex)

                        if (requestIndex == "9"): numCLientsUpdated += 1
                    else:
                        numCLientsUpdated = numClientsConnected
                        reply = "NO_NEW_DATA"
                else:
                    #This will send message to database wih address attached
                    add_message(addr[0], message)
                    numCLientsUpdated = 0
                    reply = "Message recieved"
                
                print("Sending: " + reply + f" C:U {numClientsConnected}:{numCLientsUpdated}")
                conn.sendall(str.encode(reply))
        except Exception as e:
            print(e)
            break

    print("Connection Closed")
    add_message("SERVER", f": [{addr[0]} DISCONNECTED]")
    numClientsConnected -= 1
    numCLientsUpdated = 0
    conn.close()

init_db()

numClientsConnected = 0
numCLientsUpdated = 0

# Main server loop
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    add_message("SERVER", f": [{addr[0]} CONNECTED TO THE SERVER]")

    start_new_thread(threaded_client, (conn, addr))