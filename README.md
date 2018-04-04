# pygame-base-template
pygame base template: mouse clicks, text input, simple class for objects.

I started out learning pygame and had a miserable time because the stuff I read and
tried to emulate either - didn't have this basic structure, or assumed I'd already know it:

import  
--class setup  
---functions  
-----main loop, consisting of:  
--------update screen  
----------use object class to move objects 1 step  
-------------draw to screen  
--------------check for input  
--------------repeat

Yep, thats not At All what my first creations looked like. That's exactly what this template looks like.
A happy 'hello world' moves towards whatever coordinates you set in it's class definition. The 'SimpleObject'
class contains (as seen in the screenshot) vars for current position, target (to move towards), speed. There's
even a function to easily create a text object/('surface').  The event loop checks for
mouse clicks and is already prepared to do stuff if user clicks on an object, or just return coordinates
if they don't. The main loop is also listening for keyboard keys. Pressing 'f' will toggle you in or back out of
full-screen mode.  Pressing 't' will bring up a prompt to enter text.  Pressing 'q' will immediately quit.  
Check out the picture:


![](https://darknesseverytime.live/mirror/pygame%20boilerplate.png)


I made this script as a sort of 'boilerplate' template that has all the basic functionality required to
just launch into making something.  There's even onscreen text input now, thanks to pygame_textinput at  
https://github.com/Nearoo/pygame-text-input  
The script is included here, or you can go there for any newer version.

Read the code for helpful BS comments too. I hope it helps somebody like me along the way.
