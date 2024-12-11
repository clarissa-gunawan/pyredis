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
python3 -m pyredis.main
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
echo -e '*1\r\n$4\r\nPING\r\n*1\r\n$4\r\nPING\r\n' | nc localhost 7
```


## Using Redis CLI to Test

Ensure that you have disabled redis-server

Check if redis-server is NOT alive e.g.  `[ - ]  redis-server`
```
service --status-all | grep redis
```

Stop redis-server
```
service redis-server stop
```

Start redis-server
```
service redis-server start
```