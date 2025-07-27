# LangaraCourseWatcher

This is a project to collect, collate, and serve information about courses at Langara through one service.
- Hosts an API with the courses database at [api.langaracourses.ca](api.langaracourses.ca)
- Updates data from the latest Langara semester every hour.
- Updates transfer and other Langara data every day.


### Hosting:
This service will work best with docker-compose.

Make sure that you provide a volume (`course_watcher_db:/database`) for the image.

### Development:
Create and enter a virtual environment:
- `python -m venv .venv`
- `.venv/scripts/activate`

Install requirements:
- `pip install -r requirements-api.txt`
- `pip install -r requirements-backend.txt`

Install chromium for playwright: 
- `playwright install --with-deps chromium`.

Run the api with `uvicorn api:app`.

Run the backend with `python main.py`.