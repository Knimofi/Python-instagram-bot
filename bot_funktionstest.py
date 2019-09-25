from instapy import InstaPy
from instapy.util import smart_run

## Kommentar mit Doppel Raute ## sind Erläuterungen (niemals auskommentieren)
# Kommentar mit einfacher Raute # ist ein funktionierender Befehl (bei Bedarf auskommentieren)

## Login Daten
insta_username = 'USERNAME'
insta_password = 'PASSWORD'

## Neue Session anlegen
## set headless_browser=True to run InstaPy in the Background
## headless_browser=True um InstaPy im Hintergrund laufen zu lassen
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)


with smart_run(session):
    """ Activity flow """
    ## Einstellungen
    session.set_relationship_bounds(enabled=True,                  ## Soll dieses Feature aktiviert sein?
                                      delimit_by_numbers=True,     ## Soll basierend auf min und max Follower entschieden werden? Alternative wäre potency_ratio=1.5, delimit_by_numbers=False
                                       max_followers=4590,         ## Wie viel Followers darf die Zielperson maximal haben?
                                        min_followers=0,          ## Wie viel Followers muss die Zielperson minimal haben?
                                        min_following=0)          ## Wie vielen anderen Accounts muss die Zielperson selbst mindestens folgen?

    
    ## Follower deines Accounts, die für alle Aktionen ignoriert werden sollen (Freunde)
    #session.set_dont_include(["friend1", "friend2", "friend3"])
        
    ## Interaktionen basierend auf den obigen Einstellungen 
    session.like_by_tags(["meme"], amount=5)