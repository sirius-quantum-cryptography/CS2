# Client-Server Software ver. 2: Documentation

## How-to install
```bash
git clone https://github.com/sirius-quantum-cryptography/CS2
cd CS2
pip3 install -r requirements.txt
export cs2_mode=alice # or bob
export cs2_remote_host=192.168.0.1 # or any other host
```

## Running

If you're using environment:
```bash
python -m CS2
```

Or just use arguments:

```bash
python __main__.py alice
```

## Ports
```
64295 - Alice's file server
64296 - Bob's file server
```

## Algorithm
```
Alice: connect to Bob
Alice: generate parity
Alice: send parity to Bob
Bob: get parity
Bob: generate badblocks
Bob: shuffle key
Bob: send badblocks to Alice
Alice: get badblocks
Alice: wipe badblocks
Alice: shuffle key
```
