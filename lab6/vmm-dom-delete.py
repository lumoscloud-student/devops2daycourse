#!/usr/bin/python

import requests
import json
import sys
from getpass import getpass

acipod = raw_input('Which ACI Pod # are you trying to push data to? ')
username = raw_input('What is your student admin username (e.g. student1, student2, etc)? ')
password = getpass('What is your student password? ')
apic = '10.29.10{0}.24'.format(acipod)

auth = {'aaaUser': {'attributes': {'name': username, 'pwd': password } } }

s = requests.Session()
r = s.post('https://{0}/api/mo/aaaLogin.json'.format(apic), data=json.dumps(auth), verify=False)
status = r.status_code
cookies = r.cookies
headers = r.headers
text = r.text


# Now here is a simple example of making a query of the ACI APIC, receiving the returned data in JSON format, which corresponds quite nicely 
# with what Python natively calls a 'dict' or a 'dictionary' which is basically a list of information but in a nice, neat format 
# where every bit of data (value) has a corresponding handle (key), so we call this a key-value-pair, where every value has an associative key to it
# This is also commonly referred to as an 'associative array'
# The little brother to this would be what would be a non-associative array, where we still have an array of data, but the way we reference that data is 
# not in by calling on a 'key', but rather by calling on a position, and we always start counting at zero, so the position of the data might be 
# 0 or 1 or 2 or ... well, you get the idea. Now those kinds of arrays in Python are either called 'lists' or 'tupples' - each with it's own merit 
# Once we get the associative array (dict), we then cycle over all of the resulting information by calling on the key we want to learn info about over and over and over again
# This is what we mean when we say 'iterating' over the resulting array or dataset

# The thing we're going to query here is all of the VMM Domains -- Cisco ACI calls this the 'vmmDomP' class -- and we want to find all the names of the vCenter VMM Domains
# Students in our step-by-step FE classes don't always name them what we tell them to name them, and when we go to clean off the fabric by 
# restoring a base config, the VMM Domains don't get deleted for some odd reason
# So here is our way of learning about them, and once we know what their "names" are - which is really their 'DN' or Distinguished Name, we can then 
# tell them to get lost - like in a permanent way

# First let's make the query
# If you're ever in need of wanting to know how to query something (or a lot of things) that maybe the WebUI doesn't have a web page that gatehrs the info
# we want (thus being able to capture it from the API Inspector), we can use the tool called 'Visore' to get what we want from a WebUI perspective, 
# and it will also give us the corresponding REST API query we need to make -- Ask the instructor to go over the Visore WebUI tool with the class

# Here we are making the call via the Python 'requests' module to issue an HTTP GET and ask the APIC REST API to send us all of the returned data
# in the serial data structure of JSON and we are making the REST call to the sub-api URL of 'mo/uni/vmmp-VMware.json'
# which, specifically is the Managed Object (mo) at the hierarchy of 'uni' (Universe), 'vmmp-ANYNAME' (VMM Provider) 
# and finally by using the '.json' suffix, this tells the REST API what serial data structure we intend to either POST or in this case GET data in
# We could just as easily replace that suffix with '.xml', so long as we intended to send, or here, recieve data in the XML format
r = s.get('https://{0}/api/node/class/vmmDomP.json'.format(apic), cookies=cookies, verify=False)
# Print what we found to stdout (screen)
print r
# Response looks good
# Let's see what the text from the response looks like
print r.text
# And let's see what data type the text is in
type(r.text)
# Unicode huh?
# Let's turn what we just got from that REST call into a Python dict, by calling on the JSON method 
data = r.json()
# And now let's see what data type the variable 'data' is in
type(data)
# A dict, perfect, now we can easily iterate over it


# Now we get to begin looking at the infamous 'for' loop
# Almost every programming languange in the world has some sort of a 'loop' mechanism to be able to grab large lists of data and go over it 
# and once we find the item we are looking for, to then change the value for just that item, or quite possibly to change the value for all items we find
# or possibly just to print/list all of those items
# Here we are iterating over the returned list of VMM Domains, and looking for only the 'attributes' which contain the 'dn' 
# and first finding out what 'type' the data is returned in and then printing those DNs to screen
for i in data['imdata']:
    vmmDomDn = i['vmmDomP']['attributes']['dn']
    type(vmmDomDn)
    print vmmDomDn
# By the way, if you chose for any reason to manually type the above in, or you copy and pasted each line, but possibly didn't 
# pay very close attention to indentation spacing, then your 'for' loop in Python likely did not work
# This is because Python REALLY REALLY REALLY REALLY cares a lot about spacing and indentation
#
# For instance - if you indent everything inside the 'for' loop to 2 spaces, it will work:
#for i in data['imdata']:
#  vmmDomDn = i['vmmDomP']['attributes']['dn']
#  type(vmmDomDn)
#  print vmmDomDn
#RESULT: WORKS
#
# If you indent everything inside the 'for' loop to 4 spaces, it will work:
#for i in data['imdata']:
#    vmmDomDn = i['vmmDomP']['attributes']['dn']
#    type(vmmDomDn)
#    print vmmDomDn
#RESULT: WORKS
#
# However, if you indent some lines inside the 'for' loop to 2 spaces and others to 3 or 4 spaces, nothing will work:
#for i in data['imdata']:
#    vmmDomDn = i['vmmDomP']['attributes']['dn']
#    type(vmmDomDn)
#   print vmmDomDn
#RESULT: FAILS



# Now we are iterating over the same list of VMM Domains, and again looking for only the 'attributes' which contain the 'dn' 
# but now we are dynamically updating a field in the 'jsondata' and telling it that for every entry it finds,
# firstly to turn the 'vmmDomDn' into a string and then secondly to set the 'status' of each to 'deleted'
# then we create a variable 'r' and tell the Python 'requests' module to issue an HTTP POST and send the API a JSON file of data,
# which should delete every VMM Domain found
# By the way, you can see that I have this code commented out below
# This is simply because I wanted you to see HOW to do it, but not actually perform the task
# This is because, if you did, and you happened to be the first student to get to this task, none of the other students would be 
# able to perform this or even the previous 'for' loop in this lab

# PLEASE DO NOT UNCOMMENT THE BELOW LINES AND DO NOT EXECUTE THE REMAINDER OF THIS FOR LOOP
# To prove that it works, The Instructor of the course will perform it live on the projector for all students to see
# Then we will erase the ACI Fabric and move on to the next set of labs
for i in data['imdata']:
    vmmDomDn = i['vmmDomP']['attributes']['dn']
    jsondata = {"vmmProvP":{"attributes":{"dn":"uni/vmmp-VMware","status":"modified"},"children":[{"vmmDomP":{"attributes":{"dn":str(vmmDomDn),"status":"deleted"},"children":[]}}]}}
    # r = s.post('https://{0}/api/node/mo/uni/vmmp-VMware.json'.format(apic), cookies=cookies, data=json.dumps(jsondata), verify=False)
    # print r.text


# After the instructor uncomments and runs the above Delete 'for' loop for everyone, then try to rerun the Print 'for' loop and see what it returns
for i in data['imdata']:
    vmmDomDn = i['vmmDomP']['attributes']['dn']
    type(vmmDomDn)
    print vmmDomDn
# Any ideas why the WebUI shows everything as deleted, but this 'for' loop still shows exactly the same information that it did before 
# the Instructor ran the Delete 'for' loop?
# Theorize your answers and discuss them with the Instructor

# That's it for this lab!

