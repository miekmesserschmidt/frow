import re


def extract_first_st_num(s):
    st_num_regex = re.compile(r"u\d{8}")

    if not (found := st_num_regex.search(s)):
        raise ValueError(f"{s} has no st_number")

    return found.group(0)

