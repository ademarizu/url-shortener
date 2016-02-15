# url-shortener
A Simple Url Shortener.

This is the simplest Url Shortner I could think of. It's fully implemented using Python and a few libs.

* tornado
* simplejson
* redis

## Installing
Just download this code or git clone it `git clone https://github.com/ademarizu/url-shrtnr.git`

From url-shrtnr folder:

* Run `pip install -r requirements.pip` to install required libs (if you're familiar with, try using virtualevn)
* Run `python -m urlshrtnr -d <Your Domain> -a <Redis Address>`

If you need more options, just execute `python -m urlshrtnr -h` to list them.

Just go to http://localhost:8888/stats to see your own url-shortner stats.
