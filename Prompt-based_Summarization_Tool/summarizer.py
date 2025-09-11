import argparse
from transformers import pipeline

def summarize_text(text, model_name="facebook/bart-large-cnn", max_length=130, min_length=30, do_sample=False):
    summarizer = pipeline("summarization", model=model_name)
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)
    return summary[0]['summary_text']

def main():
    parser = argparse.ArgumentParser(description=" Local Summarizer using Transformers")
    parser.add_argument("file", help="Path to input text file")
    parser.add_argument("--model", default="facebook/bart-large-cnn", help="Model name (default: bart-large-cnn)")
    parser.add_argument("--max_length", type=int, default=130, help="Max tokens in summary")
    parser.add_argument("--min_length", type=int, default=30, help="Min tokens in summary")
    parser.add_argument("--sample", action="store_true", help="Enable sampling (for creativity)")
    parser.add_argument("--output", help="Path to save the summary as a text file")

    args = parser.parse_args()

    # Read input
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(" File not found.")
        return

    print("\n Summarizing using", args.model)
    summary = summarize_text(
        text=text,
        model_name=args.model,
        max_length=args.max_length,
        min_length=args.min_length,
        do_sample=args.sample
    )

    print("\n Summary:\n")
    print(summary)

    #  Save output if path provided
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"\n Summary saved to {args.output}")
        except Exception as e:
            print(f" Error saving summary: {e}")

if __name__ == "__main__":
    main()
