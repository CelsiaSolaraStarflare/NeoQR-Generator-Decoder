# Import modules
import math
import random

# Define some constants
VERSION = 10 # QR code version
MODULES = 57 # Number of modules per side
ECC_LEVEL = "L" # Error correction level
ECC_PERCENT = 7 # Error correction percentage
ECC_BLOCKS = 1 # Number of error correction blocks
ECC_WORDS = 26 # Number of error correction words per block
DATA_WORDS = 172 # Number of data words per block
TOTAL_WORDS = 198 # Total number of words per block
REMAINDER_BITS = 0 # Number of remainder bits

# Define the alphanumeric mode table
ALPHA_TABLE = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14,
    "F": 15, "G": 16, "H": 17, "I": 18, "J": 19,
    "K": 20, "L": 21, "M": 22, "N": 23, "O": 24,
    "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29,
    "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34,
    "Z": 35, " ":36 , "$" :37 , "%" :38 , "*" :39 ,
    "+" :40 , "-" :41 , "." :42 , "/" :43 , ":" :44
}

# Define the format information table
FORMAT_TABLE = {
    ("L",0):"111011111000100",
    ("L",1):"111001011110011",
    ("L",2):"111110110101010",
    ("L",3):"111100010011101",
    ("L",4):"110011000101111",
    ("L",5):"110001100011000",
    ("L",6):"110110001000001",
    ("L",7):"110100101110110",
    ("M",0):"101010000010010",
    ("M",1):"101000100100101",
    ("M",2):"101111001111100",
    ("M",3):"101101101001011",
    ("M",4):"100010111111001",
    ("M",5):"100000011001110",
    ("M",6):"100111110010111",
    ("M",7):"100101010100000",
    ("Q",0):"011010101011111",
    ("Q",1):"011000001101000",
    ("Q",2):"011111100110001",
    ("Q",3):"011101000000110",
    ("Q",4):"010010010110100",
    ("Q",5):"010000110000011",
    ("Q",6):"010111011011010",
    ("Q",7):"010101111101101",
    ("H",0):"001011010001001",
    ("H",1):"001001110111110",
    ("H",2):"001110011100111",
    ("H",3):"001100111010000",
    ("H",4):"000011101100010",
    ("H",5):"000001001010101",
    ("H",6):"000110100001100",
    ("H",7):"000100000111011"
}

# Define the generator polynomial for error correction
GENERATOR_POLY = [
    0, 251, 67, 46, 61, 118, 70, 64, 94, 32,
    45, 11, 77, 113, 195, 242, 203, 42
]

# Define the finder pattern matrix
FINDER_PATTERN = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,7]
]

# Define the alignment pattern matrix
ALIGNMENT_PATTERN = [
    [1,1,1],
    [1,-2,-2],
    [2,-2,-2]
]

# Define the alignment pattern positions for version 10
ALIGNMENT_POSITIONS = [6 ,30 ,54]

# Define the function patterns matrix
FUNCTION_PATTERNS = [[-3 for i in range(MODULES)] for j in range(MODULES)]

# Add the finder patterns to the function patterns matrix
for x in range(7):
    for y in range(7):
        FUNCTION_PATTERNS[x][y] = FINDER_PATTERN[x][y] # Top-left corner
        FUNCTION_PATTERNS[x][MODULES - y - 1] = FINDER_PATTERN[x][y] # Top-right corner
        FUNCTION_PATTERNS[MODULES - x - 1][y] = FINDER_PATTERN[x][y] # Bottom-left corner

# Add the separator patterns to the function patterns matrix
for i in range(8):
    FUNCTION_PATTERNS[i][7] = -3 # Top-left corner
    FUNCTION_PATTERNS[7][i] = -3 # Top-left corner
    FUNCTION_PATTERNS[i][MODULES - 8] = -3 # Top-right corner
    FUNCTION_PATTERNS[7][MODULES - i - 1] = -3 # Top-right corner
    FUNCTION_PATTERNS[MODULES - i - 1][7] = -3 # Bottom-left corner
    FUNCTION_PATTERNS[MODULES - 8][i] = -3 # Bottom-left corner

# Add the timing patterns to the function patterns matrix
for i in range(8 , MODULES - 8):
    FUNCTION_PATTERNS[i][6] = i % 2 # Vertical line
    FUNCTION_PATTERNS[6][i] = i % 2 # Horizontal line

# Add the alignment patterns to the function patterns matrix
for x in ALIGNMENT_POSITIONS:
    for y in ALIGNMENT_POSITIONS:
        if FUNCTION_PATTERNS[x][y] == -3: # Skip if overlaps with finder pattern
            continue
        for dx in range(-2 ,3):
            for dy in range(-2 ,3):
                # Check if x + dx and y + dy are within the range of 0 to 56
                if 0 <= x + dx < MODULES and 0 <= y + dy < MODULES:
                    # Check if dx + 2 and dy + 2 are within the range of 0 to 2
                    if 0 <= dx + 2 < len(ALIGNMENT_PATTERN) and 0 <= dy + 2 < len(ALIGNMENT_PATTERN):
                        # Assign the value
                        FUNCTION_PATTERNS[x + dx][y + dy] = ALIGNMENT_PATTERN[dx + 2][dy + 2]


# Add the dark module to the function patterns matrix
FUNCTION_PATTERNS[8][MODULES - 8 - 1] = 4

# Define a function to convert a string to a bit list
def string_to_bits(string):
    bits = []
    for char in string:
        bits.append(int(char))
    return bits

# Define a function to convert a bit list to a string
def bits_to_string(bits):
    string = ""
    for bit in bits:
        string += str(bit)
    return string

# Define a function to convert an integer to a bit list with a fixed length
def int_to_bits(integer , length):
    bits = []
    for i in range(length):
        bits.append((integer >> (length - i - 1)) & 1)
    return bits

    # Define a function to convert a bit list to an integer


def bits_to_int(bits):
    integer = 0
    for bit in bits:
        integer = (integer << 1) | bit
    return integer

    # Define a function to append a list to another list


def append_list(list1, list2):
    for item in list2:
        list1.append(item)

    # Define a function to pad a bit list with zeros to a fixed length


def pad_bits(bits, length):
    while len(bits) < length:
        bits.append(0)

    # Define a function to encode a string in alphanumeric mode


def encode_alphanumeric(string):
    # Convert the string to uppercase
    string = string.upper()
    # Check if the string is valid for alphanumeric mode
    for char in string:
        if char not in ALPHA_TABLE:
            raise ValueError("Invalid character for alphanumeric mode: " + char)
    # Initialize an empty bit list
    bits = []
    # Append the mode indicator (0010) to the bit list
    append_list(bits , [0 ,0 ,1 ,0])
    # Append the character count indicator (9 bits) to the bit list
    append_list(bits , int_to_bits(len(string) , 9))
    # Encode each pair of characters in the string
    for i in range(0 , len(string) , 2):
        # Get the first character and its value
        char1 = string[i]
        value1 = ALPHA_TABLE[char1]
        # Check if there is a second character
        if i + 1 < len(string):
            # Get the second character and its value
            char2 = string[i + 1]
            value2 = ALPHA_TABLE[char2]
            # Combine the values of the two characters (11 bits)
            value = value1 * 45 + value2
            # Append the value to the bit list
            append_list(bits , int_to_bits(value , 11))
        else:
            # Append the value of the first character (6 bits) to the bit list
            append_list(bits , int_to_bits(value1 , 6))
    # Pad the bit list with zeros until it becomes a multiple of 8
    pad_bits(bits , (len(bits) + 7) // 8 * 8)
    # Return the bit list
    return bits



def add_error_correction(bits):
    # Calculate the number of data codewords
    data_codewords = len(bits) // 8
    # Check if there are any remainder bits
    if len(bits) % 8 != 0:
        raise ValueError("Number of bits is not a multiple of 8")
    # Check if the number of data codewords is valid
    if data_codewords > DATA_WORDS:
        raise ValueError("Too many data codewords: " + str(data_codewords))
    # Pad the bit list with terminator bits (0000) if necessary
    pad_bits(bits, DATA_WORDS * 8)
    # Split the bit list into blocks of data codewords
    blocks = []
    for i in range(ECC_BLOCKS):
        block = bits[i * DATA_WORDS * 8: (i + 1) * DATA_WORDS * 8]
        blocks.append(block)
    # For each block, calculate the error correction codewords using polynomial division
    for block in blocks:
        # Convert the block into a list of coefficients
        coefficients = []
        for i in range(DATA_WORDS):
            coefficient = bits_to_int(block[i * 8: (i + 1) * 8])
            coefficients.append(coefficient)
        # Initialize an empty list of error correction codewords
        ecc_codewords = [0] * ECC_WORDS
        # For each coefficient, perform polynomial division using synthetic division algorithm
        for coefficient in coefficients:
            # Add the coefficient to the first error correction codeword
            ecc_codewords[0] ^= coefficient
            # For each error correction codeword, multiply it by the generator polynomial term and add it to the next error correction codeword
            for i in range(ECC_WORDS - 1):
                ecc_codewords[i] = ecc_codewords[i + 1] ^ (GENERATOR_POLY[i + 1] * ecc_codewords[i]) % 255
                # For the last error correction codeword, multiply it by the generator polynomial term only
            ecc_codewords[ECC_WORDS - 1] = (GENERATOR_POLY[ECC_WORDS] * ecc_codewords[ECC_WORDS - 1]) % 255
        # Convert the error correction codewords into a bit list and append it to the block
        for ecc_codeword in ecc_codewords:
            append_list(block, int_to_bits(ecc_codeword, 8))
    # Interleave the blocks and append the remainder bits to form the final codeword sequence
    codewords = []
    for i in range(TOTAL_WORDS):
        for block in blocks:
            if i < len(block) // 8:
                append_list(codewords, block[i * 8: (i + 1) * 8])
    append_list(codewords, [0] * REMAINDER_BITS)
    # Return the codeword sequence
    return codewords

    # Define a function to choose the best mask pattern for a QR code


def choose_mask(data):
    # Initialize the best score and pattern
    best_score = math.inf
    best_pattern = -1
    # For each mask pattern, calculate the penalty score
    for pattern in range(8):
        # Apply the mask pattern to the data
        masked_data = apply_mask(data, pattern)
        # Initialize the penalty score
        score = 0
        # Evaluate the first rule: adjacent modules in row/column in same color
        for i in range(MODULES):
            # Initialize the counters for rows and columns
            row_counter = 0
            column_counter = 0
            # Initialize the previous values for rows and columns
            row_previous = -1
            column_previous = -1
            for j in range(MODULES):
                # Get the current values for rows and columns
                row_current = masked_data[i][j]
                column_current = masked_data[j][i]
                # If the current value is the same as the previous value, increment the counters
                if row_current == row_previous:
                    row_counter += 1
                else:
                    # If the counter is larger than 5, add the penalty score (3 + (counter - 5))
                    if row_counter > 5:
                        score += 3 + (row_counter - 5)
                    # Reset the counter and update the previous value
                    row_counter = 1
                    row_previous = row_current

                if column_current == column_previous:
                    column_counter += 1
                else:
                    if column_counter > 5:
                        score += 3 + (column_counter - 5)
                    column_counter = 1
                    column_previous = column_current

            # Check the counters at the end of each row and column
            if row_counter > 5:
                score += 3 + (row_counter - 5)
            if column_counter > 5:
                score += 3 + (column_counter - 5)

        # Evaluate the second rule: block of modules in same color
        for i in range(MODULES - 1):
            for j in range(MODULES - 1):
                # Get the values of four adjacent modules
                value = masked_data[i][j]
                if (value == masked_data[i + 1][j] and
                        value == masked_data[i][j + 1] and
                        value == masked_data[i + 1][j + 1]):
                    # If they are all the same, add the penalty score (3)
                    score += 3

        # Evaluate the third rule: pattern with dark-light-dark ratio of 1:1:3:1:1 or vice versa in same color
        for i in range(MODULES):
            for j in range(MODULES - 6):
                # Get the values of seven adjacent modules in a row
                values = masked_data[i][j:j + 7]
                if (values[0] == values[1] and
                        values[0] != values[2] and
                        values[2] == values[3] and
                        values[2] == values[4] * 3 and
                        values[4] == values[5] and
                        values[4] != values[6]):
                    # If they match the pattern, add the penalty score (40)
                    score += 40

        for i in range(MODULES - 6):
            for j in range(MODULES):
                # Get the values of seven adjacent modules in a column
                values = [masked_data[i + k][j] for k in range(7)]
                if (values[0] == values[1] and
                        values[0] != values[2] and
                        values[2] == values[3] and
                        values[2] == values[4] * 3 and
                        values[4] == values[5] and
                        values[4] != values[6]):
                    # If they match the pattern, add the penalty score (40)
                    score += 40

                    # Evaluate the fourth rule: proportion of dark modules in entire symbol
                    # Count the number of dark modules
                dark_count = 0
                for i in range(MODULES):
                    for j in range(MODULES):
                        if masked_data[i][j] == 1:
                            dark_count += 1
                # Calculate the percentage of dark modules
                dark_percent = dark_count * 100 / (MODULES * MODULES)
                # Calculate the previous and next multiple of five
                previous_multiple = math.floor(dark_percent / 5) * 5
                next_multiple = math.ceil(dark_percent / 5) * 5
                # Calculate the penalty score based on the smaller difference (10 * difference)
                if abs(previous_multiple - 50) < abs(next_multiple - 50):
                    score += 10 * abs(previous_multiple - 50) / 5
                else:
                    score += 10 * abs(next_multiple - 50) / 5

                # Compare the score with the best score
                if score < best_score:
                    # Update the best score and pattern
                    best_score = score
                    best_pattern = pattern

                # Return the best mask pattern
            return best_pattern

            # Define a function to apply a mask pattern to a QR code
            def apply_mask(data, pattern):
                # Make a copy of the data
                masked_data = [row[:] for row in data]
                # For each module, check if it is a data or error correction module and apply the mask pattern
                for i in range(MODULES):
                    for j in range(MODULES):
                        if FUNCTION_PATTERNS[i][j] == -3:  # Skip if it is a function module
                            continue
                        # Check the mask pattern and flip the module value if necessary
                        if pattern == 0:  # (row + column) mod 2 == 0
                            if (i + j) % 2 == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 1:  # row mod 2 == 0
                            if i % 2 == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 2:  # column mod 3 == 0
                            if j % 3 == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 3:  # (row + column) mod 3 == 0
                            if (i + j) % 3 == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 4:  # (floor(row / 2) + floor(column / 3)) mod 2 == 0
                            if ((i // 2) + (j // 3)) % 2 == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 5:  # ((row * column) mod 2) + ((row * column) mod 3) == 0
                            if (((i * j) % 2) + ((i * j) % 3)) == 0:
                                masked_data[i][j] ^= 1
                        elif pattern == 6:  # (((row * column) mod 2) + ((row * column) mod 3)) mod 2 == 0
                            # Calculate the expression
                            expression = (((i * j) % 2) + ((i * j) % 3)) % 2
                            # Check if the expression is zero
                            if expression == 0:
                                # Flip the module value
                                masked_data[i][j] ^= 1
                        elif pattern == 7:  # (((row + column) mod 2) + ((row * column) mod 3)) mod 2 == 0
                            # Calculate the expression
                            expression = (((i + j) % 2) + ((i * j) % 3)) % 2
                            # Check if the expression is zero
                            if expression == 0:
                                # Flip the module value
                                masked_data[i][j] ^= 1

    # Return the masked data
    return masked_data

# Define a function to add the format and version information to a QR code
def add_info(data , pattern):
    # Make a copy of the data
    info_data = [row[:] for row in data]
    # Get the format information string based on the error correction level and mask pattern
    format_info = FORMAT_TABLE[(ECC_LEVEL , pattern)]
    # Add the format information to the function patterns matrix
    for i in range(15):
        # Get the bit value
        bit = int(format_info[i])
        # Get the coordinates
        if i < 6: # First six bits
            x1 = i
            y1 = 8
            x2 = 8
            y2 = MODULES - i - 1
        elif i < 8: # Next two bits
            x1 = i + 1
            y1 = 8
            x2 = 8
            y2 = MODULES - i - 1 - 1
        else: # Last seven bits
            x1 = MODULES - 15 + i
            y1 = 8
            x2 = 8
            y2 = 14 - i

        # If the module is not a function module, flip it according to the bit value
        if FUNCTION_PATTERNS[x1][y1] != -3:
            info_data[x1][y1] ^= bit

        if FUNCTION_PATTERNS[x2][y2] != -3:
            info_data[x2][y2] ^= bit

    # Return the info data
    return info_data

# Define a function to place the codewords into a QR code matrix
def place_codewords(data , codewords):
    # Make a copy of the data
    codeword_data = [row[:] for row in data]
    # Initialize the current bit index and direction flag
    bit_index = 0
    up_flag = True
    # Loop through each column pair from right to left
    for x in range(MODULES - 1 ,0 ,-2):
        # Skip the timing pattern column
        if x == 6:
            x -= 1
        # Loop through each row from bottom to top or top to bottom depending on the direction flag
        for y in range(MODULES - 1 ,-1 ,-1) if up_flag else range(MODULES):
            # Loop through each column in the column pair from right to left
            for dx in range(2):
                # Get the current module value
                value = codeword_data[x - dx][y]
                # If the module is not a function module, fill it with a codeword bit
                if value == -3:
                    continue
                else:
                    # Get the current codeword bit
                    bit = codewords[bit_index]
                    # Set the module value according to the codeword bit
                    codeword_data[x - dx][y] = bit
                    # Increment the bit index
                    bit_index += 1
                    # If all bits are placed, return the codeword data
                    if bit_index == len(codewords):
                        return codeword_data
        # Flip the direction flag
        up_flag = not up_flag
    # Return the codeword data
    return codeword_data

# Define a function to render a QR code matrix as an image using PIL library
def render_image(data):
    # Import PIL library
    from PIL import Image , ImageDraw
    # Define the scale and border size
    scale = 10
    border = 4
    # Create a new image with white background
    image = Image.new("RGB" , ((MODULES + border * 2) * scale , (MODULES + border * 2) * scale) , (255 ,255 ,255))
    # Create a draw object
    draw = ImageDraw.Draw(image)
    # Loop through each module and draw it on the image
    for x in range(MODULES):
        for y in range(MODULES):
            # Get the module value
            value = data[x][y]
            # If the module is dark, draw a black square
            if value == 1:
                draw.rectangle(
                    [(x + border) * scale , (y + border) * scale , (x + border + 1) * scale - 1 , (y + border + 1) * scale - 1] ,
                    fill = (0 ,0 ,0)
                )
    # Return the image
    return image

# Define the data to be encoded
data = "HELLO WORLD"

# Encode the data in alphanumeric mode
bits = encode_alphanumeric(data)

# Add error correction codewords to the bit list
codewords = add_error_correction(bits)

# Choose the best mask pattern for the QR code
pattern = choose_mask(codewords)

# Apply the mask pattern to the QR code
masked_data = apply_mask(codewords , pattern)

# Add the format and version information to the QR code
info_data = add_info(masked_data , pattern)

# Place the codewords into the QR code matrix
codeword_data = place_codewords(info_data , codewords)

# Render the QR code matrix as an image
image = render_image(codeword_data)

# Save the image as a PNG file
image.save("qrcode.png")
