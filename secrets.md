```
pip install Mastodon.py

>>> from mastodon import Mastodon
>>> Mastodon.create_app('h2g2bob-rocks', api_base_url="https://botsin.space/", to_file = 'h2g2bob_rocks....secret')
>>> mastodon = Mastodon(client_id = 'h2g2bob_rocks....secret')
>>> mastodon.log_in("...@email...", "...", to_file="spacestationsouthend....secret")
>>> mastodon = Mastodon(access_token="spacestationsouthend....secret")
>>> mastodon.toot("...")
```
