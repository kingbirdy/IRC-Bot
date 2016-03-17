import atexit
import socket

server = "chat.freenode.net:6667"
nick = "KingTestBot"
user = "KingTestBot"
name = "KingTestBot"
master = "kingbirdy"
channels = "#kingbottest"
reject = "I only accept that command from my owner"

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IRC.connect((server.split(':')[0], int(server.split(':')[1])))

nickMsg = "NICK " + nick
userMsg = "USER " + user + " 0 * :" + name


def send(msg):
    print '>' + msg
    IRC.send(msg + '\r\n')


def privmsg(msg, user):
    send('PRIVMSG ' + user + " :" + msg)


def parseCmd(cmd, sender, channel):
    cmd = cmd[1:]
    cmd = cmd.split()
    c = cmd[0].lower()
    if (c == "sum"):
        sum = 0;
        for x in xrange(1, len(cmd)):
            sum += int(cmd[x])
        privmsg(str(sum), channel)
    elif (c == "join"):
        if(sender != master):
            privmsg(reject, channel)
            return
        send('JOIN ' + cmd[1])
    elif (c == "leave"):
        if(sender != master):
            privmsg(reject, channel)
            return
        send('PART ' + cmd[1])
    elif (c == "quit"):
        if(sender != master):
            privmsg(reject, channel)
            return
        exit()


def receive(msg):
    if msg: #won't print empty lines
        print '<' + msg
    m = msg.split(" ", 3)
    if m[1] == "376": #end of MOTD, join channels now
        send('JOIN ' + channels)
    elif m[0] == "PING": #PONGs the server's PING
        send (str.replace(msg, 'PING', 'PONG'))
    elif m[1] == "PRIVMSG": #
        sender = m[0].split("!")[0][1:] #person who sent msg
        if m[2] == nick: #private message to bot
            parseCmd(m[3], sender, sender)
        else: #message in channel
            parseCmd(m[3], sender, m[2])

@atexit.register #will automatically log out on close
def logout():
    send('QUIT')
    IRC.close()

send(nickMsg)
send(userMsg)

buffer = ''
while True:
    if '\r\n' not in buffer:
        buffer += IRC.recv(512)
    if not buffer:
        break
    line, buffer = buffer.split('\r\n', 1)
    receive(line)
logout()