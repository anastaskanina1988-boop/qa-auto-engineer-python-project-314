start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

test:
	APP_BASE_URL=http://localhost:5173 uv run pytest -v tests/

test-login:
	APP_BASE_URL=http://localhost:5173 uv run pytest -v tests/test_authentication.py::test_successful_login

test-logout:
	APP_BASE_URL=http://localhost:5173 uv run pytest -v tests/test_authentication.py::test_login_and_logout