from pathlib import Path

def test_project_files_exist():
    assert Path("config.json").exists()
    assert Path("sql/01_create_tables.sql").exists()
    assert Path("src/main.py").exists()
