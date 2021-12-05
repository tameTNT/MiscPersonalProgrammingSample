number_list = []
for i in range(256):
    number_list.append(i)
  
current_position = 0
skip_size = 0
lengths = "206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3"
lengths_ascii = []
for character in lengths:
    lengths_ascii.append(ord(character))
lengths_ascii += [17, 31, 73, 47, 23]


def circ_list(index):
    circ_index = index % len(number_list)
    return circ_index
   
     
for i in range(64):
    for length in lengths_ascii:
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
    
densehash = []
for i in range(16):
    current_sparsehash = 0
    for number in number_list[i*16:(i+1)*16]:
        current_sparsehash ^= number
    densehash.append(current_sparsehash)

hexadecimal_densehash = [hex(x) for x in densehash]
for hex_value in range(len(hexadecimal_densehash)):
    hexadecimal_densehash[hex_value] = hexadecimal_densehash[hex_value][2:]

final_string = "".join(hexadecimal_densehash)
print(final_string)