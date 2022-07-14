# Steps to run

## Install the required libraries

It would be best to use a virtual environment, but not required. Copy this into your terminal to download the required packages.

```
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Make sure you have your credential file

You will need to create a project and give it access to "Admin SDK API" in the developer portal.

```
APIs & Servies -> Enabled APIs & Services -> Search for "Admin SDK API" -> Enable
```

Then create OAuth credentials and download the JSON file. Save that JSON file in your directory where you will be running the script. Rename the file to "credntials.json".

## Run the python script

Now we can just run our script to see if it works.

```
python3 example.py
```

If it worked, you will see a JSON style (dictionary) output in your terminal.
We then will need to parse that information to get what we want.
