from typing import List


def int_array_to_bytes_n(int_arr: List[int], n: int = 32) -> List[bytes]:
    return [int(i).to_bytes(n, 'big') for i in int_arr]


def split_by(arr: List[dict], by: str):
    result_arr = []
    for element in arr:
        result_arr.append(element[by])
    return result_arr
