
from filter_plugins.excludes import \
    ExcludeByRetweetedAuthorScreenName, \
    ExcludeByTwitterList

filters = [
    ExcludeByRetweetedAuthorScreenName([]),
    ExcludeByTwitterList([])
]
