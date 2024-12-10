# pyredis

A Redis Server Clone using Python


## Setup 

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Test
```
pytest --capture=no --verbose
```

## Run Server
```
python3 -m pyredis
```

## Run Client on Terminal
```
 nc localhost <port>
```

Example Commands on Ubuntu
* Use -e to enable interpertation of backslash
* Use single quote to interpert special characters like $

```
echo -e '*1\r\n$4\r\nPING\r\n' | nc localhost 7
echo -e '*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n' | nc localhost 7
```