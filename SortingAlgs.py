def quick_sort(id_points_name_list):
    length = len(id_points_name_list)

    if length <= 1:
        return id_points_name_list

    pivot = id_points_name_list.pop()
    low = []
    high = []
    for triple in id_points_name_list:
        if triple[1] > pivot[1]:
            high.append(triple)
        else:
            low.append(triple)
    return quick_sort(low) + [pivot] + quick_sort(high)


#print(quick_sort([("a", 190, "sydni"), ("b", 19, "sydni"), ("a", -1, "sydni"), ("cc", 10, "d"), ("e", 1, "sydni")]))




