#!/usr/bin/python3
import os
import sys
import datetime
from unicodedata import category

# TODO: Sort posts by categories

HEADER_TEMPLATE = """
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="ie=edge" />
<link rel="stylesheet" type="text/css" href="https://css-storage.s3.eu-central-1.amazonaws.com/common-vendor.b8ecfc406ac0b5f77a26.css">
<link rel="stylesheet" type="text/css" href="https://css-storage.s3.eu-central-1.amazonaws.com/fretboard.f32f2a8d5293869f0195.css">
<link rel="stylesheet" type="text/css" href="https://css-storage.s3.eu-central-1.amazonaws.com/pretty-vendor.83ac49e057c3eac4fce3.css">
<link rel="stylesheet" type="text/css" href="https://css-storage.s3.eu-central-1.amazonaws.com/pretty.0ae3265014f89d9850bf.css">
<link rel="stylesheet" type="text/css" href="$root/css/misc.css">
<script type="text/javascript" id="MathJax-script" async
  src="/scripts/mathjax.js">
</script>
<style>
@font-face {
    font-family: MJXc-TeX-math-Iw;
    src: url(
        "https://assets.hackmd.io/build/MathJax/fonts/HTML-CSS/TeX/woff/MathJax_Main-Regular.woff")
}
@font-face {
    font-family: MJXZERO;
    src: url(
        "https://assets.hackmd.io/build/MathJax/fonts/HTML-CSS/TeX/woff/MathJax_Main-Regular.woff")
}
@font-face {
    font-family: MJXTEX;
    src: url(
        "https://assets.hackmd.io/build/MathJax/fonts/HTML-CSS/TeX/woff/MathJax_Main-Regular.woff")
}
.math { font-family: MJXc-TeX-math-Iw }
</style>
</head>
<div id="doc" class="container-fluid markdown-body comment-enabled" data-hard-breaks="true">
"""

RSS_LINK = """
<head>
<link rel="alternate" type="application/rss+xml" href="{}/feed.xml" title="{}">
"""

TITLE_TEMPLATE = """
<br>
<h1 style="margin-bottom:7px"> {0} </h1>
<small style="float:left; color: #888"> {1} </small>
<small style="float:right; color: #888"><a href="{2}/index.html">See all posts</a></small>
<br> <br> <br>
<title> {0} </title>
"""


TOC_TITLE_TEMPLATE = """
<title> {0} </title>
<br>
<center><h1 style="border-bottom:0px"> {0} </h1></center>
"""

FOOTER = """<p class="footer">Daniel Ratmiroff © - site made with: <a target="_blank" href="https://github.com/vbuterin/blogmaker" alt="blog maker">blogmaker</a> - credit to <a href="https://vitalik.ca/" target="_blank" alt"Vitalik's website">Vitalik Buterin</a></p></div> """

TOC_START = """
<br>
<ul class="post-list" style="padding-left:0">
"""

TOC_END = """ </ul> """

TOC_ITEM_TEMPLATE = """
<li>
    <span class="post-meta">{} • </span> <span class="post-category {}">{}</span>
    <h3 style="margin-top:12px">
      <a class="post-link" href="{}">{}</a>
    </h3>
</li>
"""

TWITTER_CARD_TEMPLATE = """
<meta name="twitter:card" content="summary" />
<meta name="twitter:title" content="{}" />
<meta name="twitter:image" content="{}" />
"""


RSS_ITEM_TEMPLATE = """
<item>
<title>{title}</title>
<link>{link}</link>
<guid>{link}</guid>
<pubDate>{pub_date}</pubDate>
<description>{description}</description>
</item>
"""


RSS_MAIN_TEMPLATE = """
<?xml version="1.0" ?>
<rss version="2.0">
<channel>
  <title>{title}</title>
  <link>{link}</link>
  <description>{title}</description>
  <image>
      <url>{icon}</url>
      <title>{title}</title>
      <link>{link}</link>
  </image>
{items}
</channel>
</rss>
"""


def extract_metadata(fil, filename=None):
    metadata = {}
    if filename:
        assert filename[-3:] == '.md'
        metadata["filename"] = filename[:-3]+'.html'
    while 1:
        line = fil.readline()
        if line and line[0] == '[' and ']' in line:
            key = line[1:line.find(']')]
            value_start = line.find('(')+1
            value_end = line.rfind(')')
            if key in ('category', 'categories'):
                metadata['categories'] = set([
                    x.strip().lower() for x in line[value_start:value_end].split(',')
                ])
                assert '' not in metadata['categories']
            else:
                metadata[key] = line[value_start:value_end]
        else:
            break
    return metadata


def metadata_to_path(global_config, metadata):
    return os.path.join(
        global_config.get('posts_directory', 'posts'),
        metadata['date'],
        metadata['filename']
    )


def generate_feed(global_config, metadatas):
    def get_link(route):
        return global_config['domain'] + "/" + route

    def get_date(date_text):
        year, month, day = (int(x) for x in date_text.split('/'))
        date = datetime.date(year, month, day)
        return date.strftime('%a, %d %b %Y 00:00:00 +0000')

    def get_item(metadata):
        return RSS_ITEM_TEMPLATE.format(
            title=metadata['title'],
            link=get_link(
                '/'.join([global_config['posts_directory'], metadata['date'], metadata['filename']])),
            pub_date=get_date(metadata['date']), description=''
        )

    return RSS_MAIN_TEMPLATE.strip().format(
        title=global_config['title'],
        link=get_link(''),
        icon=global_config['icon'],
        items="\n".join(map(get_item, metadatas))
    )


def make_twitter_card(title, global_config):
    return TWITTER_CARD_TEMPLATE.format(title, global_config['icon'])


def defancify(text):
    return text \
        .replace("’", "'") \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('…', '...') \



def make_categories_header(categories, root_path):
    o = ['<center><div class="toc-category-container">']
    for index, category in enumerate(categories, start=1):
        template = '<span class="toc-category" style="font-size:115%"><a alt="{}" href="{}/categories/{}.html">{}</a></span>'
        o.append(template.format(category, root_path,
                 category, category.capitalize()))

        if index != len(categories):
            o.append(" • ")

    o.append('</div></center>')
    return '\n\n'.join(o)


def get_printed_date(metadata):
    year, month, day = metadata['date'].split('/')
    month = 'JanFebMarAprMayJunJulAugSepOctNovDec'[int(month)*3-3:][:3]
    return year + ' ' + month + ' ' + day


def get_printed_category(metadata):
    year, month, day = metadata['date'].split('/')
    month = 'JanFebMarAprMayJunJulAugSepOctNovDec'[int(month)*3-3:][:3]
    return year + ' ' + month + ' ' + day


# article preview
def make_toc_item(global_config, metadata, root_path):
    link = metadata_to_path(global_config, metadata)
    category = list(metadata['categories'])[0]
    return TOC_ITEM_TEMPLATE.format(get_printed_date(metadata), metadata['color'], category, root_path + '/' + link, metadata['title'])

# articles


def make_toc(toc_items, global_config, all_categories, category=None):
    title = global_config['title']
    if category:
        root_path = '..'
    else:
        root_path = '.'

    return (
        RSS_LINK.format(root_path, title) +
        HEADER_TEMPLATE.replace('$root', root_path) +
        make_twitter_card(title, global_config) +
        TOC_TITLE_TEMPLATE.format(title) +
        make_categories_header(all_categories, root_path) +
        TOC_START +
        ''.join(toc_items) +
        TOC_END +
        FOOTER
    )


if __name__ == '__main__':
    # Get blog config
    global_config = extract_metadata(open('config.md'))

    # Special case: '--sync' option
    if '--sync' in sys.argv:
        os.system(
            'rsync -av site/. {}:{}'.format(global_config['server'], global_config['website_root']))
        sys.exit()

    # Normal case: process each provided file
    for file_location in sys.argv[1:]:
        filename = os.path.split(file_location)[1]
        print("Processing file: {}".format(filename))

        # Extract path
        file_data = open(file_location).read()
        metadata = extract_metadata(open(file_location), filename)
        path = metadata_to_path(global_config, metadata)

        # Generate the html file
        options = metadata.get('pandoc', '')

        os.system(
            'pandoc -o /tmp/temp_output.html {} {}'.format(file_location, options))
        root_path = '../../../..'
        total_file_contents = (
            RSS_LINK.format(root_path, metadata['title']) +
            HEADER_TEMPLATE.replace('$root', root_path) +
            make_twitter_card(metadata['title'], global_config) +
            TITLE_TEMPLATE.format(metadata['title'], get_printed_date(metadata), root_path) +
            defancify(open('/tmp/temp_output.html').read()) +
            FOOTER
        )

        print("Path selected: {}".format(path))

        # Make sure target directory exists
        truncated_path = os.path.split(path)[0]
        os.system('mkdir -p {}'.format(os.path.join('site', truncated_path)))

        # Put it in the desired location
        out_location = os.path.join('site', path)
        open(out_location, 'w').write(total_file_contents)

    # Reset ToC
    metadatas = []
    categories = set()
    for filename in os.listdir('posts'):
        if filename[-4:-1] != '.sw':
            metadatas.append(extract_metadata(
                open(os.path.join('posts', filename)), filename))
            categories = categories.union(metadatas[-1]['categories'])

    print("Detected categories: {}".format(' '.join(categories)))

    sorted_metadatas = sorted(metadatas, key=lambda x: x['date'], reverse=True)
    feed = generate_feed(global_config, sorted_metadatas)

    os.system('mkdir -p {}'.format(os.path.join('site', 'categories')))

    print("Building tables of contents...")

    homepage_toc_items = [
        make_toc_item(global_config, metadata, '.') for metadata in sorted_metadatas if
        # Filter posts that are not in the homepage category
        global_config.get('homepage_category',
                          '') in metadata['categories'].union({''})
    ]

    for category in categories:
        # Enable to concat all categories into homepage_category
        # if category == global_config.get('homepage_category'):
        #     category_toc_items = [make_toc_item(
        #         global_config, metadata, '..') for metadata in sorted_metadatas]
        # else:
        category_toc_items = [
            make_toc_item(global_config, metadata, '..') for metadata in sorted_metadatas if
            category in metadata['categories']
        ]

        toc = make_toc(category_toc_items, global_config, categories, category)
        open(os.path.join('site', 'categories', category+'.html'), 'w').write(toc)

    open('site/feed.xml', 'w').write(feed)
    open('site/index.html',
         'w').write(make_toc(homepage_toc_items, global_config, categories))

    # Copy CSS and scripts files
    this_file_directory = os.path.dirname(__file__)

    os.system('cp -r {} site/'.format(os.path.join(this_file_directory, 'css')))
    os.system('cp -r {} site/'.format(os.path.join(this_file_directory, 'scripts')))
    os.system('rsync -av images site/')
