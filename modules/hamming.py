import numpy as np
import time as t
import struct
import pickle
from bitarray import bitarray

from modules.matrices import gen_matrix
from modules.shuffle import gen_shuffle

debug = False


# len_nes in bits
def hamming_parity(fname_in, fname_out, power, len_nes=0):
    gen_m = gen_matrix(power)[0]

    ba_key = bitarray()
    with open(fname_in, "rb") as file_in:
        if len_nes:
            ba_key.fromfile(file_in, len_nes // 8)
        else:
            ba_key.fromfile(file_in)

    ba_parity = bitarray()
    len_block_data = 2 ** power - 1 - power

    for i in range(len_nes // len_block_data):
        block_data = np.matrix(
            [
                int(j)
                for j in list(ba_key[i * len_block_data : (i + 1) * len_block_data])
            ]
        )
        if debug:
            print(block_data)

        block_parity = (
            (np.dot(gen_m, block_data.transpose()) % 2).transpose().tolist()[0]
        )
        block_parity.append(
            (
                sum(block_parity)
                + sum(ba_key[i * len_block_data : (i + 1) * len_block_data])
            )
            % 2
        )
        # print('PStar', block_parity[-1])

        # print(ba_parity, block_parity)
        ba_parity += block_parity
        # if debug: print(ba_parity)

    with open(fname_out, "wb") as file_out:
        ba_parity.tofile(file_out)


# len_nes in blocks
def hamming_correct(
    fname_key,
    fname_parity,
    fname_kout,
    fname_bad,
    power,
    len_nes=0,
    len_nes_par=0,
    drop_bad=False,
):
    syn_m = gen_matrix(power)[1]
    len_block_data = 2 ** power - 1 - power

    ba_key = bitarray()
    with open(fname_key, "rb") as file_in:
        if len_nes:
            ba_key.fromfile(file_in, len_nes * len_block_data // 8)
        else:
            ba_key.fromfile(file_in)

    ba_parity = bitarray()
    with open(fname_parity, "rb") as file_in:
        if len_nes_par:
            ba_parity.fromfile(file_in, len_nes_par * (power + 1) // 8)
        else:
            ba_parity.fromfile(file_in)

    if not len_nes:
        len_nes = len(ba_key) // len_block_data
    ba_result = bitarray()
    bad_blocks = []

    for i in range(len_nes):
        block_data = ba_key[i * len_block_data : (i + 1) * len_block_data]
        block_parity = ba_parity[i * (power + 1) : (i + 1) * (power + 1)]
        if debug:
            print(block_data, block_parity)
        block_merged = [-1 for i in range(2 ** power)]
        for j in range(power + 1):
            # if power == 4: print(i, len(block_merged), block_merged, j, 2 ** j - 1)
            block_merged[2 ** j - 1] = int(block_parity[j])
        for j in range(len(block_merged)):
            if len(block_data):
                if block_merged[j] == -1:
                    block_merged[j] = int(block_data[0])
                    block_data.pop(0)
        if debug:
            print(f"#{i} - block: {block_merged}")
        block_syndrome = (
            np.dot(np.matrix(block_merged), syn_m.transpose()) % 2
        ).tolist()[0]
        if debug and sum(block_syndrome):
            print(f"#{i} - block: {block_merged}")
            print(f"syn: {block_syndrome}")
        if debug:
            print(f"syn: {block_syndrome}")

        if drop_bad and (block_syndrome[0] != (sum(block_syndrome) > 0)):
            if debug:
                print(f"Bad block!")
            bad_blocks.append(i)
            continue

        block_syndrome.pop(0)

        num = 0
        for j in range(len(block_syndrome)):
            num += block_syndrome[-1 - j] * 2 ** j

        block_merged[num - 1] ^= 1
        for j in range(power, -1, -1):
            block_merged.pop(2 ** j - 1)
        ba_result += block_merged

        if debug:
            print(block_merged)

    with open(fname_kout, "wb") as file_out:
        ba_result.tofile(file_out)

    with open(fname_bad, "wb") as file_bad:
        pickle.dump(bad_blocks, file_bad)


def hamming_wipe(fname_in, fname_out, fname_bad, power, len_nes):
    len_block_data = 2 ** power - 1 - power

    ba_key = bitarray()
    with open(fname_in, "rb") as file_in:
        if len_nes:
            ba_key.fromfile(file_in, len_nes * len_block_data // 8)
        else:
            ba_key.fromfile(file_in)

    ba_out = bitarray()

    with open(fname_bad, "rb") as file_bad:
        bad_blocks = pickle.load(file_bad)

    temp = [True for i in range(len(ba_key))]
    for i in bad_blocks[::-1]:
        # print(i)
        for j in range(i * len_block_data, (i + 1) * len_block_data):
            try:
                temp[j] = False
            except:
                pass  # print('Fail', len(temp), j)

    for i in range(len(temp)):
        if temp[i]:
            ba_out.append(ba_key[i])
    # print(len(ba_key))

    with open(fname_out, "wb") as file_out:
        ba_out.tofile(file_out)


# len_nes in blocks
def shuffle(fname_in, fname_out, len_block, len_nes):
    ba_in = bitarray()
    with open(fname_in, "rb") as file_in:
        if len_nes:
            ba_in.fromfile(file_in, len_nes * len_block // 8)
        else:
            ba_in.fromfile(file_in)

    if not len_nes:
        len_nes = len(ba_in) // len_block

    for i in range(len_nes):
        ba_in[i * len_block : (i + 1) * len_block] = bitarray(
            gen_shuffle(ba_in[i * len_block : (i + 1) * len_block])
        )
        # print(f'Shuffled #{i}!')

    with open(fname_out, "wb") as file_out:
        ba_in.tofile(file_out)


class NoCorrectionException(Exception):
    pass
