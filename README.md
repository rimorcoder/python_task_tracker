# Task Tracker w/Python
 
https://roadmap.sh/projects/task-tracker

This Python script allows you to manage a list of tasks using commands like `add`, `update`, `delete`, and `list`. The tasks are stored in a JSON file and each task has attributes like `description`, `status`, `createdAt`, and `updatedAt`. 

## Features

- **Add** new tasks with a description and status.
- **Update** the description or status of an existing task.
- **Delete** a task by its ID.
- **List** all tasks, filter by ID, or filter by status.
- Tasks are stored with timestamps for creation (`createdAt`) and last update (`updatedAt`) in UTC.

## Prerequisites

- Python 3.9 or above
- No external dependencies

## Usage

### 1. Add a New Task

You can add a new task by providing a description and an optional status. The default status is `todo`.

```bash
python script.py add "Your task description"
```
##### Example
```bash
python script.py add "Finish the report" --status in-progress

# Output: Added item: {'id': 1, 'description': 'Finish the report', 'status': 'in-progress', 'createdAt': '2024-09-10T12:34:56+00:00', 'updatedAt': '2024-09-10T12:34:56+00:00'}
```
### 2. Update an Existing Task

You can update the description and/or status of a task by its ID. The `updatedAt` field will be updated to the current UTC time.

```bash
python script.py update <task_id> --description "Updated description" --status done
```
##### Example
```bash
python script.py update 1 --description "Finish the report draft" --status done
# Output: Updated description for item 1: Finish the report draft
# Output: Updated status for item 1: done
# Output: Updated item 1
```
### 3. Delete a Task

You can delete a task by its ID.

```bash
python script.py delete <task_id>
```
##### Example
```bash
python script.py delete 1
# Output: Deleted item with ID 1
```
### 4. List Tasks

You can list all tasks, filter by ID, or filter by status.

##### List All Tasks:
```bash
python script.py list
```
##### List by ID:
```bash
python script.py list --id <task_id>
```
##### List by Status:
```bash
python script.py list --status in-progress
```
##### Example
```bash
python script.py list --status done
# Output: {'id': 1, 'description': 'Finish the report draft', 'status': 'done', 'createdAt': '2024-09-10T12:34:56+00:00', 'updatedAt': '2024-09-10T12:36:00+00:00'}
```

## Task Schema
Each task is stored as a JSON object with the following schema:
```bash
{
    "id": int,
    "description": string,
    "status": string,  # Allowed values: "todo", "in-progress", "done"
    "createdAt": string,  # UTC timestamp of when the task was created
    "updatedAt": string   # UTC timestamp of when the task was last updated
}
```

## Valid Status Values
The following status values are allowed for tasks:
- `todo`
- `in-progress`
- `done`
Any other status will result in an error.

## File Storage
The tasks are stored in a JSON file (`items.json`) in the current directory. It is created if it doesnt exist. 