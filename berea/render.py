# TODO: Adjustable line length? (BSB wraps lines at 40-43 characters)
def list_multiline_verse(verse):
    lines = []
    
    next_line = verse
    
    while len(next_line) > 80:
        # Split the verse if there's more than one line left
        space_split = next_line[:79].rfind(' ')
        lines.append(next_line[:space_split])
        next_line = next_line[space_split:].lstrip()
            
    # Append last line of verse
    lines.append(next_line)

    return lines


# TODO: Replace consecutive spaces with single spaces
# TODO: Input line length?
def verses_to_wall_of_text(verse_records, verse_numbers=False): 
    verses = ''
    for row in verse_records:
        # Skip empty verses so orphaned verse numbers or extra whitespace
        # is not displayed
        if not row['text']:
            continue
        if verse_numbers:
            verses += str(row['verse']) + ' '
        
        verses += row['text'].strip() + ' '
    
    verses_split = list_multiline_verse(verses)
    wrapped_verses = '\n'.join(verses_split)
    
    return wrapped_verses


def create_link_label(translation, book, chapter=None, verse=None):
    """Creates a link label, eg. `Isaiah 14:12-20`
    """
    label = book
    
    if chapter:
        label += f" {chapter}"
        
        if verse:
            label += f":{verse}"
    
    label += f" {translation}"
    
    return label


# TODO: Print paragraphs from Bible format
def create_markdown_excerpt(bible_client, verse_records, book, chapter, verse):
    """Generate Markdown excerpt for the verses.

    Args:
        verse_records (_type_): _description_
        params (_type_): _description_
    """
    verse_text = verses_to_wall_of_text(verse_records)
    book = bible_client.get_book_from_abbreviation(book)
    output = (
        '###\n'
        '\n______________________________________________________________________\n'
        f"\n{verse_text}"
        f"\n([{create_link_label(bible_client.translation, book, chapter, verse)}]"
        f"({bible_client.create_link(book, chapter, verse)}))\n"
        '\n______________________________________________________________________'
    )
    return output
    

# TODO: Return paragraphs from Bible format
def render_reference_results(bible_client, format, verse_records, verse_numbers=False, book=None, chapter=None, verse=None):
    """_summary_

    Args:
        bible_client (BibleClient): Used to create the link and label if needed.
        format (_type_): _description_
        verse_records (_type_): _description_
        verse_numbers (bool, optional): _description_. Defaults to False.
        book (_type_, optional): _description_. Defaults to None.
        chapter (_type_, optional): _description_. Defaults to None.
        verse (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    match format: 
        case 'txt':
            return verses_to_wall_of_text(verse_records, verse_numbers)

        case 'md':
            return create_markdown_excerpt(bible_client, verse_records, book, chapter, verse)


def render_search_results(
    bible_client,
    verse_records,
    phrase,
    testament=None,
    book=None,
    chapter=None
):
    if chapter:
        book = bible_client.get_book_from_abbreviation(book)
        output = f"{len(verse_records)} occurrences of '{phrase}' in {book} {chapter} ({bible_client.translation}):\n___\n"
        for verse in verse_records:
            output += f"\n{verse['book']} {verse['chapter']}:{verse['verse']}:\n{verse['text']}\n___\n"
        
    elif book:
        book = bible_client.get_book_from_abbreviation(book)
        output = f"{len(verse_records)} occurrences of '{phrase}' in {book} ({bible_client.translation}):\n___\n"
        for verse in verse_records:
            output += f"\n{verse['book']} {verse['chapter']}:{verse['verse']}:\n{verse['text']}\n___\n"
            
    elif testament:
        testament = 'New Testament' if testament == 'nt' else 'Old Testament'
        output = f"{len(verse_records)} occurrences of '{phrase}' in the {testament} ({bible_client.translation}):\n___\n"
        for verse in verse_records:
            output += f"\n{verse['book']} {verse['chapter']}:{verse['verse']}:\n{verse['text']}\n___\n"
            
    else:
        output = f"{len(verse_records)} occurrences of '{phrase}' in the {bible_client.translation} Bible:\n___\n"
        for verse in verse_records:
            output += f"\n{verse['book']} {verse['chapter']}:{verse['verse']}:\n{verse['text']}\n___\n"

    return output
