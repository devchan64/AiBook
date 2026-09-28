"""Create fictional grouped observations for P3-4.2; not operational data."""
import csv
from pathlib import Path

OUTPUT = Path(__file__).with_name('p3_4_2_split_log.csv')
LABELS = [1, 0, 1, 0, 1, 0, 0, 1]
OFFSETS = [0.0, 0.2, -0.1]


def main():
    with OUTPUT.open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(['event_id', 'second', 'flow', 'review_needed'])
        for index, label in enumerate(LABELS):
            for second in range(18):
                writer.writerow([
                    chr(ord('A') + index), second,
                    f'{10 + 20 * index + OFFSETS[second % 3]:.1f}', label,
                ])


if __name__ == '__main__':
    main()
