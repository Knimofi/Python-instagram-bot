"""Dieses Skript folgt den Followern von Zielpersonen. Besonders geeignet für die eigene Niesche"""
""" Skript ist mehr auf organisches Wachstum ausgelegt weniger auf Performance """
## Imports
import sys
import base64
import random
from instapy import InstaPy
from instapy.util import smart_run


## Kommentar mit Doppel Raute ## sind Erläuterungen (niemals auskommentieren)
# Kommentar mit einfacher Raute # ist ein funktionierender Befehl (bei Bedarf auskommentieren)

## Login Daten
insta_username = 'YOUR_USERNAME'
insta_password = 'YOUR_PASSWORD'
dont_likes, targets, comments, ignore_users, friends, ignore_list = ([] for i in range(6))

## Einstellungen Ausnahmen ##

## Ausnahme für Hashtags in einem Post, die Dir (dem Bot) nicht geliked werden sollen.
## Volltreffer mit [#] als Prefix.  Worttreffer ohne [#] als Prefix.  (Beispiel: Stift, Bleistift, Stiftung)
## Vergliechen wird immer mit alle Hashtags in einem Post. Sowohl die Beschreibung des Posts als auch alle Kommentare des Besitzers.
#dont_likes = ["Porn", "#Porno", "#Volltreffer", "Worttreffer"]
dont_likes = ["Porn"]

## Ausnahme für Follower deines Accounts, die für Likes ignoriert werden sollen (Freunde)
#ignore_users = ["Freund1", "Freund2", "Freund3"]

## Ausnahme für Follower deines Accounts, die für Kommentare und Unfollows ignoriert werden sollen.
## Sprich Deine Freunde. (Posts werden trotzdem geliked)
#friends = ["Freund4", "Freund2", "Freund5"]

## Ausnahme der Ausnahmen (Obwohl eine der Ausnahmen zutrifft, wird trotzdem geliked,
## wenn folgendes Wort vorkommt ...)
## Beispiel: Freund1 hat einen Post veröffentlicht "Ich liebe Schnitzel #Schnitzeltag".
## Obwohl er auf der Ignore Users Liste ist wird der Post trotzdem geliked wegen der
## Ausnahme der Ausnahme.
#ignore_list = ["Schnitzeltag"]


## Einstellungen Zielgruppe
## Die Follower folgender Accounts werden als potentielle Zielperson in Betracht gezogen
## Es empfiehlt sich Accounts aus der gleichen Nische zu nehmen bzw. Konkurrenten
targets = ['buzzfeedtasty', 'piatti.italiani', 'israeli_kitchen', 'proper_tasty', 'recipesofholly', 'tasteofhome', 'delicious.eats.asmr', 'tastykaty', 'einfachtasty', 'foodsmut']


## Einstellungen Kommentare
comments = [u'👍', u'👌', u'👏',"great :)"]

## Der Bot ist auf 24 Sessions eingestellt, wobei eine Session ca. 1 Std. dauert.
## Kann jederzeit unterbrochen werden. 
for x in range(int(sys.argv[1])):

## Browser unsichtbar im Hintergrund wegen headless_browser=True
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      	headless_browser=True,
                      		disable_image_load=True,
                      			multi_logs=True)

    with smart_run(session):

        ## Losgehts
        session.set_dont_include(friends)
        session.set_dont_like(dont_likes)
        session.set_ignore_if_contains(ignore_list)
        session.set_ignore_users(ignore_users)
        session.set_simulation(enabled=True)
        session.set_relationship_bounds(enabled=True,     ## Vgl. Bot_funktionstest
                    potency_ratio=None,                   ## Vgl. Bot_funktionstest
                    delimit_by_numbers=True,
                    max_followers=4950,                   ## Vgl. Bot_funktionstest
                        max_following=1000,               ## Vgl. Bot_funktionstest
                        min_followers=25,                 ## Vgl. Bot_funktionstest
                        min_following=25,                 ## Vgl. Bot_funktionstest
                        min_posts=10)                     ## Minimale Posts (Keinen Leichen folgen)
        session.set_skip_users(skip_private=True,         ## Accounts die auf privat gesetzt sind ignorieren
                                    skip_no_profile_pic=True,   ## Accounts ohne Profilbild ignorieren
                                    skip_business=True)   ## Überspringe Instagram Geschäftskonten
                               
        
        ## Der Bot hat sich nun eine Liste von potentiellen Zielpersonen erstellt,
        ## auf die alle vorgenommenen Einstellungen zutreffen.
        
        ## Wie viele Ineraktionen sollen maximal pro Zielperson vorgenommen werden?
        session.set_user_interact(amount=2, randomize=True, percentage=80, media='Photo')
        ## Wie viele der Interaktionen sind Likes?
        session.set_do_like(enabled=True, percentage=90)
        ## Wie viele der Interaktionen sind Kommentare?
        session.set_do_comment(enabled=True, percentage=15)
        ## Was wird kommentiert?
        session.set_comments(comments, media='Photo')
        ## Wie viele der Interaktionen sind Follows (Von dir an die Zielperson)
        session.set_do_follow(enabled=True, percentage=40, times=1)
        #session.set_dont_unfollow_active_users(enabled=True, posts=3)
        
        ## Zielauswahl des Bots (Mehr Zufall)
        number = random.randint(3, 5)
        random_targets = targets
        if len(targets) <= number:
            random_targets = targets
        else:
            random_targets = random.sample(targets, number)

        
        ## Das Skript auf Likers von Bildern eines Users umstellen:
        ## Nun versucht der Bot nicht mehr die Follower Liste durch Klick auf Followers abzurufen sondern öffnent
        ## die Fotos eines Accounts, guckt wer es geliked hat und führt dann die eingestellten Interaktionen (follow/like/comment) durch.
        session.follow_likers(random_targets, photos_grab_amount = 2, follow_likers_per_photo = random.randint(15,35), randomize=True, sleep_delay=600, interact=True)

        ## UNFOLLOW wichtig für die Instagram tägliche Follow Limits und den Follower:Following Ratio
        ## Unfollow jedem, dem DU (nicht der Bot) gefollowed bist, der aber nach 24 Stunden nicht zurück gefollowed hat.
        session.unfollow_users(amount=random.randint(75,100), InstapyFollowed=(True, "nonfollowers"), style="FIFO", unfollow_after=24*60*60, sleep_delay=600)
        ## Unfollow jedem, dem der Bot gefollowed hat, wenn nach 72 Stunden (3 Tage) nicht zurück gefollowed wurde.
        session.unfollow_users(amount=random.randint(75,100), InstapyFollowed=(True, "all"), style="FIFO", unfollow_after=72*60*60, sleep_delay=600)
    