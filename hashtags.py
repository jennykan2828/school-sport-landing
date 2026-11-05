hashtags_dict = {"Peter": {"cake", "rice"},
            "Mary": {"cake", "apple", "orange"},
            "Frankie": {"rice", "orange"}}

def get_menu():
    choice = '0'
    while choice not in "12345678X":
        print("Hashtags menu")
        print("1. List all the persons")
        print("2. List all hashtags")
        print("3. Input a person and list a person's hastags")
        print("4. Add/update a person's hashtags... in one sentence")
        print("5. Delete a person")
        print("6. Input a hashtag and list all the people")
        print("7. Input multiple hashtag and list all the people that has all of them.")
        print("8. Input multiple hashtag and list all the people that has any of them.")
        print("X. Quit the program")
        choice = input("Your choice ===> ").strip().upper()
    return choice

def list_persons():
    print(', '.join(hashtags_dict.keys()))
    return

def list_hashtags():    
    for tags in hashtags_dict.values():
        print(', '.join(tags))
    return 

def person_has_tag():
    person = input('Enter a person: ')
    if person in hashtags_dict:
        print(', '.join(hashtags_dict[person]))
    else:
        print('Person not found')
    return

def add_person_hashtags():
    person = input('Enter a person: ')
    hashtags_input = input('Enter hashtags (separated by comma): ')
    
    new_tags = {tag.strip() for tag in hashtags_input.split(',')}
    
    if person in hashtags_dict:
        hashtags_dict[person].update(new_tags)
    else:
        hashtags_dict[person] = new_tags
    print(f"Updated successfully! {person}'s tags are now: {', '.join(hashtags_dict[person])}")

# 5. Delete a person
def delete_person():
    person = input('Enter a person to delete: ').strip()
    if person in hashtags_dict:
        del hashtags_dict[person]
        print(f"Successfully deleted {person} from the system.")
    else:
        print("Person not found.")

# 6. Input a hashtag and list all the people
def search_single_hashtag():
    search_tag = input('Enter a hashtag to search: ').strip()
    matches = []
    
    for person, tags in hashtags_dict.items():
        if search_tag in tags:
            matches.append(person)
            
    if matches:
        print(f"People with #{search_tag}: {', '.join(matches)}")
    else:
        print(f"Nobody has the hashtag #{search_tag}.")

# 7. Input multiple hashtags (ALL)
def search_all_hashtags():
    tags_input = input('Enter multiple hashtags (separated by comma): ')
    search_tags = {tag.strip() for tag in tags_input.split(',')}
    matches = []
    
    for person, tags in hashtags_dict.items():
        # Check if all search_tags exist inside the person's tags
        if search_tags.issubset(tags):
            matches.append(person)
            
    if matches:
        print(f"People who have ALL these tags: {', '.join(matches)}")
    else:
        print("No matches found with ALL of those tags.")

# 8. Input multiple hashtags (ANY)
def search_any_hashtags():
    tags_input = input('Enter multiple hashtags (separated by comma): ')
    search_tags = {tag.strip() for tag in tags_input.split(',')}
    matches = []
    
    for person, tags in hashtags_dict.items():
        # Check if there is any intersection (common elements) between the sets
        if search_tags & tags:
            matches.append(person)
            
    if matches:
        print(f"People who have ANY of these tags: {', '.join(matches)}")
    else:
        print("No matches found with any of those tags.")


choice = get_menu()
while choice != 'X':
    match choice:
        case '1':
            list_persons()            
        case '2':
            list_hashtags()
        case '3':
            person_has_tag()
        case '4':
            add_person_hashtags()
        case '5':
            delete_person()
        case '6':
            search_single_hashtag()
        case '7':
            search_all_hashtags()
        case '8': 
            search_any_hashtags()
        case _:
            print('Invalid choice') 

    choice=get_menu()
print('Bye bye')