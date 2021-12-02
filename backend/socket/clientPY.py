#client .py

import socket 

# Như mình đã nói ở trên thì chúng ta không truyền tham số vào vẫn ok
s = socket.socket()
host = socket.gethostname()
s.connect((host, 4000)) 

# 1024 là số bytes mà client có thể nhận được trong 1 lần
# Phần tin nhắn đầu tiên
msg = s.recv(1024)

# Phần tin nhắn tiếp theo 
while msg:
  print("Recvied ", msg.decode())
  msg = s.recv(1024)

s.close()