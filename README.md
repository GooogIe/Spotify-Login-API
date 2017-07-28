# Spotify-Login-API
An unofficial wrapper for Spotify's services


### How to use it ###

```python
import Spotify

print Spotify.login("email","password") # Params= email/username,password

# It'll return a list, containing [False,"Dead"] if the account is dead
# or [True,"Free"] if it isn't and it's free
# or [True,sub+" until "+exp+",Country:"+country] if it's paid

```
