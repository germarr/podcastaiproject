import argparse


# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Add the --type argument
parser.add_argument('--isyoutube', type=str, required=True, help="The type of processing to apply")

# Parse the arguments
args = parser.parse_args()

# Access the input and type arguments
urlOfTheVideo = args.input
processing_type = args.isyoutube

print("URL of the Video:", urlOfTheVideo)
print("Processing Type:", processing_type)