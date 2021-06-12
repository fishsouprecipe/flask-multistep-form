def is_dunder(s: str) -> bool:
    return (
        len(s) > 4 and
        s[:2] == s[-2:] == '__' and
        s[2] != '_' and
        s[-3] != '_'
    )


def camel_case_to_snake_case(s: str) -> str:
    if not s:
        return ''

    last_pos = pos = 0

    words = []

    for pos, char in enumerate(s):
        if pos == 0:
            continue

        if char.isupper():
            words.append(s[last_pos:pos])
            last_pos = pos

    words.append(s[last_pos:pos + 1])

    return '_'.join(map(str.lower, words))
