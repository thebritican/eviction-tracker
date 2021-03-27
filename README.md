# Eviction Tracker

Currently helping verify detainer warrant data for middle Tennessee - via Middle TN DSA - Red Door Collective

## Features

### Phone Number Verification

🚧 [Under Construction](/projects/1) 🚧 

## Development

### Setup

You'll need to set a few secret environment variables before booting the app.

You can copy-paste the following lines into your terminal if you're using bash.

```bash
echo 'export TWILIO_ACCOUNT_SID=fake' >>~/.bash_profile
echo 'export TWILIO_AUTH_TOKEN=fake' >>~/.bash_profile
```

Then, you can either run `source ~/.bash_profile` or open a new terminal tab and proceed to the next step.

> If you're wondering what the above code does: it defines two environment variables with the value "fake" and ensures they are available in all future (bash) shell sessions. TODO: make this process less painful.

#### Nix

Nix is a tool we use to ensure reproducable builds and deployments. Python's default build and deployment system is notoriously tricky.
We've elected to use Nix instead to ease setup. Nix can be used for installing and deploying multiple languages, which may end up being useful for this project.

##### Install Nix

Please follow the instructions to install [Nix on their website](https://nixos.org/download.html#nix-quick-install).

(Please ignore instructions regarding **NixOS** - that's a whole new operating system).

##### Using Nix

To work with the same python version as everyone else working on this project, you'll need to make sure you're in the `nix-shell` first.

1. Check that you're in the same directory as `shell.nix`
2. Type `nix-shell` and hit enter
3. Wait for necessary dependencies to install from the internet to your machine

You'll get a new prompt that looks like:

```
[nix-shell:~/some/path/eviction-tracker]$ 
```

Now you're ready to run `python` and `ipython`! You can escape the `nix-shell` at any time by holding ctrl pressing the D key or typing `exit` and pressing enter.

#### Database

We use [PostgreSQL](https://www.postgresql.org/) for both development and production so that we can be assured working with the data locally will work exactly the same in production. Unfortunately, this requires a bit more manual setup for developers who don't already use Postgres.

##### First-time postgres

Install postgres with the [most convenient installer for your OS](https://www.postgresql.org/download/).

The app doesn't care how you set up your postgres connection, so feel free to set up your postgres service in whatever method is convenient for you. By default, the `SQLALCHEMY_DATABASE_URL` is set to `postgresql+psycopg2://eviction_tracker@localhost/eviction_tracker`, which assumes that you've created a database called `eviction_tracker`, a user called `eviction_tracker` (without a password), and that you are using the default host and port of a postgres service running on the same host as the app.

Feel free to override this environment variable like `SQLALCHEMY_DATABASE_URL="..." flask shell` or create the same setup locally. If you're running your database on another host like a Docker container, you'll need to change `localhost` and possibly add a `:port` to your override.

Some postgres instructions on setting up for the default flow:

```bash
psql -U postgres # or, the superuser you've set up. -U postgres is default for modern installs
```

The above command will place you in this postgres shell:
```
postgres=# CREATE DATABASE eviction_tracker;
postgres=# CREATE USER eviction_tracker;
postgres=# GRANT ALL ON eviction_tracker to eviction_tracker;
```

These commands create the database, user, and assign all privileges for the user to the development database;

#### Migrations

Make sure to run `flask db upgrade` after setting up your database, or whenever a new migration is added to the `migrations/` folder.

#### Google Spreadsheets

You'll need authentication to make requests to the online spreadsheet with the most current data.

Please install [Keybase](https://keybase.io/), a secure messaging platform. I will send any contributor who requests the authentication secrets the necessary file. When I send the file over Keybase, you'll need to download it, and move it somewhere you won't lose it.

By default, our scripts expect the file to be at the following path: `~/.config/gspread/service_account.json`. In plain english: it should be in your home directory, under a hidden folder named `.config` and finally inside another folder called `gspread`. The file should be named `service_account.json`. If these are all true, you're good to go! If you'd like to save the file elsewhere or rename it, just run the script with your custom path under the optional argument: `--service_account_key=/path/to/your/file.json`.

### Using a REPL

REPL (Read Eval Print Loop) is a concept implemented in many programming languages. If you've never written python before, we recommend spending an afternoon on [these basics](https://developers.google.com/edu/python). You'll interact with a REPL in those courses. 

While in a [Nix Shell](#using-nix), launch the IPython shell like so:

```
ipython
```

And now, you can write python code with any of our libraries!

### Running commands

While in a [Nix Shell](#using-nix), run `flask <name-of-command>`.

#### Sync database

To sync the data from our org's Google Spreadsheet, run `flask sync <spreadsheet-name>`.

If you want just a bit of data to work with locally, pass the `--limit` argument.

Example: `flask sync --sheet-name 'detainer-warrants_15-02-2020' --limit 10` will populate the database with 10 detainer warrants from the spreadsheet titled `detainer-warrants_15-02-2020`.

#### Run app

To run the website locally, use `flask run --no-reload` within the `nix-shell`.

You'll be able to visit it at http://127.0.0.1:5000/

You can browse api endpoints like detainer warrants at http://127.0.0.1:5000/api/v1/detainer-warrants