import re


def remove_emoji(caption):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', caption)


def remove_marks(caption):
    # links
    regex = r"((((https?):((//)|(\\\\)))|(www))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
    text = re.sub(regex, "", caption)

    # mentions and hashtags
    regex = r"[@#][\w-]+"
    return re.sub(regex, "", text)


def remove_misplaced_punctuation(caption):
    # the beginning of first and the end of the last words, respectively.
    start = 0
    end = 0
    caption = caption.strip()

    # remove cases of 'e:' in the beginning
    regex = r"^e|E\s*:\s*"
    caption = re.sub(regex, "", caption)

    exceptions = ['"', '“', '\'', '(', '[', '{']
    for i, c in enumerate(caption):
        if c.isalnum() or c in exceptions:
            start = i
            break

    exceptions = ['"', '”', '\'', ')', ']', '}']
    for i, c in enumerate(reversed(caption)):
        if c.isalnum() or c in exceptions:
            end = -i
            break

    if end < -1:
        caption = caption[start:end]
    else:
        caption = caption[start:]

    caption = caption.strip()
    punctuation = ['.', ',', '?', '!', ';', ':']
    if len(caption) and caption[-1] not in punctuation:
        caption += '.'

    return caption


def extract_text(caption, hashtag='#pracegover'):
    caption_copy = caption
    caption = caption.lower()

    start = caption.find(hashtag)
    caption_copy = caption_copy[start:]
    caption = caption[start:]

    end = -1
    for match in re.finditer(r'fim .* descrição|fim descrição', caption):
        end = match.start()
        break

    if end == -1:
        end = caption.find('\n.')

    caption = caption_copy
    if end != -1:
        caption = caption[:end]

    caption = remove_emoji(caption)
    caption = remove_marks(caption)
    caption = remove_misplaced_punctuation(caption)

    return caption
