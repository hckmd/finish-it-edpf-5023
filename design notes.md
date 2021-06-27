# Finish it: EDPF5023 Sample Project

## Design Notes

### Brief

*Finish It* is a webapp to help me keep track of the *books* and *courses* that I have started (or that I am planning to start) and need to finish.

Unlike a todo list app, this webapp won't involve small to-do items as I have a tool I already use for those kind of tasks that should be completed in the short term. 
The main purpose of this app is to identify books and courses that may take days/weeks to complete and that are likely to be useful for my longer-term goals.

The main information about the books and courses that will be stored in the app will be their title, their current status (for example: *started* and *completed*), how much I want to prioritise completing them, the next steps I need to take to progress further with them, and any barriers to completing them. 
Details that might be in a book collection or course catalog app, such as the book genre or the date/s that a course runs, will not be essential for this app as I do not need this information.
However, I want to be able to create and assign 'tags' on the different books and courses, which will help me categorise these items when I want to prioritise learning/reading in a particular topic.
For example, I could create a tag for *Statistics*, which I'd tag the courses and books related to Statistics with.

I want to be able to tag the items with multiple tags. For example, a book about Statistics with Python could be tagged with both *Statistics* and *Python*.
The app will allow me to select a tag from a list of tags in the app and see all the books and courses with that tag. 

### Assumptions

Some assumptions and items that are out of scope are discussed below.

There won't be a table of course categories or book genres, tags can be used by the user to categorise items instead.

For now, priorities and statuses of the different items will be hardcoded, rather than in separate tables.

Each user will be able to create and modify their own tags, these won't be system-wide tags.

To simplify deletion of users, deletion of users will only be able to be done when they have no tags or items (books or courses) attached to them. This will be checked through the app, rather than the database level. Trying to delete users without this check will error because of foreign key constraints.

### Gold plating

Some features and functionality that would be nice to include but that are low priority are listed below:

- Fields on the Item table with dates (modified, created). These could be useful for sorting or presenting items but, in this case, I'll not have them to keep the data model simple
- A user interface with some client-side features (for example, creating tags when creating a new book / course). For simplicitly, I'll stick to using synchronous server-side requests
- Pagination on tables of the different items (server-side or client-side)
- Colour coding of tags, these could just be a single colour for now but could be stored in the Tag table

## Data Model

This section has sub-sections for each of the entities in the data model. 
This has been created to help in the scoping and design of the app, the most updated and comprehensive version is likely to be in the *models.py* file.

### User

An entity to store the users in the app.
Users can log into the app and keep track of the items they have started / completed or need to complete.

For simplicity, there will be two roles in the app: a normal role and an administrator role and a flag will be used to indicate the role of the user.
The normal role will be able to create, edit and delete their items and tags. 
The administrator role will have the same permissions as the normal role and will also be able to add and remove users.

| Name	 | Type | Description |
|-|-|-|
| id | Integer | Primary key |
| username | String |  |
| email | String | |
| password_hash | String | |
| is_adminstrator | Boolean | |

### Item

An entity that has the fields that are common to both *books* and *courses*. 
Those entities both inherit from this entity.

| Name  | Type | Description |
|-|-|-| 
| id | Integer | Primary key |
| title | String | |
| status | String | |
| priority | String | |
| next_steps | String | Optional |
| barriers | String | Optional |
| notes | String | Optional |
| user_id | Integer | Foreign key to User table |

### Book

An entity to represent *books* in the app.

| Name  | Type | Description |
|-|-|-| 
| authors | String | Optional |

### Course

An entity to represent *courses* in the app.

| Name  | Type | Description |
|-|-|-| 
| url | String | Optional |

### Tag

| Name	 | Type | Description |
|-|-|-|
| id | Integer | |
| name | String | |
| user_id | Integer | Foreign key to User table |

### ItemTag

| Name	 | Type | Description |
|-|-|-|
| id | Integer | |
| item_id | Integer | Foreign key to Item table |
| tag_id | Integer | Foreign key to Tag table |

# User Interface

## Navigation items

Navigation items:
- Home (Items ordered by priority and not complete)
- By Tag (Different tags with grouping by tags)
- Books 
- Courses
- Tags
- Users (only available to administrator roles)

## Milestone 1 Views

- Home (with navigation, list of items)
- List of books
- Add a book to the list
- Succesfully added a book to the list