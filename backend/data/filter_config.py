
from filter_plugins.excludes import \
    ExcludeByRetweetedAuthorScreenName, \
    ExcludeByTwitterList, \
    ExcludeByWords

filters = [
    ExcludeByRetweetedAuthorScreenName([]),
    ExcludeByTwitterList([]),
    ExcludeByWords([])
]
