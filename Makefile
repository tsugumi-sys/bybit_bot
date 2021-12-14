.PHONY run_predict_api:
run_predict_api:
	cd predict_api/src && poetry run uvicorn app:app --port 8000 --reload

.PHONY run_bot:
run_bot:
	cd bot/src && poetry run uvicorn app:app --port 5000 --reload