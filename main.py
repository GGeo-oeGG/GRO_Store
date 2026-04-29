def main(n):
    current_number = 1
    count = 0

    while count < n:
        for _ in range(current_number):
            if count >= n:
                break
            return current_number
            count += 1
        current_number += 1


def generate_sequence(n):
    result = []
    current_number = 1
    while len(result) < n:
        result.extend([current_number] * current_number)
        current_number += 1
    return result[:n]


if __name__ == "__main__":
    main(10)
    print()
    print(" ".join(map(str, generate_sequence(50))))
