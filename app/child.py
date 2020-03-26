'''This File is run as an exectuble and run in the background'''

#childnode makes a request to the head with a key, then the server determines whether that key can be used to connect to the server
#everytime the child node is connected, the terminal outputs the IP Address and Port that you need to add to the Webapp
#the web app stores which nodes are awake by trying a connection with each of them, when the /home page is loaded, but doesnt connect until the user expliclity opens that node
#this is done so only one connection at a time is maintained from the server to the child