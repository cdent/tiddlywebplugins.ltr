"""
Link Text Renderer.

Turn plain text into plain text with links from wikilinks and
freelinks.
"""
from pyparsing import (Literal, Word, alphanums, punc8bit, Regex, White,
        Optional, SkipTo, Or)
from string import punctuation


TYPE = 'text/x-linkedtext'


### Establish Parser Rules
URL_PATTERN = r"(?:file|http|https|mailto|ftp|irc|news|data):[^\s'\"]+(?:/|\b)"
SPACE = (Literal('@').suppress() + Word(alphanums, alphanums + '-')('space'))
WIKIWORD = Regex(r'[A-Z][a-z]+(?:[A-Z][a-z]*)+')('link')
LINK = (Literal("[[").suppress() + SkipTo(']]')('link')
        + Literal("]]").suppress())
SPACELINK = ((LINK ^ WIKIWORD) + SPACE.leaveWhitespace())('spacelink')
NONWIKISPACE = (Word(alphanums, alphanums)('link') + SPACE.leaveWhitespace())('spacelink')
URI = Regex(URL_PATTERN)('urilink')
PUNC = Word(punctuation)('punc')
WS = White()('ws')
WORD = Word(alphanums)('word')
CONTENT = Or([PUNC, LINK, WIKIWORD, URI, SPACELINK, SPACE, NONWIKISPACE, WS, WORD])


def tokenize(text):
    """
    Turn text into tokens.
    """
    return CONTENT.leaveWhitespace().scanString(text)


def render(tiddler, environ):
    pass


def init(config):
    config['wikitext.type_render_map'][TYPE] = __name__
