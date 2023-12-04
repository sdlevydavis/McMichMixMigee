def merge_sort(arr):
    if len(arr) < 2:
        return arr
    middle_index = len(arr) // 2
    left_arr = merge_sort(arr[:middle_index])
    right_arr = merge_sort(arr[middle_index:])

    return _merge(left_arr, right_arr)


def _merge(left_arr, right_arr):
    if len(left_arr) == 0:
        return left_arr

    if len(right_arr) == 0:
        return right_arr

    combined_arr = []
    left_arr_curr_index = 0
    right_arr_curr_index = 0
    while len(combined_arr) < len(left_arr) + len(right_arr):
        if left_arr[left_arr_curr_index][1] < right_arr[right_arr_curr_index][1]:
            combined_arr.append(left_arr[left_arr_curr_index])
            left_arr_curr_index += 1
        else:
            combined_arr.append(right_arr[right_arr_curr_index])
            right_arr_curr_index += 1
        if left_arr_curr_index == len(left_arr) or right_arr_curr_index == len(right_arr):
            combined_arr.extend(left_arr[left_arr_curr_index:] or right_arr[right_arr_curr_index:])
            break

    return combined_arr

# print(merge_sort([("a", 190, "sydni"), ("b", 19, "sydni"), ("a", -1, "sydni"), ("cc", 10, "d"), ("e", 1, "sydni")]))
