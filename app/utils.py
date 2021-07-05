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


