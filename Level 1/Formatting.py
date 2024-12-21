import sys


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

def formatting(input_file):
    with open(input_file, 'r') as input:
        lines = input.readlines()
        
        result = []
        first_tag = True
        indent = 0
        for i in range(len(lines)):
            line = lines[i].strip() 
            prev_line = lines[i-1].strip() 
            #extraction of all the tags in the file
            if line == "":
                continue
            status ,tag = tag_extraction(line)
            #to check if it's opening tag
            if "<" + tag + ">" in line:
                if first_tag:
                    result.append(line)
                    #(no spaces needed for the first tag)
                    first_tag = False
                    continue
                #checking if the opening and closing tages are in the same line
                if "<" + tag + ">" and "</" + tag + ">" in line:
                    result.append(" " * (indent + 4) + line)
                    continue
                previous_op, previous_tag = tag_extraction(prev_line)
                #checking on having ~(op and closing tages in the same line)&(having the previous tag to be closing tag)
                if (not (("<" + previous_tag + ">" in prev_line and "</" + previous_tag + ">" in prev_line) )) and ("</" + previous_tag + ">" in prev_line): 
                    result.append(" " * indent + line)
                    continue
                indent+=4
                result.append(" " * indent + line)
                continue
            #checking if it's closing tag
            if "</" + tag + ">" in line:
                prev_op, prev_tag = tag_extraction(prev_line)
                #checking on having two closing tages consecutively
                if not status and not prev_op:
                    indent-= 4
                    result.append(" " * indent + line)
                    continue
                result.append(" " * indent + line)
            else:
                if line == "\n":
                    continue
                j = 0
                string = ""
                string+=(" " * (indent+4))
                while lines[i][j] != "\n":
                    string += lines[i][j]
                    j+=1
                result.append(string)   
                      
    return result                

def main():
    x = formatting("trial.xml")  
    for s in x:
        print(s)
    if len(sys.argv) < 3:
        print("Usage:")
        print("  xml_editor format -i input_file.xml -o output_file.xml")
        sys.exit(1)


    if sys.argv[1] == "format":
        if len(sys.argv) == 6 and sys.argv[2] == "-i" and sys.argv[4] == "-o":
            input_file = sys.argv[3]
            formatting(input_file)
        else:
            print("Usage: xml_editor compress -i input_file.xml -o output_file.xml")
            sys.exit(1)



if __name__ == "__main__":
    main()    

