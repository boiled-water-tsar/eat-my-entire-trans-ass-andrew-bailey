# Tool for submitting data to the Missouri Attorney General Transgender Center Concerns Form - TRANS RIGHTS

Python program using the frankly terrible code of the Missouri Attorney General's office to flood their snitching
website with garbage and noise.

They want us to die but honey, these colors don't run 🏳️‍⚧️🏳️‍⚧️🏳️‍⚧️

## How it's done and a bit of history

In a nutshell: Garbage and noise is generate -> a captcha is solved -> noise is sent to the REST API serving the snitching form.
The program has been through several permutations. From sending the rawest of garbage to sending data specific enough to
MO that it would be a herculean task to sort through.
Security has been attempted implemented and bypassed from nothing (as in, no security at all lmao what were they thinking)
to ensuring an IP could only submit one report to introducing a captcha.
As time goes on I'm sure the MO AGs office will introduce even more security, and we will defeat it all.

## How to use

Strongly consider using a VPN. Submitting millions of false reports may not be illegal, but it might also be wire fraud?
IANAL. For VPNs there's a number of options such as [Cloudflare WARP](https://1.1.1.1) or [Proton VPN](https://protonvpn.com),
and of course there's always Starbucks free WI-FI. 

### Installation

Install Python version 3.10 or higher and pip. You can learn how to at [https://python.org](https://python.org).

Then either clone this repository or download and extract it

Install depedencies
> python3 -m pip install -r requirements.txt

or

> pip install -r requirements.txt

When the dependencies have been installed run the program with

> python3 defend_trans.py

If the program is running successfully you should see output akin to

> Response submitted for Barlett, Eric
> 
> Response submitted for Rivers, Stacey

## How to contribute

Oh god please contribute this is too important to just have me, a dumb idiot, make and handle.
