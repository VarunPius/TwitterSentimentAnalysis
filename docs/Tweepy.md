# Build a search filter

The first step will be to create a filter that will allow us to search for specific tweets.

The documentation on how to create a filter can be found here and a more advanced tutorial here. I will however mention some information.
— Depending on the type of access you have, probably `Essential` if you are just starting out, you will be limited to creating a filter of 512 characters in length.
— You can use several operators to perform your search, some of the most important are:
    - `AND` which is naturally used by separating the search keywords with a space. 
        For example, if I want a tweet that includes the words `banana` and `potato` (I'm not hungry!) I would build a `banana potato` filter.
    - `OR` if I want a tweet that includes `banana` or `potato`, I would write (`banana OR potato`).
        Note that parentheses are necessary, for example, if you want to search for exact sentences like ("Twitter API" OR #v2).
    - `-` the negation of a search, for example, if I search for tweets that have potato but not banana, I will have a filter `potato -banana`. So a sentence that contains both words will not pass the search.
    - `from:` to search for tweets from a specific account, for example `from:marvel`.
    - `to:` to search for tweets in response to a specific account, for example `to:marvel`.
    - `conversation_id:` In discussion threads, tweets descending from the root tweet will have a conversation_id field to try to reconstruct the whole discussion. This can be used to filter tweets. Example: `conversation_id:1334987486343299072`.
    - `has:` allows you to search for tweets with metadata, for example, a tweet search containing media or links: (`has:media OR has:links`).
    - `is:` allows you to search for different types of tweets such as retweets (`is:retweet`), quotes, or retweets with a message (`is:quote`) or other contextual information such as whether the user is verified (you know the little blue mark that may soon become payable :p) `is:verified`.

For our example, we will search positive messages about the last Marvel movie (at the moment of writing) "Wakanda Forever". The filter will be the following: `("black panther" OR #wakandaforever) (magnificent OR amazing OR excellent OR awesome OR great) -is:retweet`. Normally, you should understand it but let's unpack it, so we look for tweets:
- Having the term *black panther* (for your information the search is case-insensitive) or the hashtag *#wakandaforever*:  `("black panther" OR #wakandaforever)`
- and having one of the following words: *magnificent*, *amazing*, *excellent*, *awesome*, *great*: `(magnificent OR amazing OR excellent OR awesome OR great)`
- and is not a retweet: `-is:retweet`.

This last filter is very important and even recommended in the official documentation because many tweets are often retweets, it avoids adding unnecessary noise in our replies.