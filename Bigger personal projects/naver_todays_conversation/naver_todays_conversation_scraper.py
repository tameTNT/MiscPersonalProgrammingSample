# Author: Luca Huelle
# This Python script can be used to retrieve conversation data from
# https://learn.dict.naver.com/conversation#/ and associated sites
# This includes conversations (and their translations) in both Korean and English,
# as well as the associated audio files.
# All of these resources can then be used for practice and reference.

# All conversation material (c)Naver, Yonsei University, Korean Language Institute, SIWON SCHOOL (이시원)

import argparse  # to use python file as command line program
import datetime as dt
import time  # timing statement execution
import urllib.request
from abc import ABC  # abstract base class helper
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path
from typing import List, TypedDict

# pip install requests pydub (--user) --upgrade
import requests
from pydub import AudioSegment  # to merge mp3 files

# includes placeholders {...} to use with .format() later
FILE_NAME_TEMPLATE = "[{lang}][{req_date:%Y%m%d}] Naver Today's Conversation"
DOWNLOAD_BASE_PATH = Path('downloads')
DOWNLOAD_BASE_PATH.mkdir(exist_ok=True)  # makes directory in case it doesn't already exist


# Typed Dictionaries for return type reference in later functions
class ConversationFullDataDict(TypedDict):
    id: str
    title: str
    title_translation: str
    dic_type: str
    public_date: str
    open_yn: int
    source: str
    difficulty: int
    theme: str
    source_url: str
    pron: str
    pron_file_url: str
    description: str
    week_day: int
    type: int
    total_num: int
    quiz_format_title: str
    quiz_format_translation: str
    pron_file_all_url: str
    title_elucidate: str
    sentences: List[dict]
    entrys: List[dict]
    studys: List[dict]


class SentenceDict(TypedDict):
    original: str
    translation: str


class GrammarDict(TypedDict):
    title: str
    en_description: str
    kr_description: str
    examples: List[SentenceDict]


class ConversationDict(TypedDict):
    sentences: List[SentenceDict]
    audio: List[str]
    grammar: List[GrammarDict]


# src: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser, ABC):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_html_tags(html_str: str) -> str:
    """
    This function is used together with the helper class above to remove the markup language (ML) tags from HTML strings
    e.g. 'example <i>text</i>' -> 'example text'

    :param html_str: String possibly containing HTML/markup language tags e.g. <b>, <i>, <u>
    :return: html_str with all markup tags removed
    """

    s = MLStripper()
    s.feed(html_str)
    return s.get_data()


def get_dates_in_week(date_in_week: dt.date) -> List[dt.date]:
    """
    Returns a list of the 6 datetime.date objects corresponding to Mon-Sat (inc.) from the week of date_in_week.
    Weeks are considered to start on a Monday.

    :param date_in_week: Date of day within desired week
    :return: List of dates within desired week
    """

    weekday = date_in_week.weekday()  # Monday==0, Sunday==6
    monday_date = date_in_week - dt.timedelta(days=weekday)  # finds date of the Monday using the weekday as an offset
    return [monday_date + dt.timedelta(days=i) for i in range(6)]  # only 6 days since Sunday is for review


def get_mp3_urls(sentences: List[dict]) -> List[str]:
    """
    Retrieves the urls of the mp3 audio files associated with a day's conversation's sentences.
    Warning: these urls are untested and may not link to anything at all.

    :param sentences: List of sentence data dictionaries containing a 'sentence_pron_file' field
    :return: List of urls *potentially* leading to required mp3 files
    """

    mp3_file_paths = []
    for sentence in sentences:
        mp3_file_paths.append(sentence['sentence_pron_file'])

    # base url of request API that hashes (comma-separated) filePaths provided
    url_stem = 'https://learn.dict.naver.com/dictPronunciation.dict?filePaths='
    request_url = url_stem + ','.join(mp3_file_paths)

    mp3_urls = requests.get(request_url).json()['url']  # 'url' attribute within returned json object
    return mp3_urls


def get_conversation_data_dict(lang: str = 'kr', date: dt.date = dt.date.today()) -> ConversationFullDataDict:
    """
    Retrieves conversation data dictionary for date and language provided

    :param lang: Language of conversation to retrieve. Either 'kr' (Korean) or 'en' (English)
    :param date: Date of conversation to retrieve - defaults to today's date
    :return: Dictionary containing conversation sentences, examples, grammar and more
    """

    # all request urls start and end with these bases
    url_stem = 'https://gateway.dict.naver.com/'
    url_end = f'today/{date:%Y%m%d}/conversation.dict'

    if lang == 'kr':
        request_url = url_stem + 'krdict/kr/koen/' + url_end
    elif lang == 'en':
        request_url = url_stem + 'endict/kr/enko/' + url_end
    else:
        raise ValueError('Unsupported language option provided for lang argument')

    conversation_data = requests.get(request_url).json()['data']
    if conversation_data:
        return conversation_data
    else:
        raise ValueError("That date doesn't appear to have any associated conversation data. Sorry :(")


def scrape_conversation_from_date(lang: str = 'kr', date: dt.date = dt.date.today()) -> ConversationDict:
    """
    Returns all available information for the conversation requested.

    :param lang: Language of conversation to return. Either 'kr' (Korean) or 'en' (English)
    :param date: Date of conversation to retrieve - defaults to today's date
    :return: Dictionary with three entries: 'sentences' listing all the relevant sentences + their translations
        and 'audio' listing urls of the mp3s related to those sentences.
        If lang is 'kr' then a 'grammar' field is also populated with a title, description and example sentences.
    """

    if date.weekday() == 6:  # Sunday is review day
        raise ValueError('date cannot be a Sunday - there are no new sentences on Sundays')

    # Constructs empty return dictionary containing values for sentences, audio files and grammar details
    return_data = {
        'sentences': list(),
        'audio': list(),
        'grammar': {'title': '', 'en_description': '', 'kr_description': '', 'examples': list()},
    }

    conversation_data_dict = get_conversation_data_dict(lang, date)
    sentences = conversation_data_dict['sentences']

    if lang == 'kr':  # grammar notes only exist for Korean sentences
        grammar_dict = conversation_data_dict['studys'][0]

        return_data['grammar']['title'] = grammar_dict['title']
        return_data['grammar']['en_description'] = grammar_dict['translation']
        return_data['grammar']['kr_description'] = grammar_dict['description']
        for e_dict in grammar_dict['examples']:
            return_data['grammar']['examples'].append({
                'original': strip_html_tags(e_dict['example']),
                'translation': strip_html_tags(e_dict['translation'])
            })

    for s_dict in sentences:
        return_data['sentences'].append({
            'original': strip_html_tags(s_dict['orgnc_sentence']),
            'translation': strip_html_tags(s_dict['trsl_orgnc_sentence']),
        })

    return_data['audio'] = get_mp3_urls(conversation_data_dict['sentences'])
    # noinspection PyTypeChecker
    return return_data


def output_conversation(lang: str = 'kr', date: dt.date = dt.date.today(), print_audio: bool = True,
                        hide_original: bool = False, hide_translation: bool = False,
                        print_file=None, download_audio: bool = False, concat_silence: int = 1) -> None:
    """
    Outputs a Korean/English conversation to the terminal to varying degrees of verbosity depending on arguments
    provided.

    :param lang: Language of conversation to return. Either 'kr' (Korean) or 'en' (English)
    :param date: Date of conversation to retrieve - defaults to today's date
    :param print_audio: Boolean specifying whether the links to the sentence audio mp3 files should be output
    :param hide_original: Boolean specifying whether to hide the original sentences from output
        (i.e. only show translations. If lang == 'kr', then only English sentences are output).
    :param hide_translation: Boolean specifying whether to hide the translations from output
        (i.e. only show original sentences. If lang == 'kr', then only Korean sentences are output).
    :param print_file: Optional object with write(string) method.
        Typically you want this to be a file-like object (e.g. open('example.txt', 'w+')).
        If provided, all output typically destined for the terminal will be written to the file instead.
    :param download_audio: Boolean specifying whether to physically download the mp3s associated with the urls fetched.
        If True, all sentence audio files are downloaded and concatenated into one file.
    :param concat_silence: Optional integer specifying the length of silence (in seconds) to concatenate downloaded
        audio files with. Ignored if download_audio == False.
    """

    # Builds appropriate URL for attribution of conversation depending on language specified
    url_stem = 'https://learn.dict.naver.com/conversation#/'
    if lang == 'kr':
        url_stem += 'korean-en/'
    elif lang == 'en':
        url_stem += 'endic/'
    else:
        raise ValueError('Unsupported language option provided for lang argument')

    conversation_data = scrape_conversation_from_date(lang, date)

    audio_paths = list()  # the paths to temporarily downloaded audio files will be added here

    full_src_url = f'{url_stem}{date:%Y%m%d}'
    print(f'📆 {date:%Y%m%d} - 🌐 src: {full_src_url}', file=print_file)

    # iterates through sentences and associated audio
    for i, (sentence, audio_url) in enumerate(zip(conversation_data['sentences'], conversation_data['audio'])):
        if not hide_original:  # outputs original sentence
            print(f'{i + 1}.', sentence['original'], file=print_file)
        if not hide_translation:  # outputs translation
            print('📚 ', sentence['translation'], file=print_file)
        if print_audio:  # outputs audio link
            print('🔊 ', audio_url, file=print_file)
        if download_audio:  # if requested, writes audio parts to disk
            # first item returned from urlretrieve() is path to newly created file
            # create a Path object from this string path and add it the audio_paths list
            try:
                audio_paths.append(Path(urllib.request.urlretrieve(audio_url, f'temp-{i}.mp3')[0]))
            except urllib.error.HTTPError:
                print(f"[sys] There was an error retrieving the audio file associated with sentence number {i+1}. "
                      f"Its download has been skipped and it will not be in the concatenated audio file.")

    if download_audio:  # concatenates audio parts if they were downloaded above
        # loads mp3 files into memory as AudioSegment objects
        audio_segments = [AudioSegment.from_mp3(mp3_path) for mp3_path in audio_paths]

        final_concat_mp3_file = AudioSegment.empty()  # initial building block
        for segment, path in zip(audio_segments, audio_paths):
            # concatenation is simply a Python addition operation between AudioSegments
            final_concat_mp3_file += segment
            final_concat_mp3_file += AudioSegment.silent(duration=(concat_silence * 1000))  # duration in ms
            path.unlink()  # deletes temp mp3 file as it is now no longer needed

        output_file_name = FILE_NAME_TEMPLATE.format(lang=lang.upper(), req_date=date)  # formats template from above

        tags = {  # creates tags dictionary to write to mp3 file
            'title': output_file_name,
            'TIT3': f'Source: {full_src_url}',  # TIT3 = subtitle field
            'date': f'{date:%Y}',  # date = year field
            'track': f'{date.weekday() + 1}/6',  # 6 conversations per week
            'artist': None,
            'genre': 'Education',
            'album_artist': 'Naver Dictionary',
            'album': f"Today's {lang.upper()} Conversation - "  # conversation audio is grouped into albums by weeks
                     f'w/c {get_dates_in_week(date)[0]:%Y%m%d}',
        }
        if lang == 'kr':  # attribution is slightly different depending on language
            tags['artist'] = 'Yonsei University - Korean Language Institute/Naver Dictionary'
        elif lang == 'en':
            tags['artist'] = 'Siwon School/Naver Dictionary'

        output_file_path = DOWNLOAD_BASE_PATH / (output_file_name + '.mp3')

        print(f'[sys] Writing concatenated {lang.upper()} conversation audio file from {date:%Y%m%d} to\n'
              f'      "{output_file_path}"')
        final_concat_mp3_file.export(out_f=output_file_path, format='mp3', tags=tags)


def output_all_conversations_from_week(lang: str = 'kr', date_in_week: dt.date = dt.date.today(),
                                       print_audio: bool = True, hide_original: bool = False,
                                       hide_translation: bool = False, print_file=None, download_audio: bool = False,
                                       concat_silence: int = 1) -> None:
    """
    Executes output_conversation(...) for each day in the same week as date_in_week
    (weeks are considered to start on a Monday).

    See documentation of output_conversation(...) for role of all other arguments.
    """

    dates_to_scrape = get_dates_in_week(date_in_week)
    for date in dates_to_scrape:
        output_conversation(lang, date, print_audio, hide_original, hide_translation, print_file, download_audio, concat_silence)
        print('\n---------------------\n', file=print_file)  # separator between conversations


def write_all_conversations_of_week_to_file(lang: str = 'kr', date_in_week: dt.date = dt.date.today(),
                                            print_audio: bool = False, hide_original: bool = False,
                                            hide_translation: bool = True, download_audio: bool = False,
                                            concat_silence: int = 1) -> None:
    """
    Executes output_conversation(...) for each day in the same week as date_in_week
    (weeks are considered to start on a Monday).
    However, this function generates a print_file (.txt) for each conversation automatically,
    so you don't need to manually supply one as a function argument.

    See documentation of output_conversation(...) for role of all other arguments.
    """

    dates_to_scrape = get_dates_in_week(date_in_week)
    for date in dates_to_scrape:
        # constructs path to appropriate text file and then creates it if it doesn't already exist
        # with encoding UTF-8 to ensure Korean Hangul characters are saved correctly
        txt_file_path = DOWNLOAD_BASE_PATH / Path(FILE_NAME_TEMPLATE.format(lang=lang.upper(), req_date=date) + '.txt')
        print_file = txt_file_path.open('w+', encoding='UTF-8')

        print(f'[sys] Writing {lang.upper()} conversation from {date:%Y%m%d} to\n'
              f'      "{txt_file_path}"')
        output_conversation(lang, date, print_audio, hide_original, hide_translation, print_file, download_audio, concat_silence)


def test_date_str(date_str: str) -> dt.date:
    """
    Simply validation function to test whether date_str is in format YYYYMMDD

    :param date_str: String to test
    :return: datetime.date object if string is valid
    :raises ValueError: If string is not valid
    """

    try:
        date = dt.datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        raise ValueError('Date provided not in format YYYYMMDD')

    return date


if __name__ == '__main__':
    # initialises an ArgumentParser object to enable use of this file as a command line application
    parser = argparse.ArgumentParser(
        description="Fetches and outputs texts, and links to associated audio files, "
                    "of Naver's daily Korean/English conversations."
    )

    # adds all various arguments/options corresponding to relevant function arguments above
    parser.add_argument('-l', '--language', default='kr', choices=['kr', 'en'],
                        help='Specify the language of conversations to be fetched.')

    parser.add_argument('-au', '--audio-urls', action='store_true',
                        help='If given, urls to native speaker audio files are also printed.')

    parser.add_argument('-ad', '--audio-download', action='store_true',
                        help='If given, native speaker audio is downloaded and concatenated into 1 mp3 per day.')

    parser.add_argument('-cs', '--concat-silence', metavar='SECONDS', type=int,
                        help='If audio-download is also given, this is the length of silence (in secs) between '
                             'sentence audio in the final concatenated  mp3 file. Otherwise, ignored.')

    parser.add_argument('-ho', '--hide-original', action='store_true',
                        help='If given, the original language sentences are *not* printed.')

    parser.add_argument('-ht', '--hide-translation', action='store_true',
                        help='If given, translations of each of the sentences are *not* printed.')

    parser.add_argument('-wtf', '--write-to-file', metavar='OUTPUT_FILE',
                        type=argparse.FileType('w+', encoding='UTF-8'),  # UTF-8 for KR characters
                        help='The (relative) path to a file (does *not* already have to exist) that, if given, results '
                             'in all output being written to this file, as text, instead of the terminal.')

    # the following arguments are mutually exclusive - only one of the them needs to be provided depending on use case
    use_case = parser.add_mutually_exclusive_group(required=True)

    # nargs='*' used to make meta variable optional - otherwise doesn't play nicely with required=True
    use_case.add_argument('-d', '--date', metavar='DATE', nargs='*',
                          help='Prints the conversation associated with the given DATE (YYYYMMDD). '
                               'If no DATE is provided, defaults to today.')

    use_case.add_argument('-w', '--week', metavar='DATE', nargs='*',
                          help='Prints all of the conversations that form part of the week that includes DATE (YYYYMMDD).'
                               'Weeks are considered to start on a Monday. If no DATE is provided, defaults to today.')

    use_case.add_argument('-www', '--write-whole-week', metavar='DATE', nargs='*',
                          help="All conversations within the given week are written to their own individual text file - "
                               "e.g. `[KR][YYYYMMDD] Naver Today's Conversation.txt`. "
                               'Note: still affected by all other arguments such as --hide-translation and --hide-original.')

    args = parser.parse_args()

    user_date = f'{dt.date.today():%Y%m%d}'  # initial default for date argument

    start = time.time()  # used to time download/execution
    if args.write_to_file:  # status updates only needed when writing to files - otherwise terminal would be silent
        print(f'[sys] All non-[sys] output is being written to "{args.write_to_file.name}".\n[sys] Fetching data...', end='\r')

    if args.date is not None:  # i.e. an empty or 1-arg-populated list - `if args.week` would evaluate to False if no DATE provided
        if args.date:  # date default needs to be overwritten by user input
            user_date = args.date[0]  # since nargs='*', args.week is a list of supplied arguments provided

        output_conversation(lang=args.language, date=test_date_str(user_date), print_audio=args.audio_urls,
                            hide_original=args.hide_original, hide_translation=args.hide_translation,
                            print_file=args.write_to_file, download_audio=args.audio_download,
                            concat_silence=args.concat_silence)

    elif args.week is not None:
        if args.week:
            user_date = args.week[0]

        output_all_conversations_from_week(lang=args.language, date_in_week=test_date_str(user_date),
                                           print_audio=args.audio_urls, hide_original=args.hide_original,
                                           hide_translation=args.hide_translation, print_file=args.write_to_file,
                                           download_audio=args.audio_download, concat_silence=args.concat_silence)

    elif args.write_whole_week is not None:
        if args.write_whole_week:
            user_date = args.write_whole_week[0]

        print('[sys] Writing conversations to files...')
        write_all_conversations_of_week_to_file(lang=args.language, date_in_week=test_date_str(user_date),
                                                print_audio=args.audio_urls, hide_original=args.hide_original,
                                                hide_translation=args.hide_translation,
                                                download_audio=args.audio_download, concat_silence=args.concat_silence)

    if args.write_to_file:
        print(f'[sys] Done. (Took {time.time() - start:.2f}s)')
