import itertools
import random


# Function to generate combinations for a single line of the pattern
def generate_combinations_for_line(pattern_part):
    combinations = [""]

    if pattern_part == "(S|T)(U|V)W*Y+24":
        st_choices = ["S", "T"]
        uv_choices = ["U", "V"]
        w_repeats = ["W" * i for i in range(6)]
        y_repeats = ["Y" * i for i in range(1, 6)]

        new_combinations = []
        for st, uv, w, y in itertools.product(st_choices, uv_choices, w_repeats, y_repeats):
            new_combinations.append(st + uv + w + y + "24")
        return new_combinations

    elif pattern_part == "L(M|N)O^3P*Q(2|3)":
        mn_choices = ["M", "N"]
        o_part = "OOO"
        p_repeats = ["P" * i for i in range(6)]
        num_choices = ["2", "3"]

        new_combinations = []
        for mn, p, num in itertools.product(mn_choices, p_repeats, num_choices):
            new_combinations.append("L" + mn + o_part + p + "Q" + num)
        return new_combinations

    elif pattern_part == "R*S(T|U|V)W(X|Y|Z)^2":
        r_repeats = ["R" * i for i in range(6)]
        tuv_choices = ["T", "U", "V"]
        xyz_choices = ["XX", "YY", "ZZ"]

        new_combinations = []
        for r, tuv, xyz in itertools.product(r_repeats, tuv_choices, xyz_choices):
            new_combinations.append(r + "S" + tuv + "W" + xyz)
        return new_combinations

    return combinations


# Function to show the sequence of processing for a given combination
def show_processing_sequence(pattern_part, combination):
    print(f"\nProcessing sequence for combination '{combination}' in pattern '{pattern_part}':")
    current_string = ""
    step = 1

    if pattern_part == "(S|T)(U|V)W*Y+24":
        # Step 1: (S|T)
        char = combination[0]
        current_string += char
        print(f"Step {step}: Process '(S|T)'. Chose '{char}'. Current string: '{current_string}'")
        step += 1

        # Step 2: (U|V)
        char = combination[1]
        current_string += char
        print(f"Step {step}: Process '(U|V)'. Chose '{char}'. Current string: '{current_string}'")
        step += 1

        # Step 3: W* (0 to 5 times)
        w_count = 0
        pos = 2
        while pos < len(combination) and combination[pos] == 'W':
            w_count += 1
            pos += 1
        current_string += "W" * w_count
        print(f"Step {step}: Process 'W*'. Chose {w_count} W's. Current string: '{current_string}'")
        step += 1

        # Step 4: Y+ (1 to 5 times)
        y_count = 0
        while pos < len(combination) and combination[pos] == 'Y':
            y_count += 1
            pos += 1
        current_string += "Y" * y_count
        print(f"Step {step}: Process 'Y+'. Chose {y_count} Y's. Current string: '{current_string}'")
        step += 1

        # Step 5: 24 (literal)
        current_string += "24"
        print(f"Step {step}: Process '24'. Added literal '24'. Current string: '{current_string}'")

    elif pattern_part == "L(M|N)O^3P*Q(2|3)":
        # Step 1: L (literal)
        current_string += "L"
        print(f"Step {step}: Process 'L'. Added literal 'L'. Current string: '{current_string}'")
        step += 1

        # Step 2: (M|N)
        char = combination[1]
        current_string += char
        print(f"Step {step}: Process '(M|N)'. Chose '{char}'. Current string: '{current_string}'")
        step += 1

        # Step 3: O^3 (exactly 3 O's)
        current_string += "OOO"
        print(f"Step {step}: Process 'O^3'. Added exactly 3 O's. Current string: '{current_string}'")
        step += 1

        # Step 4: P* (0 to 5 times)
        p_count = 0
        pos = 5  # After L(M|N)OOO
        while pos < len(combination) and combination[pos] == 'P':
            p_count += 1
            pos += 1
        current_string += "P" * p_count
        print(f"Step {step}: Process 'P*'. Chose {p_count} P's. Current string: '{current_string}'")
        step += 1

        # Step 5: Q (literal)
        current_string += "Q"
        print(f"Step {step}: Process 'Q'. Added literal 'Q'. Current string: '{current_string}'")
        step += 1

        # Step 6: (2|3)
        char = combination[-1]
        current_string += char
        print(f"Step {step}: Process '(2|3)'. Chose '{char}'. Current string: '{current_string}'")

    elif pattern_part == "R*S(T|U|V)W(X|Y|Z)^2":
        # Step 1: R* (0 to 5 times)
        r_count = 0
        pos = 0
        while pos < len(combination) and combination[pos] == 'R':
            r_count += 1
            pos += 1
        current_string += "R" * r_count
        print(f"Step {step}: Process 'R*'. Chose {r_count} R's. Current string: '{current_string}'")
        step += 1

        # Step 2: S (literal)
        current_string += "S"
        print(f"Step {step}: Process 'S'. Added literal 'S'. Current string: '{current_string}'")
        step += 1

        # Step 3: (T|U|V)
        char = combination[pos + 1]
        current_string += char
        print(f"Step {step}: Process '(T|U|V)'. Chose '{char}'. Current string: '{current_string}'")
        step += 1

        # Step 4: W (literal)
        current_string += "W"
        print(f"Step {step}: Process 'W'. Added literal 'W'. Current string: '{current_string}'")
        step += 1

        # Step 5: (X|Y|Z)^2 (XX, YY, or ZZ)
        last_two = combination[-2:]
        current_string += last_two
        print(f"Step {step}: Process '(X|Y|Z)^2'. Chose '{last_two}'. Current string: '{current_string}'")

    print(f"Final string: '{current_string}'")


# Generate combinations for each line
line1 = "(S|T)(U|V)W*Y+24"
line2 = "L(M|N)O^3P*Q(2|3)"
line3 = "R*S(T|U|V)W(X|Y|Z)^2"

combinations1 = generate_combinations_for_line(line1)
combinations2 = generate_combinations_for_line(line2)
combinations3 = generate_combinations_for_line(line3)

lines_and_combinations = [
    (line1, combinations1),
    (line2, combinations2),
    (line3, combinations3)
]

for line, combinations in lines_and_combinations:
    print(f"Examples for Line: {line}")
    random_combinations = random.sample(combinations, 5)
    for i, combo in enumerate(random_combinations):
        print(f"{i + 1}. {combo}")
    show_processing_sequence(line, random_combinations[0])
    print()