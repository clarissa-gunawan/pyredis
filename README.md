# pyredis

A Redis Server Clone using Python


## Setup 

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup Dev Dependencies

```
pip install -r requirements-dev.txt
```

#### Install pre-commit
```
pre-commit install
pre-commit run --all-files
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
echo -e '*1\r\n$4\r\nPING\r\n*1\r\n$4\r\nPING\r\n' | nc localhost 7
```

## Run Client with redis-cli
```
redis-cli -p 6380 PING
redis-cli -p 6380 PING "Hello World"
redis-cli -p 6380 ECHO "Hello World"
redis-cli -p 6380 SET message "Hello World"
redis-cli -p 6380 GET message
```

## Lint & Format
Use [Ruff](https://docs.astral.sh/ruff/)

Lint
```
ruff check                  # Lint all files in the current directory.
ruff check --fix            # Lint all files in the current directory, and fix any fixable errors.
```

Format
```
ruff format                   # Format all files in the current directory.
ruff format --check           # Avoid writing any formatted files back; instead, exit with a non-zero status code if any files would have been modified, and zero otherwise
ruff format --diff            # Avoid writing any formatted files back; instead, exit with a non-zero status code and the differencebetween the current file and how the formatted file would look like
```

## Logging
See logs
```
 tail -f /tmp/pyredis.log
```

## Benchmark
```
# Profile Setup
python3 -m cProfile -o /tmp/pyredis-out.pstats pyredis/__main__.py

# Benchmark Examples
redis-benchmark -p 6380 -t get,set -n 1000 -q
redis-benchmark -p 6380 -t lrange -n 1000 -q

# List outcome in the terminal 
python scripts/read_pstats.py /tmp/pyredis-out.pstats

# Visualize outcome on a webpage
snakeviz /tmp/pyredis-out.pstats
```