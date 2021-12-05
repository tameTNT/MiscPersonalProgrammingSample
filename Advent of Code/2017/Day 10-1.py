number_list = []
for i in range(256):
    number_list.append(i)
  
current_position = 0
skip_size = 0
lengths = [206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3]


def circ_list(index):
    circ_index = index % len(number_list)
    return circ_index
        

for length in lengths:
    if current_position + length < len(number_list):
        segment = number_list[current_position:circ_list(current_position + length)]
        reversed_segment = segment[::-1]
        number_list[current_position:circ_list(current_position + length)] = reversed_segment

    else:
        offset = len(number_list) - current_position
        beginning_section_index = length - offset
        segment = number_list[current_position:]
        segment += number_list[:beginning_section_index]
        segment = segment[::-1]
        number_list[current_position:] = segment[:offset]
        number_list[:beginning_section_index] = segment[offset:]

    current_position = circ_list(current_position + length + skip_size)
    skip_size += 1
    
print(number_list[0] * number_list[1])