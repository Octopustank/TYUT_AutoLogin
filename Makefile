init:
	poetry install
clean:
	-rm -rf poetry.lock .venv
run:
	poetry run python3 ./main.py
