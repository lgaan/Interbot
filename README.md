# Interbot

Interbot is a do-it-all bot originally made for the [Interbyte Studios discord server](https://discord.gg/jR8U94Vu6b).

This repo contains the code for this bot, allowing you to contribute or run your own instance.


# Running

To run the bot there are a few things you'll need:

- Python v3.8.5 or above.
- PostgreSQL
- Git
<hr>

First, you'll need to install the python packages used in the project, this can be done via:

```shell
python -m pip install -U -r config/requirements.txt
```

Now we will need to update the config vars in `config/config.toml` (Create this using the template config)
<hr>

To run the bot, simply type from the base directory:
```shell
python main.py
```

Before the bot will run properly, we will need to create a database and our tables within it.
You can find some good videos on YouTube to teach you how to do so.

Once your database is up and running, type the following command into a channel the bot can see:

```shell
[prefix]jishaku py await _bot.db.executemany(open("config/schema.sql").read().split("|"))
```

The bot will now be running!