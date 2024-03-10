import ipaddress
import socket
import argparse 

print("""
.______        ___      .______        ______   ______    _______   _______ 
|   _  \      /   \     |   _  \      /      | /  __  \  |       \ |   ____|
|  |_)  |    /  ^  \    |  |_)  |    |  ,----'|  |  |  | |  .--.  ||  |__   
|   _  <    /  /_\  \   |      /     |  |     |  |  |  | |  |  |  ||   __|  
|  |_)  |  /  _____  \  |  |\  \----.|  `----.|  `--'  | |  '--'  ||  |____ 
|______/  /__/     \__\ | _| `._____| \______| \______/  |_______/ |_______|
                                                                            
Peep!

Reverse PTR host lookup with the ability to provide
ranges in all formats:

1.1.1.1
1.1.1.1/28
1.1.1.1-1.1.1.100

and also the ability extending the lookup range.

Examples usage: python3 barcode.py -l 200 -d sapiens_old.txt -i ips_old.txt
Where: -l is how much ip's to look forward and backwards
-d is a keyword file containing all keywords the script will look for in the resplved name.
-i is the IP list to scan.
      """)
parser = argparse.ArgumentParser()

# Argument for the IP range file
parser.add_argument(
    '-i','--ip_file', 
    type=str, 
    help='Path to a file containing IP ranges (single IP, CIDR, or range format).'
)

# Argument for the override database
parser.add_argument(
    '-o','--override_db', 
    type=str, 
    default="false",
    help="Choose if to fetch known ip's from the database or look them up again and override database query."
)

# Argument for lookahead and lookbehind counter
parser.add_argument(
    '-l', '--look_range',
    type=int, 
    default=512, 
    help="""Lookahead and lookbehind counter (default: 512). 
    For example '-l 2' on 10.10.10.10 will return 10.10.10.8,10.10.10.9,10.10.10.10,10.10.10.11,10.10.10.12."""
)

# Argument for the domain list file
parser.add_argument(
    '-d', '--domain_list', 
    type=str, 
    help="""Path to a text file containing a list of TLDs and key wordlist you want 
    to search in the output list. A TLD like example.com will be extracted to example and example.com as search terms."""
)

# Parse arguments
args = parser.parse_args()

import sqlite3

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ Create table if it doesn't exist """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ip_hostname (ip TEXT PRIMARY KEY, hostname TEXT)''')
    except sqlite3.Error as e:
        print(e)

def get_ip_range(ip_str, offset=args.look_range):
    # Convert the input string to an IPv4Address object
    ip = ipaddress.ip_address(ip_str)
    
    # Generate a range of IPs
    ip_range = []
    for i in range(-offset, offset + 1):
        try:
            new_ip = ip + i
            ip_range.append(str(new_ip))
        except ValueError:
            # Skip if the new IP is out of the IPv4 range
            continue

    return ip_range

def get_domain_name(ip_address):
    try:
        result=socket.gethostbyaddr(ip_address)
        return list(result)[0]
    except socket.herror as e:
        pass

with open(args.ip_file) as ips:
    ip_ranges = ips.readlines()
    ip_ranges = [x.strip("\n".strip(" ")) for x in ip_ranges]

final_list = []
for ip_range in ip_ranges:
    if '/' in ip_range:
        final_list = list(set([str(ip) for ip in ipaddress.ip_network(ip_range, strict=False)]+final_list))
    
        # Handle range notation
    elif '-' in ip_range:
        start_ip, end_ip = ip_range.split('-')
        start_ip = ipaddress.ip_address(start_ip.strip())
        end_ip = ipaddress.ip_address(end_ip.strip())
        final_list = list(set([ipaddress.ip_address(i).exploded for i in range(int(ipaddress.ip_address(start_ip)), int(ipaddress.ip_address(end_ip)))]+final_list))
        
    #    Single IP
    else:
        final_list = list(set([ip_range.strip()]+final_list))

# We add 512 ips left and right
final_list_expanded = []    
for ip in final_list:
    final_list_expanded = list(set(final_list_expanded+get_ip_range(ip)))


database = "ip_hostname.sqlite"
# Create a database connection
conn = create_connection(database)
create_table(conn)
cur = conn.cursor()
        
tlds_expanded = []
tlds = []
if args.domain_list:
    with open(args.domain_list, "r") as queries:
        tlds = queries.readlines()
        tlds = [y.strip("\n").lower() for y in tlds]
        tlds_expanded = list(set([z.split(".")[0].lower() for z in tlds]+tlds))
 
print(f"Total IP's to check: {len(final_list_expanded)}")
print(f"Average speed is : 1,440 ips per hour. Estimated time(If no records in db) is around: {round(len(final_list_expanded)/1440)} Hours.")
#Check if ip in table
for ip in final_list_expanded:
    # Check if ip in database already:
    cur.execute("SELECT hostname FROM ip_hostname WHERE ip = ?", (ip,))
    row = cur.fetchone()
    if (row) and (args.override_db.lower() == "false"):
        #print(f"IP {ip} already exists with hostname {row[0]}")
        ptr = row[0]
        
        if len(tlds_expanded) > 0:
            for i in tlds_expanded:
                if ptr != None:
                    if i in ptr.lower():
                        print(ptr)        
    #IP not in database
    else:
        ptr = get_domain_name(ip)
        if len(tlds_expanded) > 0:
            for i in tlds_expanded:
                if ptr != None:
                    if i in ptr.lower():
                        print(ptr)        
        else:
            print("No TLD file added. Showing all results:")
            if ptr != None:
                print(ptr)
                
        cur.execute("INSERT OR REPLACE INTO ip_hostname (ip, hostname) VALUES (?, ?)", (ip, ptr))
        conn.commit()
            
print("Finished!\nIf you see no results it means none were found.")