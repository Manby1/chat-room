# chat-room

## Requirements:

Python standard library. For uno, pygame is required.

## Hosting:

Host must port forward to enable access to their server. Note this is the case whenever the user wants to host a server in any game - unless somebody else is hosting for you (Steam).

server.txt is a recommended file so you don't have to type in your IP and Port when opening.
For uno, it should be in the uno folder.
For chat-room, it should be in the chat-room folder.

***

### A more thorough explanation of how send and receive works:

The user wants to send the message 'hel-\uFFFF-lo'. 
They have decided they want to put the unicode character \uFFFF into their message - 
this would never happen though, because it would either be interpreted as single characters or 
they would not be able to type it in. But let's say they did - the \uFFFF would be stripped from 
the message anyways by this code.

The message is put into a tuple where the first element is the message type - 
e.g. M for message, N for name, (E for error?). The second element is their actual message that
they wanted to send - in this case, 'hel--lo'. Their message would become:
('M','hel--lo'). This would be converted into "['M','hel--lo']" by json (into a string object)
and made into a bytes object. Then, the character '\uFFFF' (that was previously stripped from
all of the messages) would be added to the end to signify the end.
b"['M','hel-lo']\uFFFF" would be sent. (b"" is a bytes object).

Let's say two messages were sent rapid-fire. The python sockets module would put them together, so
if the example message would sent twice, the server/client would receive:
b"['M','hel-lo']\uFFFF['M','hel-lo']\uFFFF". After being decoded back into a string from bytes,
this would be split by the end characters '\uFFFF' and made into the list:
["['M','hel-lo']","['M','hel-lo']",""]. Notice the lists are still strings and there is a final
empty element left there because of how the python split function works.
The last element would be ignored, and then the module json would be used to convert the list strings
into actual lists! We would finally have:
[['M','hel-lo'],['M','hel-lo']].

***

### Message characterizations

#### Client -> Server:
* N - Name specification. Sent when connection has ocurred.
* M - Chat message specification - support is currently non-existant for this type of message.
* L - Leave specification. Useful for standard exit procedures - can be otherwise inferred.
* C - Card pick - sent as standard card codes (shown in image files).
* E - Other event, e.g. Wild +4 Challenge - non chat, non card pick.

#### Server -:> Client:
* J - Join event - broadcast a join event with user name, colour, and ID.
* B - Broadcast - Redirection of a chat message - unsupported
* C - Card play - broadcast the most recent move. Send with a player ID and a card play code.
* E - Other event, e.g. Wild +4 Challenge. Similar to Client 'E', but ID is specified.
