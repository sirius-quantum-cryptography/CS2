__authors__ = ["AfoninZ", "mashed-potatoes"]

from bitarray import bitarray

def calc_ber(logger, file_alice='./data_alice/alice.bin', file_bob='./data_bob/bob.bin') -> float:
    ba_alice = bitarray()
    with open(file_alice, "rb") as f:
        ba_alice.fromfile(f)

    ba_bob = bitarray()
    with open(file_bob, "rb") as f:
        ba_bob.fromfile(f)

    len_nes = min(len(ba_alice), len(ba_bob))
    errs = 0

    for i in range(len_nes):
        if i % 102400 == 0:
            logger.proc("Calculating BER", points=min(4, int(i / len_nes * 5)))
        errs += ba_alice[i] ^ ba_bob[i]
    logger.ok()
    logger.info(f"Errors: {errs} in {len_nes}")
    return errs / len_nes * 100
