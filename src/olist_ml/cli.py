import argparse

import pandas as pd

from src.olist_ml.inference import predict


def main():
    """Run late-delivery prediction from the command line."""

    parser = argparse.ArgumentParser(
        description="Predict whether an Olist order will be delivered late."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to a CSV file containing order data.",
    )

    args = parser.parse_args()

    # Read input order data
    df = pd.read_csv(args.input)

    # Run inference
    results = predict(df)

    # Display results
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()