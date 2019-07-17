# Client-Server Software ver. 2: Documentation

## Ports
```
64295 - Alice's file server
64296 - Bob's file server
29083 - Bob's socket server
```

## Algorithm
```
Alice: connect to Bob's socket server
Alice: generate parity
Alice: send parity to Bob
Bob: get parity
Bob: generate badblocks
Bob: shuffle key
Bob: send badblocks
Alice: get badblocks
Alice: wipe badblocks
Alice: shuffle key
```