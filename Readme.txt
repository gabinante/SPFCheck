README

This project is intended to take a list of domains associated with customer number or some other identifying piece of information, then run validation on SPF records for all of those domains. It will then spit out a list of 
customers which failed validation.

If you send a bunch of email using SPF, this is useful because it gives you some agency in protecting your IP reputation. Otherwise you rely upon other  IT/Network teams to not mess things up.

You’ll need to edit the IP addresses hard-coded in the script and then create a CSV (mysql INTO OUTFILE or whatever).

This project uses PySPF to do record validation. You can find the latest version of PySPF here: https://pypi.python.org/pypi/pyspf/