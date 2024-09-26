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