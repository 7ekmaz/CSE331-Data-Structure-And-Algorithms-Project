def tag_extraction(line):
    # Find the first tag  
    start = line.find('<')
    end = line.find('>', start)
    tag_content = "" 
    if start != -1 and end != -1 and start < end - 1:
        tag_content = line[start + 1:end].strip()  # Extract content between '<' and '>'
        if tag_content[0] == "/":
            return False,tag_content[1:]
    return True,tag_content 
    #opening flag , tag content as return value


with open('trial.xml', 'r') as input:
    lines = input.readlines()
    with open('output.xml', 'w') as output:
        first_tag = True
        indent = 0
        #to remove all spaces in the files to apply the function
        for i in range(len(lines)):
            line = lines[i].strip() + "\n"
            prev_line = lines[i-1].strip() + "\n"
            #extraction of all the tags in the file
            status ,tag = tag_extraction(line)
            #to check if it's opening tag
            if "<" + tag + ">" in line:
                if first_tag:
                    output.writelines(line)
                    #(no spaces needed for the first tag)
                    first_tag = False
                    continue
                #checking if the opening and closing tages are in the same line
                if "<" + tag + ">" and "</" + tag + ">" in line:
                    output.writelines(" " * (indent + 4) + line.replace(" ",""))
                    continue
                previous_op, previous_tag = tag_extraction(prev_line)
                #checking on having ~(op and closing tages in the same line)&(having the previous tag to be closing tag)
                if (not (("<" + previous_tag + ">" in prev_line and "</" + previous_tag + ">" in prev_line) )) and ("</" + previous_tag + ">" in prev_line):
                    output.writelines(" " * indent + line)
                    continue
                indent+=4
                output.writelines(" " * indent + line)
                continue
            #checking if it's closing tag
            if "</" + tag + ">" in line:
                prev_op, prev_tag = tag_extraction(prev_line)
                #checking on having two closing tages consecutively
                if not status and not prev_op:
                    indent-= 4
                    output.writelines(" " * indent + line)
                    continue
                output.writelines(" " * indent + line) 
            else:
                if line == "\n":
                    continue
                j = 0
                temp_flag = False
                output.writelines(" " * (indent+4))
                #to write the content between any two tags
                while lines[i][j] != "\n":
                    #for each 100 charcter , make a new line
                    if j % 100 == 0 and temp_flag:
                        output.writelines("\n")
                        output.writelines(" " * (indent+4))
                    output.writelines(lines[i][j])
                    j+=1
                    temp_flag = True
                output.writelines("\n")     

# Time Complexity Analysis:
# Let:
# - L: Length of each line in the XML file
# - N: Number of lines in the XML file

# 1. strip() Function:
# - The strip() function is called for each line.
# - For each line, it iterates through the entire string of length L.
# - Time Complexity: O(N * L)

# 2. tag_extraction() Function:
# - This function is called once per line.
# - Inside the function:
#   - find() has a complexity of O(L)
#   - strip() contributes another O(L)
# - Time Complexity: O(N * L)

# 3. Writing Output:
# - Writing each line to the output file involves processing the entire line.
# - Time Complexity: O(N * L)

# 4. replace() Function:
# - The replace() function removes spaces from each line.
# - It scans through the entire line of length L.
# - Time Complexity: O(N * L)

# Overall Time Complexity:
# - Combining all the operations: O(N * L) + O(N * L) + O(N * L) + O(N * L)
# - Overall: O(N * L)

# Conclusion:
# - The runtime is proportional to both the number of lines (N) and the average length of each line (L).

    