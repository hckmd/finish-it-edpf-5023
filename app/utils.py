import json

from app import db
from app.models import Tag, Item

class ImportResult:
    success: bool
    messages: list
    imported: int

    def __init__(self, success, messages, imported):
        self.success = success
        self.messages = messages
        self.imported = imported

def get_tag_for_name(tag_name, user_id):
    # Check if a tag with this name already exists for the user doing the import
    tag = Tag.query.filter_by(name = tag_name, user_id = user_id).first()
    if tag is None:
        # The tag doesn't exist, so needs to be created
        tag = Tag(name = tag_name, user_id = user_id)
        db.session.add(tag)
    return tag

def import_user_items(file, user_id):
    # Set up variables to keep track for import result
    success = True
    imported_count = 0
    messages = []

    # Open the file and save items in the file to the database
    import_data = json.loads(file.read())
    for item in import_data['items']:
        new_item = Item()
        new_item.title = item['title']
        new_item.status = item['status']
        new_item.priority = item['priority']
        new_item.next_steps = item['next_steps']
        new_item.barriers = item['barriers']
        new_item.notes = item['notes']
        new_item.type = item['type']
        new_item.user_id = user_id

        imported_count += 1
        db.session.add(new_item)

        for tag_name in item['tags']:
            tag = get_tag_for_name(tag_name, user_id)
            new_item.tags.append(tag)

    if success:
        db.session.commit()
    
    import_result = ImportResult(success, messages, imported_count)
    return import_result

def export_user_items(items):
    exported_items = []
    for item in items:
        # Map the values from each item to a dictionary
        item_dict = {}
        item_dict['title'] = item.title
        item_dict['status'] = item.status
        item_dict['priority'] = item.priority
        item_dict['next_steps'] = item.next_steps
        item_dict['barriers'] = item.barriers
        item_dict['notes'] = item.notes
        item_dict['type'] = item.type

        # Go through the tags and add these names as strings
        tags_list = []
        for tag in item.tags:
            tags_list.append(tag.name)
        item_dict['tags'] = tags_list

        exported_items.append(item_dict)
    
    return { 'items': exported_items }


