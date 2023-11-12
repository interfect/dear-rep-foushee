# Dear Rep. Foushee

A tool for sending messages to Valerie Foushee, representative of North Carolina's 4th District in the U.S. House of Representatives.

# How do I use it?

1. Install Git. Mac should already have it. On Windows, you can use [Git for Windows](https://gitforwindows.org/).

2. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository).

3. Install Python. Mac, again, should already have it. On Windows, you can use [the Python Windows installer](https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe).

4. Execute the `dear-rep-foushee.py` Python script with Python.

5. Fill out your details when the script prompts you in its terminal window. Your information will be saved in `user-data.json` next to the script and will be re-used. After typing each value and pressing enter, type `y` and then enter to accept it, or `n` and then enter to try again.

6. Review the proposed message. If you want to send a different message, make `subject.txt` and `message.txt` next to the script, and run it again. They will be loaded and provide your message text and subject. Note that your message will always be in the "International Affairs" category.

7. Approve sending the message by typing `y` and pressing enter.

8. Make sure the script says that the message was accepted. **If your message is not accepted, figure out why and fix it! Do not blithely send unmanageable numbers of unwanted messages to a U.S. Government computer system!** It is probably some kind of illegal, and it is definitely unwanted.

# Why does this exist?

I've been asked to contact my congresspeople every day to demand that they solve the ongoing humanitarian crisis in Gaza.

I am a computer programmer and I have a religious objection to doing things by hand.

Rep. Foushee helpfully maintains an apparently standard-compliant GraphQL endpoint, implementing a [`SubmitGravityFormsForm` (later renamed to `SubmitGForm`) Mutation](https://github.com/AxeWP/wp-graphql-gravity-forms/blob/develop/docs/submitting-forms.md#submitting-forms), which she uses to back her public contact form. Anyone can submit their comments to this endpoint and have them added to the (as of this writing) 4,909 comments that Rep. Foushee's system reports having.

While Rep. Foushee's provided contact page application only works if you complete a Google reCAPTCHA test to demonstrate that Google considers you human, and moreover requires you to [agree to this contract with Google](https://policies.google.com/terms?hl=en) in order to use it, Rep. Foushee has chosen not to require other applications interacting with her GraphQL API to impose this requirement on their users.

Dear Rep. Foushee allows constituents to contact Rep. Foushee, as conveniently as can be, without forming any contract with any private company, provided that it is used for Good (see **May I use it?** below).

# How does it work?

**All traffic from this script includes a `User-Agent` header of `dear-rep-foushee.py 1.0`**, meaning that it can easily be blocked if desired.

The system submits a POST request to Rep. Foushee's `https://foushee.house.gov/graphql` endpoint, with an `application/json` content type.

The request's body is JSON, in this format:

```
{
    "query": "mutation SubmitGravityFormsForm($formId: Int!, $clientMutationId: String, $fieldValues: [FieldValuesInput]) {\n  submitGravityFormsForm(\n    input: {formId: $formId, clientMutationId: $clientMutationId, fieldValues: $fieldValues}\n  ) {\n    entryId\n    errors {\n      id\n      message\n    }\n  }\n}\n",
    "variables": {
        "formId": 21,
        "clientMutationId": "1699824671000",
        "fieldValues":[
            {
                "id": 1,
                "value": "This is the subject of my message to Rep. Foushee."
            },
            {
                "id": 2,
                "value": "This is the body of my message to Rep. Foushee.\nHopefully she will read it."
            },
            {
                "id": 5,
                "addressValues": {
                    "country": "USA",
                    "street": "123 Wherever St.",
                    "city": "Durham",
                    "state": "NC",
                    "zip": "27713-1234"
                }
            },
            {
                "id": 7,
                "nameValues": {
                    "prefix": "Mx.",
                    "first": "Yourname",
                    "last": "Here"
                }
            },
            {
                "id": 8,
                "emailValues": {
                    "value": "your@email.here"
                }
            },
            {
                "id": 10,
                "checkboxValues": []
            },
            {
                "id":16, "value": "International Affairs"
            }
        ]
    }
}
```

If all goes well, the server accepts your message to Rep. Foushee, and returns a status code of `200` and a reply like the following:

```
{"data":{"submitGravityFormsForm":{"entryId":4908,"errors":null}},"extensions":{"debug":[{"type":"DEBUG_LOGS_INACTIVE","message":"GraphQL Debug logging is not active. To see debug logs, GRAPHQL_DEBUG must be enabled."}]}}
```

If Rep. Foushee does not want your message, presumably an error will be returned. You may be required to consult or obey any error message returned. **Do not do any computer crimes!**

# May I use it?

`dear-rep-foushee.py` is licensed under the JSON License (see the `LICENSE` file). This means that it must only be used for Good. It may not be used for Evil.

But you don't just have to ask me; you also need to worry about Rep. Valerie Foushee.

As of this writing, [Rep. Foushee's `robots.txt` file](https://foushee.house.gov/robots.txt) provides permission for all automated programs to interact with all parts of Rep. Foushee's web site:

```
User-agent: *
Allow: /

# Host
Host: https://foushee.house.gov

# Sitemap
Sitemap: https://foushee.house.gov/sitemap.xml
```

Since Dear Rep. Foushee is mostly an interactive tool, it doesn't itself check `robots.txt`. You are encouraged to do so if you intend to use this script in an automated way, and to continue to check it on a regular basis to see if Rep. Foushee has decided to change it.

# How would I automate it?

**Do not** automate using this script without checking [Rep. Foushee's `robots.txt` file](https://foushee.house.gov/robots.txt) to see if she has asked that you not do so.

If you have a Mac or Linux computer, after you have sent an initial message, you can [use a cronjob to automate](https://ostechnix.com/a-beginners-guide-to-cron-jobs/) contacting Rep. Valerie Foushee every day to express your thoughts.

You can run `crontab -e` in the terminal, and add a line like this to the file it opens:

```
# At 13:00 (i.e. 1 PM) every day, send your message to Rep. Valerie Foushee.
0 13 * * * cd /path/to/the/directory/with/the/script && ./dear-ref-foushee.py
```

Remember to replace `/path/to/the/directory/with/the/script` with the full path to the directory the script is in, which can be gotten with the `pwd` command if you are in the right directory in the terminal.

If you set this up, make sure that your computer is on and in the Internat at the appropriate time, and that `message.txt` and `subject.txt` are always up to date. Also, pick a different time than 13:00, because if everyone sends an automated message at that time, it might break Rep. Foushee's system, which would, to reiterate, **be illegal**.

To stop sending periodic messages, do `crontab -e` again and remove the line you added.


