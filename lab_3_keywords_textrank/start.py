"""
TextRank keyword extraction starter
"""

from pathlib import Path
from lab_3_keywords_textrank.main import *


if __name__ == "__main__":

    # finding paths to the necessary utils
    PROJECT_ROOT = Path(__file__).parent
    ASSETS_PATH = PROJECT_ROOT / 'assets'

    # reading the text from which keywords are going to be extracted
    TARGET_TEXT_PATH = ASSETS_PATH / 'article.txt'
    with open(TARGET_TEXT_PATH, 'r', encoding='utf-8') as file:
        text = file.read()

    # reading list of stop words
    STOP_WORDS_PATH = ASSETS_PATH / 'stop_words.txt'
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as file:
        stop_words = tuple(file.read().split('\n'))

    RESULT = None
    # python -m pytest -m mark8
    punctuation = ('!', '"', '#', '$', '%', '&', '''''', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
                   '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~')
    decoded = None
    decoded_dict = None
    decoded_position_biased_adjacency = None
    decoded_position_biased_edge = None

    text_preprocessor = TextPreprocessor(stop_words=stop_words, punctuation=punctuation)
    tokens = text_preprocessor.preprocess_text(text=text)

    text_encoder = TextEncoder()
    encoded_tokens = text_encoder.encode(tokens=tokens)

    if encoded_tokens:
        graph = AdjacencyMatrixGraph()
        graph.fill_from_tokens(encoded_tokens, window_length=3)
        graph.fill_positions(encoded_tokens)
        graph.calculate_position_weights()

        graph_dict = EdgeListGraph()
        graph_dict.fill_from_tokens(encoded_tokens, window_length=3)
        graph_dict.fill_positions(encoded_tokens)
        graph_dict.calculate_position_weights()

        vanilla = VanillaTextRank(graph)
        vanilla.train()
        keywords = vanilla.get_top_keywords(10)
        decoded = text_encoder.decode(encoded_tokens=keywords)

        vanilla_dict = VanillaTextRank(graph_dict)
        vanilla_dict.train()
        keywords_dict = vanilla_dict.get_top_keywords(10)
        decoded_dict = text_encoder.decode(encoded_tokens=keywords_dict)

        position_biased_textrank_adjacency = PositionBiasedTextRank(graph)
        position_biased_textrank_adjacency.train()
        keywords_position_biased_adjacency = position_biased_textrank_adjacency.get_top_keywords(10)
        decoded_position_biased_adjacency = text_encoder.decode(encoded_tokens=keywords_position_biased_adjacency)

        position_biased_textrank_edge = PositionBiasedTextRank(graph_dict)
        position_biased_textrank_edge.train()
        keywords_position_biased_edge = position_biased_textrank_edge.get_top_keywords(10)
        decoded_position_biased_edge = text_encoder.decode(encoded_tokens=keywords_position_biased_edge)

    RESULT = decoded
    print('keywords with AdjacencyMatrixGraph: ', decoded, '\n',
          'keywords with EdgeListGraph: ', decoded_dict, '\n',
          'keywords with AdjacencyMatrixGraph PositionBiasedTextRank', decoded_position_biased_adjacency, '\n',
          'keywords with EdgeListGraph PositionBiasedTextRank', decoded_position_biased_edge)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Keywords are not extracted'
