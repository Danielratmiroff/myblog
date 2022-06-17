[category]: <> (side projects)
[date]: <> (2022/06/15)
[title]: <> (Youtube podcasts)
[color]: <> (green)

## Fetch your favourite podcasts

[Build Status](https://github.com/Danielratmiroff/yt-podcasts/actions/workflows/main.yml/badge.svg)

While searching for podcasts in youtube, I get distracted by all of its rich features.

To addressed this problem, I created this simple website that fetchs uniquely my favourite podcasts.

[Github](https://github.com/Danielratmiroff/yt-podcasts)![Visit App](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

#### Currently supported podcasts:

- [Lex Fridman Podcast](https://www.youtube.com/c/lexfridman)![Github](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

## Usage

1. Clone the project into a local folder
2. Create a Youtube API Key - [How to create API key](https://developers.google.com/youtube/registering_an_application)
3. Set you Youtube API Key as a OS environmental variable

```bash
sudo nano ~/.bashrc
```

Add in the file:

```bash
export YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

4. Run it using run-locally.sh

```bash
sh run-locally.sh
```

5. Access [http://localhost:9000](http://localhost:9000/)

## UI Design:

![Screenshot](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/podcasts/screenshot.jpg)\
