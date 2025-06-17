import pandas as pd
import re
from flashtext import KeywordProcessor


class PrivacyFilter:
    """
    A class to remove personal information like phone numbers, emails, postal codes, and dates from text.
    """

    def __init__(self):
        self.keyword_processor = KeywordProcessor()

    def remove_phone_numbers(self, text: str) -> str:
        patterns = [
            r"\+\d{1,3}[- ]?\d{1,4}[- ]?\d{1,4}[- ]?\d{1,4}",  # e.g. +31 612 345 678
            r"\(?0\)?\d{1}[- ]?\d{8}",                         # e.g. (0)6-12345678
            r"\(?31\)?\d{9}",                                  # e.g. (31)612345678
            r"\d{2}[- ]?\d{8}",                                # e.g. 06-12345678
            r"https://wa.me/\d+"                              # WhatsApp links
        ]
        for pattern in patterns:
            text = re.sub(pattern, "<PHONE>", text)
        return text

    def remove_dates(self, text: str) -> str:
        text = re.sub(r"\d{2}[- /.]\d{2}[- /.]\d{,4}", "<DATE>", text)
        text = re.sub(
            r"(\d{1,2}[^\w]{,2}(januari|februari|maart|april|mei|juni|juli|augustus|"
            r"september|oktober|november|december)([- /.]{,2}(\d{4}|\d{2})){,1})(?P<n>\D)(?![^<]*>)",
            "<DATE>", text)
        text = re.sub(
            r"(\d{1,2}[^\w]{,2}(jan|feb|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec)"
            r"([- /.]{,2}(\d{4}|\d{2})){,1})(?P<n>\D)(?![^<]*>)",
            "<DATE>", text)
        return text

    def remove_email(self, text: str) -> str:
        return re.sub(r"[\w\.-]+@[\w\.-]+\.[a-z]{2,6}", "<EMAIL>", text, flags=re.IGNORECASE)

    def remove_postal_codes(self, text: str) -> str:
        return re.sub(r"[0-9]{4}[ ]?[A-Z]{2}([ ,.:;])", r"<POSTALCODE>\1", text)

    def filter(self, text: str) -> str:
        text = self.remove_phone_numbers(text)
        text = self.remove_email(text)
        text = self.remove_postal_codes(text)
        text = self.remove_dates(text)
        return text


def filter_file(input_file: str, output_file: str):
    """
    Applies the PrivacyFilter to a CSV file and saves the result.
    Assumes the first column should be preserved without modification.
    """
    df = pd.read_csv(input_file, delimiter=';')
    filter_instance = PrivacyFilter()
    df_filtered = df.iloc[:, 1:].map(lambda x: filter_instance.filter(str(x)))
    df_filtered.insert(0, df.columns[0], df.iloc[:, 0])
    df_filtered.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Example usage — replace with your own paths or remove in final version
    input_path = "<YOUR_INPUT_PATH>.csv"      # e.g. "data/dataset_raw.csv"
    output_path = "<YOUR_OUTPUT_PATH>.csv"    # e.g. "data/dataset_cleaned.csv"
    filter_file(input_path, output_path)
