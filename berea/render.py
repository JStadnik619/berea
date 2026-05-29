import re

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


# TODO: Input line length?
def verses_to_wall_of_text(verse_records, verse_numbers=False, format='txt'): 
    verses = ''
    for row in verse_records:
        # Skip empty verses so orphaned verse numbers or extra whitespace
        # is not displayed
        if not row['text']:
            continue
        if verse_numbers:
            if format == 'md':
                verses += f"<sup>{str(row['verse'])}</sup> "
            else:
                verses += str(row['verse']) + ' '
        
        verses += row['text'].strip() + ' '
    
    verses_split = list_multiline_verse(verses)
    wrapped_verses = '\n'.join(verses_split)
    
    return wrapped_verses


def get_indent(string):
    return (len(string) - len(string.lstrip())) * ' '


# This assumes that the last verse has a trailing newline
def wrap_long_lines(verses):
    """Replace the last space before the 80th character 
    in a line longer than 80 characters with a newline.
    """
    wrapped_verses = ''
    current_pos = 0
    next_pos = 0

    while next_pos < len(verses):
        # Line length is the distance to the next newline character
        next_pos = verses.find('\n', current_pos)
        if next_pos == -1:
            break
        line_length = next_pos - current_pos
        
        if line_length > 80:
            indent = get_indent(verses[current_pos:next_pos])
            # Replace the last space before the 80th character with a newline
            last_space_pos = next_pos
            # Add as many newlines between current and next positions as needed
            while current_pos <= next_pos:
                while (last_space_pos - current_pos) > 80:
                    last_space_pos = verses.rfind(" ", current_pos, last_space_pos)
                
                if last_space_pos != -1:
                    line = verses[current_pos:last_space_pos]
                    # Remove extra whitespace in the middle of the line
                    line = re.sub(r'(?<=\S)\s+(?=\S)', ' ', line)
                    # Add a space after the following characters are followed
                    # by an alphabet character: . , ! ? ; :
                    line = re.sub(
                        r'([.,!?;:]+[\'"’”)\]]?)(?![\s\d\W]|$)',
                        r'\1 ',
                        line
                    )
                    if not line.startswith(indent):
                        wrapped_verses += indent
                    wrapped_verses += line + "\n"
                    # Shift the current and last space positions forward
                    current_pos = last_space_pos + 1
                    last_space_pos = next_pos
                    continue
                
                # Add the last piece of this line
                else:
                    wrapped_verses += indent + verses[current_pos:next_pos + 1]
                    break
        
        else:
            wrapped_verses += verses[current_pos:next_pos + 1]

        # Proceed to the next line
        current_pos = next_pos + 1
        continue

    return wrapped_verses


# TODO: Rendering cross references/footnotes will require special handling
# eg, [^1] or [^a] for markdown, anchors for HTML
# superscript alphabetical characters for stdout?
# TODO: Handle section headings, subtitles, acrostic letters
def render_markup(markup_records, verse_numbers=False, format='txt'):
    PARAGRAPH_MARKERS = ['m', 'pmo', 'sc', 'p', 'pc',]
    verses = ''
    
    if verse_numbers:
        verse_number = 0
        contiguous_verse = False
        for record in markup_records:
            verse_number_str = ''
            
            if not isinstance(record['verse'], int):
                continue
            
            if record['verse'] > verse_number:
                verse_number = record['verse']
                verse_number_str = ''
                match format:
                    case 'txt':
                        verse_number_str = str(verse_number) + ' '
                    case 'md':
                        verse_number_str = f"<sup>{verse_number}</sup>" + ' '
            
            if record['marker'] in PARAGRAPH_MARKERS and record['text']:
                if not contiguous_verse:
                    verses += verse_number_str + record['text']
                    contiguous_verse = True
                else:
                    verses += ' ' + verse_number_str + record['text']
            # TODO: Do adds ever occur at the start of the verse?
            elif record['marker'] == 'add':
                verses += ' ' + record['text']
            elif record['marker'] == 'li1':
                verses += '  ' + verse_number_str + record['text']
            elif record['marker'] == 'li2':
                verses += '    ' + verse_number_str + record['text']
            elif record['marker'] == 'q1' and record['text']:
                verses += '\n' + verse_number_str + record['text']
            elif record['marker'] == 'q2' and record['text']:
                verses += '\n' + '  ' + verse_number_str + record['text']
            elif record['marker'] == 'b':
                verses += '\n\n'
                contiguous_verse = False
            else:
                continue
        verses = verses
    
    else: 
        for record in markup_records:
            if record['marker'] in PARAGRAPH_MARKERS:
                verses += record['text']
            elif record['marker'] in ['add', 'tl']:
                verses += ' ' + record['text']
            elif record['marker'] == 'li1':
                verses += '  ' + record['text']
            elif record['marker'] == 'li2':
                verses += '    ' + record['text']
            elif record['marker'] in ['q1', 'qr'] and record['text']:
                verses += '\n' + record['text']
            elif record['marker'] == 'q2' and record['text']:
                verses += '\n' + '  ' + record['text']
            elif record['marker'] == 'q3' and record['text']:
                verses += '\n' + '    ' + record['text']
            elif record['marker'] == 'b':
                verses += '\n\n'
            else:
                continue
    
    # Add trailing newline in case last verse doesn't have one
    wrapped_verses = wrap_long_lines(verses + '\n')
    # Remove consecutive blank lines
    wrapped_verses = re.sub(r'\n\s*\n+', '\n\n', wrapped_verses)
    return wrapped_verses.strip()


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


# TODO: Toggle wall of text (or replace pre tags with lines)
def create_markdown_excerpt(bible_client, markup_records, book, chapter, verse, verse_numbers=False):
    """Generate Markdown excerpt for the verses.

    Args:
        markup_records (_type_): _description_
        params (_type_): _description_
    """
    passage = render_markup(markup_records, verse_numbers, 'md')
    book = bible_client.get_book_from_abbreviation(book)
    output = (
        f"[{create_link_label(bible_client.translation, book, chapter, verse)}]"
        f"({bible_client.create_link(book, chapter, verse)}):\n"
        '<pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">\n'
        f"{passage}\n"
        '</pre>'
    )
    return output


def render_reference_results(bible_client, format, markup_records, verse_numbers=False, book=None, chapter=None, verse=None):
    """_summary_

    Args:
        bible_client (BibleClient): Used to create the link and label if needed.
        format (_type_): _description_
        markup_records (_type_): _description_
        verse_numbers (bool, optional): _description_. Defaults to False.
        book (_type_, optional): _description_. Defaults to None.
        chapter (_type_, optional): _description_. Defaults to None.
        verse (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    match format: 
        case 'txt':
            return render_markup(markup_records,  verse_numbers)

        case 'md':
            # TODO: Toggle wall of text
            return create_markdown_excerpt(bible_client, markup_records, book, chapter, verse, verse_numbers)


 # TODO: Output txt, markdown table, csv format
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
    
    # Replace highlight bold tags with ANSI escape codes
    output = output.replace('<b>', '\033[1m')
    output = output.replace('</b>', '\033[0m')
    return output
