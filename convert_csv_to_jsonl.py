import csv
import json

with open('RAGCodePiece.csv', 'r', newline='', encoding='utf-8') as fin:
    reader = csv.reader(fin)
    next(reader)  # skip header
    with open('rag_code_piece.jsonl', 'w', encoding='utf-8') as fout:
        for desc, code in reader:
            fout.write(json.dumps({'prompt': desc, 'correct_code': code}) + '\n') 