
''' 
                             COMMENT FROM THE AUTHORS 
    This part is for test purposes only. A person tasked with connecting the project parts
    should remove this main function and devise his own test file.
'''
def main():
    operation = sys.argv[1]
    input_file = sys.argv[3]
    output_file = sys.argv[5]

    if operation == 'compress':
        if input_file.endswith('.xml'):
            compress_xml(input_file, output_file)
        else:
            print("Unsupported file format. Please use .xml files.")
    elif operation == 'decompress':
        if input_file.endswith('.comp'):
            if output_file.endswith('.xml'):
                decompress_xml(input_file, output_file)
            else:
                print("Unsupported file format for output.")
    else:
        print("Invalid operation. Use 'compress' or 'decompress'.")


if __name__ == "__main__":
    main()

