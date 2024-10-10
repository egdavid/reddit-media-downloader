import pytest
import asyncio
from unittest.mock import Mock, patch
from reddit_media_downloader import RedditMediaDownloader, RedditMedia

@pytest.fixture
def downloader():
    return RedditMediaDownloader("testuser")

@pytest.mark.asyncio
async def test_fetch_posts(downloader):
    mock_response = {
        "data": {
            "children": [
                {"data": {"url": "https://i.redd.it/test1.jpg"}},
                {"data": {"url": "https://i.redd.it/test2.png"}},
                {"data": {"url": "https://v.redd.it/test3.mp4"}},
            ],
            "after": "t3_abc123"
        }
    }
    
    with patch.object(downloader.session, "get") as mock_get:
        mock_get.return_value.__aenter__.return_value.json = asyncio.coroutine(lambda: mock_response)
        mock_get.return_value.__aenter__.return_value.status = 200
        
        result = await downloader.fetch_posts()
        
        assert result == mock_response
        mock_get.assert_called_once_with(downloader.base_url.format(downloader.username))

def test_extract_media_urls(downloader):
    mock_data = {
        "data": {
            "children": [
                {"data": {"url": "https://i.redd.it/test1.jpg"}},
                {"data": {"url": "https://i.redd.it/test2.png"}},
                {"data": {"url": "https://v.redd.it/test3.mp4"}},
                {"data": {"url": "https://www.reddit.com/r/test/comments/123/test_post/"}},
            ]
        }
    }
    
    result = downloader.extract_media_urls(mock_data)
    
    assert len(result) == 3
    assert all(isinstance(media, RedditMedia) for media in result)
    assert result[0].url == "https://i.redd.it/test1.jpg"
    assert result[0].filename == "test1.jpg"
    assert result[1].url == "https://i.redd.it/test2.png"
    assert result[1].filename == "test2.png"
    assert result[2].url == "https://v.redd.it/test3.mp4"
    assert result[2].filename == "test3.mp4"

@pytest.mark.asyncio
async def test_download_media(downloader):
    media = RedditMedia(url="https://i.redd.it/test.jpg", filename="test.jpg")
    
    with patch.object(downloader.session, "get") as mock_get, \
         patch("aiofiles.open") as mock_open:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.read = asyncio.coroutine(lambda: b"fake image data")
        
        mock_file = Mock()
        mock_open.return_value.__aenter__.return_value = mock_file
        mock_file.write = asyncio.coroutine(lambda _: None)
        
        await downloader.download_media(media)
        
        mock_get.assert_called_once_with(media.url)
        mock_open.assert_called_once()
        mock_file.write.assert_called_once_with(b"fake image data")

@pytest.mark.asyncio
async def test_download_all_media(downloader):
    with patch.object(downloader, "fetch_posts") as mock_fetch, \
         patch.object(downloader, "extract_media_urls") as mock_extract, \
         patch.object(downloader, "download_media") as mock_download:
        
        mock_fetch.side_effect = [
            {"data": {"children": [{"data": {"url": "https://i.redd.it/test1.jpg"}}], "after": "t3_abc123"}},
            {"data": {"children": [{"data": {"url": "https://i.redd.it/test2.jpg"}}], "after": None}}
        ]
        mock_extract.side_effect = [
            [RedditMedia(url="https://i.redd.it/test1.jpg", filename="test1.jpg")],
            [RedditMedia(url="https://i.redd.it/test2.jpg", filename="test2.jpg")]
        ]
        mock_download.return_value = None
        
        await downloader.download_all_media()
        
        assert mock_fetch.call_count == 2
        assert mock_extract.call_count == 2
        assert mock_download.call_count == 2

if __name__ == "__main__":
    pytest.main()