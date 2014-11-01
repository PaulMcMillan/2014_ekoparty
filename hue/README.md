There are 3 parts to this process:

 * Generate requests
 * Capture data
 * Analyze data

The analysis step feeds back into the request generation to start with
new data.

You should probably watch the video from my ekoparty talk before
trying to run this. I'll add a link here when it gets posted. In the
meantime, you can read the slides (and the speaker notes) to get a
sense of how this works.

This depends on scipy and matplotlib and requests and some other
things I'm sure I've forgotten. You'll also need to download my fork
(yeah, it's a bunch of ugly hacking) of dpkt into this directory.

https://github.com/PaulMcMillan/dpkt/commit/4a050ef2443908c7d5c0614c7b7dfef0fb70a8d0

Follow the suggestions in the slides to quiet down all the various
sources of noise in your machine before you start. It's sensitive
enough that I can't even run my speaker slides from the machine
running the attack without introducing measurable noise. You might
want to have a dedicated machine or a dedicated OS install to work on
this with. I turned off hyperthreading and all power management in the
BIOS, which helps a lot. Don't forget to turn off power management in
the OS, and set everything to the highest performance configuration
possible. Run the attack with the machine plugged in.

There's a bunch of stuff in here that's hardcoded for the demo machine
so it doesn't fail. You'll need to configure a network interface that
has an address in the 192.254.x.x range, as well as answering on
208.67.222.222 (to block opendns requests). You'll have to go replace
all occurances of eth4 with whatever you're using.

Once you've done that, run `capture.sh` to start dnsmasq for 30
seconds. Reset your Hue, and allow dnsmasq to give it an IP and answer
the DNS query it needs to make. After 30 seconds, dnsmasq will stop
and tcpdump will start. Make sure you've got a version of tcpdump that
supports hardware timestamps. See the preso and speaker notes for more
details.

Now, run the `reset_users.py` script to add the user you'll attack to
the Hue. It saves the created username in this directory, so you can
double-check and watch how the script is progressing. It also removes
all other users from the hue.

Run `make clean` for luck and because you probably forgot to do it
after you were messing around last time.

Once that's done, run `collect_data.py` in a new terminal to actually
start the attack. You'll probably have to adjust your "keep_point"
values at the top of `calculate_guess.py` to reflect your hardware and
device.

Once you've collected a few thousand points, uncomment the "return
True" in that function, and run `vis_graph3.py` to graph out the
points you've collected. You should be able to zoom in to find the
least noisy area in that line, and set the bounds in `keep_point()`
accordingly. See the pictures in the preso dir and the ekoparty video
for more details on what that looks like. This graphing tool can be
handy to evaluate and troubleshoot sources of external noise. I'm
sorry about all the external dependencies.

`make clean` again (you don't have to restart the capture when you do
this, ignore the errors there), and then restart `collect_data.py`. If
you've done everything right, you should see it collect data, and
every 3k data points, run an analysis pass.

After a few thousand points per character in the attack set, if
everything is going well, it should choose the next guess, clean up
your data, and start again. If it takes more than 15k samples per
guess, you've got something tuned wrong. Make sure it hasn't
mis-chosen the next character (evidenced by lots of samples, and few
or no detected differences) or gotten to a bad place with the
heuristic (evidenced by the correct answer having very very low
p-values, but the script doesn't move on). You might want to fiddle
with the default p-value (0.1), but if you do that, you'll need to
modify the choice heuristic. You may need to do that anyway - going
for a higher p-value will require more samples (and thus more time)
but should make the process more reliable if you're not trying to do
it all on stage in a 50 minute talk slot.

For examples of what a successful run looks like, see the ekoparty
video, and the SUCCESS1 and SUCCESS2 files in the preso dir.

If you get this running (or if you're having problems), PLEASE shout
at me on twitter [@PaulM](https://twitter.com/PaulM) or drop me an
email (first @ last .ws).

This produces a slightly quieter output if you don't have any powered
(plugged in) hue bulbs nearby. Start with that, then move back to
making it work with the bulbs. The location of the sweet spot is very
dependent on how the device is configured - use the reset it to get
consistency while you develop your attack.

I'm sorry about the misleading bits of dead code. I'd love to clean it
up more, but this is research code, not production grade stuff, so the
evolution of the technique shows. I hate people who don't publish
their code because it isn't pretty. Don't be that guy.

Uses the standalone SSDP library by Dan Kraus, available at:
https://gist.github.com/dankrause/600024