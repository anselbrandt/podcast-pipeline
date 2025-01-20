import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Label speaker segments with speaker names."
    )
    parser.add_argument(
        "input_dir", type=str, help="Directory containing input and wavs folder"
    )
    parser.add_argument(
        "output_dir", type=str, help="Directory to save labeled transcripts."
    )

    args = parser.parse_args()

    print(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
