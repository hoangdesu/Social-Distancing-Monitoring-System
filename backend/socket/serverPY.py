#server.py 

import socket 

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
host = socket.gethostname()
print(host)
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

s.listen(1) # 1 ở đây có nghĩa chỉ chấp nhận 1 kết nối
print("Server listening on port", port)

c, addr = s.accept()
print("Connect from ", str(addr))

#server sử dụng kết nối gửi dữ liệu tới client dưới dạng binary
c.send(b"Hello, how are you")
# c.send("Bye", encode())
c.close()