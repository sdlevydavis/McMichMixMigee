def _heapifyDown(scores, size, rt):
    while rt * 2 + 2 < size:
        if scores[rt][1] < scores[rt * 2 + 1][1] > scores[rt * 2 + 2][1]:
            (scores[rt], scores[rt * 2 + 1]) = (scores[rt * 2 + 1], scores[rt])
            rt = rt * 2 + 1
        elif rt * 2 + 2 < size and scores[rt][1] < scores[rt * 2 + 2][1]:
            (scores[rt], scores[rt * 2 + 2]) = (scores[rt * 2 + 2], scores[rt])
            rt = rt * 2 + 2
        else:
            break
    if rt * 2 + 1 < size and scores[rt][1] < scores[rt * 2 + 1][1]:
        (scores[rt], scores[rt * 2 + 1]) = (scores[rt * 2 + 1], scores[rt])


def heapSort(scores):
    for i in range(len(scores) // 2 - 1, -1, -1):
        _heapifyDown(scores, len(scores), i)

    for j in range(len(scores) - 1, 0, -1):
        (scores[0], scores[j]) = (scores[j], scores[0])
        _heapifyDown(scores, j, 0)


# merge sort inspired by discussion slides
def merge_sort(arr):
    if len(arr) < 2:
        return arr
    middle_index = len(arr) // 2
    left_arr = merge_sort(arr[:middle_index])
    right_arr = merge_sort(arr[middle_index:])

    return _merge(left_arr, right_arr)


def _merge(left_arr, right_arr):
    combined_arr = []

    while len(left_arr) > 0 and len(right_arr) > 0:
        if left_arr[0][1] <= right_arr[0][1]:
            combined_arr.append(left_arr[0])
            left_arr = left_arr[1:]
        else:
            combined_arr.append(left_arr[0])
            right_arr = right_arr[1:]

    return combined_arr
