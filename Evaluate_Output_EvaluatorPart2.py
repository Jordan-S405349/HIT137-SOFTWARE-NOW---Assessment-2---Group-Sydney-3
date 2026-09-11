import sys
from Evaluator import evaluate_file

if __name__ == "__main__":
    # Usage:
    #   python Evaluate_Output_EvaluatorPart2.py
    #   python Evaluate_Output_EvaluatorPart2.py my_input.txt
    #   python Evaluate_Output_EvaluatorPart2.py my_input.txt my_output.txt
    input_path = sys.argv[1] if len(sys.argv) > 1 else "sample_input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    results = evaluate_file(input_path, output_path)

    for entry in results:
        print("Input: " + entry["Input"])
        print("Tree: " + entry["Tree"])
        print("Tokens: " + entry["Tokens"])
        print("Result: " + entry["Result"])
        print()

    print(f"Done. Read {len(results)} expression(s) from '{input_path}', wrote results to '{output_path}'.")
