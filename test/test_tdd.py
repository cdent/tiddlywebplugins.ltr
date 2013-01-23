
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.ltr import init, TYPE, tokenize
from tiddlyweb.config import config

def setup_module(module):
    tiddler = Tiddler('test')
    tiddler.type = TYPE
    tiddler.text = """
This is the text. It has a WikiLink and
it has a [[freelink]] and a modified
[[link to something|else]], and a
[[link to http|http://example.com]] and a
raw http://example.com link. And well we
may as Well@space and [[something]]@space and
[[link to where|this]]@space and oh yeah
just @space.
"""
    module.tiddler = tiddler


def test_init():
    render_type = config['wikitext.type_render_map']
    assert TYPE not in render_type
    init(config)
    assert TYPE in render_type


def test_parse():
    tokens = tokenize(tiddler.text)

    print tiddler.text
    print '#' * 80
    output = ''
    for token in tokens:
        inner = token[0]
        name = inner.getName()
        if name == 'word' or name == 'ws' or name == 'punc':
            output += inner.get(name)
        elif name == 'urilink':
            value = inner.get('urilink')
            output += '<a href="%s">%s</a>' % (value, value)
        elif name == 'link':
            value = inner.get('link')
            if '|' in value:
                label, target = value.split('|', 1)
            else:
                label = target = value
            output += '<a href="%s">%s</a>' % (target, label)
        elif name == 'spacelink':
            value = inner.get('link')
            space = inner.get('space')
            if '|' in value:
                label, target = value.split('|', 1)
            else:
                label = target = value
            output += ('<a href="http://%s.space.com/%s">%s@%s</a>'
                    % (space, target, label, space))
        elif name == 'space':
            value = inner.get('space')
            output += '<a href="http://%s.space.com/">@%s</a>' % (value, value)
    print output
