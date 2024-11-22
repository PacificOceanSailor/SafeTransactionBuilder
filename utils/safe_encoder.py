def encode_raw_tx(raw_tx: dict):
    value = raw_tx["value"]
    to = raw_tx["to"]
    data = raw_tx["data"][2:]
    operation = "00"  # zero for call, one for delegatecall
    return operation + to[2:] + str(value).zfill(64) + hex(int(len(data) / 2))[2:].zfill(64) + data.zfill(64)
