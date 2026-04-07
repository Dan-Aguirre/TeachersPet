import sqlite3
import json
import urllib.request

DATASETS = {
    "easy": "https://raw.githubusercontent.com/RamonKaspar/MathDataset-ElementarySchool/main/data/II_WordProblems/wordProblems_100.json",
    "medium": "https://raw.githubusercontent.com/RamonKaspar/MathDataset-ElementarySchool/main/data/I_Arithmetic/arithmetic_100.json",
    "hard": "https://raw.githubusercontent.com/RamonKaspar/MathDataset-ElementarySchool/main/data/III_Geometry/geometry_100.json"
}

def fetch_and_import():
    con = sqlite3.connect("game.db")
    
    print("Clearing existing questions...")
    con.execute("DELETE FROM questions")
    con.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    con.commit()
    
    for difficulty, url in DATASETS.items():
        print(f"Pulling {difficulty} dataset...")
        
        try:
            with urllib.request.urlopen(url) as response:
                lines = response.read().decode('utf-8').strip().split('\n')
                
                for line in lines:
                    if not line.strip():
                        continue
                        
                    item = json.loads(line)
                    
                    con.execute(
                        "INSERT INTO questions (question, answer, difficulty) VALUES (?, ?, ?)",
                        (item["question"], float(item["answer"]), difficulty)
                    )
        except Exception as e:
            print(f"Failed on {difficulty}: {e}")
    
    con.commit()
    con.close()
    print("Database updated.")

if __name__ == "__main__":
    fetch_and_import()