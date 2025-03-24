import random

# Limit for repetition
MAX_REPEAT = 5

# Superscript map
SUPERSCRIPT_MAP = {
    "²": 2,
    "³": 3,
}

def parse_regex(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]

        if char == "(":
            end = i + 1
            depth = 1
            while end < len(expression) and depth > 0:
                if expression[end] == "(":
                    depth += 1
                elif expression[end] == ")":
                    depth -= 1
                end += 1
            group_content = expression[i + 1:end - 1]
            options = group_content.split("|")
            token = ('choice', options)
            i = end

        elif char in SUPERSCRIPT_MAP:
            prev = tokens.pop()
            count = SUPERSCRIPT_MAP[char]
            token = ('repeat', prev, count, count)
            i += 1

        elif char == '*':
            prev = tokens.pop()
            token = ('repeat', prev, 0, MAX_REPEAT)
            i += 1

        elif char == '+':
            prev = tokens.pop()
            token = ('repeat', prev, 1, MAX_REPEAT)
            i += 1

        elif char.isspace():
            i += 1
            continue

        else:
            token = ('literal', char)
            i += 1

        tokens.append(token)
    return tokens

def generate_from_token(token):
    if token[0] == 'literal':
        return token[1]
    elif token[0] == 'choice':
        return random.choice(token[1])
    elif token[0] == 'repeat':
        _, inner_token, min_r, max_r = token
        repeat_count = random.randint(min_r, max_r)
        return ''.join(generate_from_token(inner_token) for _ in range(repeat_count))

def generate_string(expression):
    tokens = parse_regex(expression)
    return ''.join(generate_from_token(token) for token in tokens)

# Input regex list
regex_list = [
    "(S|T)(U|V)w*y+24",
    "L(M|N)000p*Q(2|3)",
    "R*S(T|U|V)w(x|y|z)²"
]

# Show processing breakdown
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


regex_pairs = [
    ("(S|T)(U|V)w*y+24", "(S|T)(U|V)W*Y+24"),
    ("L(M|N)000p*Q(2|3)", "L(M|N)O^3P*Q(2|3)"),
    ("R*S(T|U|V)w(x|y|z)²", "R*S(T|U|V)W(X|Y|Z)^2")
]

for pattern, breakdown_pattern in regex_pairs:
    print(f"\n--- Generating for: {pattern} ---")
    for i in range(3):
        combo = generate_string(pattern)
        print(f"{i + 1}. Generated: {combo}")
    # Use one example for breakdown
    example = generate_string(pattern).upper()  # convert to uppercase for matching breakdown logic
    show_processing_sequence(breakdown_pattern, example)