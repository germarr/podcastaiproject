import feedparser

def getMP3URL(mp3URL:str=None):
    # Parse the RSS feed
    feed = feedparser.parse(mp3URL)

    url_list = []
    title_list = []

    for episode in feed.entries:
        episode_audio_url = episode.enclosures[0]['href'] if 'enclosures' in episode else None

        if episode_audio_url:
            url_list.append(episode_audio_url)
            title_list.append(episode.title)

    return {
        'rss_url':url_list[0],
        'episode_title':title_list[0]
        }


if __name__ == "__main__":
    getMP3URL(mp3URL='https://feeds.simplecast.com/Sl5CSM3S')
    