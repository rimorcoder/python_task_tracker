import argparse
import json
import os
import datetime

# Path to the JSON file
JSON_FILE = 'items.json'

# Allowed status values
ALLOWED_STATUSES = ['todo', 'done', 'in-progress']

# Load items from the JSON file
def load_items():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return []

# Save items to the JSON file
def save_items(items):
    with open(JSON_FILE, 'w') as file:
        json.dump(items, file, indent=4)

# Helper function to find an item by ID
def find_item_by_id(items, item_id):
    return next((item for item in items if item['id'] == item_id), None)

# Validate status
def validate_status(status):
    if status not in ALLOWED_STATUSES:
        print(f"Error: Invalid status '{status}'. Allowed statuses are: {', '.join(ALLOWED_STATUSES)}.")
        return False
    return True

# Get the current time in UTC (timezone-aware)
def current_utc_time():
    return datetime.datetime.now(datetime.UTC).isoformat()  # ISO 8601 format with UTC time

# Initialize the parser
parser = argparse.ArgumentParser(description="A script to manage items with commands: add, update, delete, list.")

# Add commands (subparsers for each action)
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Add command
add_parser = subparsers.add_parser('add', help='Add a new item')
add_parser.add_argument('description', type=str, help='The description of the item')
add_parser.add_argument('--status', type=str, help=f'The status of the item ({", ".join(ALLOWED_STATUSES)}). Default is "todo"', default='todo')

# Update command
update_parser = subparsers.add_parser('update', help='Update an existing item\'s description or status')
update_parser.add_argument('id', type=int, help='The ID of the item to update')
update_parser.add_argument('--description', type=str, help='The new description for the item', required=False)
update_parser.add_argument('--status', type=str, help=f'The new status for the item ({", ".join(ALLOWED_STATUSES)})', required=False)

# Delete command
delete_parser = subparsers.add_parser('delete', help='Delete an item')
delete_parser.add_argument('id', type=int, help='The ID of the item to delete')

# List command
list_parser = subparsers.add_parser('list', help='List all items, or filter by ID or status')
list_parser.add_argument('--id', type=int, help='Filter by item ID', required=False)
list_parser.add_argument('--status', type=str, help=f'Filter by item status ({", ".join(ALLOWED_STATUSES)})', required=False)

# Parse the arguments
args = parser.parse_args()

# Load existing items
items = load_items()

# Functionality based on the command
if args.command == "add":
    # Validate status
    if not validate_status(args.status):
        exit(1)

    # Add new item with auto-increment ID, current UTC createdAt and updatedAt
    new_item = {
        "id": len(items) + 1,  # Simple auto-increment based on list size
        "description": args.description,
        "status": args.status,
        "createdAt": current_utc_time(),  # Set creation time to current UTC time
        "updatedAt": current_utc_time()   # Initially, updatedAt is the same as createdAt
    }
    items.append(new_item)
    save_items(items)
    print(f"Added item: {new_item}")
    
elif args.command == "update":
    # Find item by ID
    item = find_item_by_id(items, args.id)
    if item:
        # Update description if provided
        if args.description:
            item['description'] = args.description
            print(f"Updated description for item {args.id}: {item['description']}")
        
        # Update status if provided and valid
        if args.status:
            if not validate_status(args.status):
                exit(1)
            item['status'] = args.status
            print(f"Updated status for item {args.id}: {item['status']}")
        
        # Update updatedAt to current UTC time
        item['updatedAt'] = current_utc_time()
        save_items(items)
        print(f"Updated item {args.id}")
    else:
        print(f"Item with ID {args.id} not found.")
        
elif args.command == "delete":
    # Find and delete item by ID
    item = find_item_by_id(items, args.id)
    if item:
        items.remove(item)
        save_items(items)
        print(f"Deleted item with ID {args.id}")
    else:
        print(f"Item with ID {args.id} not found.")
        
elif args.command == "list":
    # List by ID if provided
    if args.id is not None:
        item = find_item_by_id(items, args.id)
        if item:
            print(item)
        else:
            print(f"Item with ID {args.id} not found.")
    
    # List by status if provided
    elif args.status is not None:
        if validate_status(args.status):
            filtered_items = [item for item in items if item['status'] == args.status]
            if filtered_items:
                for item in filtered_items:
                    print(item)
            else:
                print(f"No items found with status '{args.status}'.")
    
    # List all items
    else:
        if items:
            for item in items:
                print(item)
        else:
            print("No items to list.")
        
else:
    parser.print_help()
