import random
import time
import matplotlib.pyplot as plt


def generate_random_dna(length):
    nucleotides = ['A', 'G', 'C', 'T']
    random_string = ''.join(random.choice(nucleotides) for _ in range(length))
    return random_string


def insert_sequence_randomly(original, query):
    
    insert_index = random.randint(0, len(original))  
    new_string = original[:insert_index] + query + original[insert_index:]
    return new_string, insert_index


def search_query_in_target_randomly(target_with_query, query):
    checked = [i for i in range(len(target_with_query))]
    found = False
    operations = 0 

    while not found and checked:
        operations += 1

        start_index = random.sample(checked, 1)[0]
        checked.remove(start_index)  

        if target_with_query[start_index] == query[0]:
            
            match = True
            for i in range(1, len(query)):
                if (start_index + i >= len(target_with_query)) or (target_with_query[start_index + i] != query[i]):
                    match = False
                    break

            if match:
                found = True
                return True, operations, start_index  

    return False, operations, -1 

#Boyer-Moore Algorithm
def preprocess_bad_character_rule(pattern):
    bad_char_shift = {}
    for i in range(len(pattern)):
        bad_char_shift[pattern[i]] = i 
    return bad_char_shift

def preprocess_good_suffix_rule(pattern):
    m = len(pattern)
    good_suffix_shift = [0] * (m + 1)
    border_pos = [0] * (m + 1)

    i = m
    j = m + 1
    border_pos[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix_shift[j] == 0:
                good_suffix_shift[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(m + 1):
        if good_suffix_shift[i] == 0:
            good_suffix_shift[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix_shift

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    operations = 0
    
    if m == 0:
        return 0, operations, -1
    
    bad_char_shift = preprocess_bad_character_rule(pattern)
    good_suffix_shift = preprocess_good_suffix_rule(pattern)
    
    s = 0

    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            operations += 1
            j -= 1

        if j < 0:
            return s, operations, s
        else:
            operations += 1
            bad_char_shift_val = bad_char_shift.get(text[s + j], -1)
            shift_bc = j - bad_char_shift_val
            shift_gs = good_suffix_shift[j + 1]
            s += max(shift_bc, shift_gs)

    return -1, operations, -1


def run_test_cases_and_plot():
    
    target_lengths = [10000,50000,100000,200000] 
    query_lengths = [10,20,40,80,160]

    
    random_sampling_operations = []
    boyer_moore_operations = []
    labels = []

    for target_length in target_lengths:
        for query_length in query_lengths:
            
            target = generate_random_dna(target_length)

            query = generate_random_dna(query_length)

            target_with_query, query_index = insert_sequence_randomly(target, query)

            _, random_operations, _ = search_query_in_target_randomly(target_with_query, query)

            _, bm_operations, _ = boyer_moore_search(target_with_query, query)

            random_sampling_operations.append(random_operations)
            boyer_moore_operations.append(bm_operations)
            labels.append(f'Target: {target_length}, Query: {query_length}')

    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(labels))

    
    ax.bar(x, random_sampling_operations, width=0.4, label='LDSS', align='center', color='skyblue')
    ax.bar([i + 0.4 for i in x], boyer_moore_operations, width=0.4, label='Boyer-Moore', align='center', color='orange')

    
    ax.set_xlabel('Test Scenarios')
    ax.set_ylabel('Number of Operations')
    ax.set_title('LDSS vs. Boyer-Moore: Number of Operations')
    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.show()

# Run the test cases and plot the results:
run_test_cases_and_plot()
