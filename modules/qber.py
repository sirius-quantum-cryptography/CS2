__author__ = "AfoninZ"

def calc(file_alice, file_bob):
    ba_alice = bitarray()
    with open(file_alice, "rb") as filek_in:
        ba_alice.fromfile(filek_in)

    ba_bob = bitarray()
    with open(file_bob, "rb") as filek_in:
        ba_bob.fromfile(filek_in)

    print(len(ba_alice), len(ba_bob))
    len_nes = min(len(ba_alice), len(ba_bob))
    errs = 0

    for i in range(len_nes):
        if i % 102400 == 0:
            print(f"{i} - {i / (len_nes) * 100}%", end="\r")
        errs += ba_alice[i] ^ ba_bob[i]
    print(errs, len_nes)
    print(f"BER: {errs / len_nes * 100}%")
