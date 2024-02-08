

# our url + 6 random characters (a-z, A-Z, 0-9), create in database the id
## Shorten_url could be implemented two-fold:
## We store our site URL as some string of characters (no limit) but also
## store a paired "short" link from bit.ly or goo.gl that redirects to our
## site's URL.
## This would offload the shortening to a much shorter, and trusted, domain.
## e.g. (goo.gl/nZc2Th -> Summari.ly/t2Ch5mRzyt)
def shorten_url(url: str) -> str:
    
    return