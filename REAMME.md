# TCP-PROXY
## function
local TCP connect -> remote TCP address(IP/Host:port)

## How to use
* Command
```bash
python main.py local_port hostname port
```
* Example
```bash
sudo python main.py 80 127.0.0.1 8088
```
* Successful output
> Listening for incoming connections on 127.0.0.1:65530. --> 127.0.0.1:8088
