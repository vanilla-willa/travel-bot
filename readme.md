# Facebook Messenger Bot
Python template using Flask to build webhook for Facebook's Messenger Bot API cloned from https://github.com/hartleybrody/fb-messenger-bot.

Tutorial from https://blog.hartleybrody.com/fb-messenger-bot/.

# "Instructions"

Work with a virtual environment.

`git clone https://github.com/hartleybrody/fb-messenger-bot`

`pip install -r requirements.txt`

Create a Heroku account, if it doesn't already exist.

Install Heroku CLI Toolbelt using Homebrew: `brew tap heroku/brew && brew install heroku`
Otherwise, follow: https://devcenter.heroku.com/articles/heroku-cli

Track changes in git
`git init`
`git add`
`git commit -m "initial commit"`

See compatible python runtimes: https://devcenter.heroku.com/articles/python-support#supported-runtimes
At the time of writing, Heroku deployment with Python only allowed python-3.7.4, python-3.6.9, python-2.7.16. 
Current webhook requirement uses wsgiref==0.1.2, which is not compatible with python3. 
Update runtime.txt to the latest python2 support: `python-2.7.16`.

Creating Heroku remotes: https://devcenter.heroku.com/articles/git
To create a new Heroku app
Run `heroku create`
Check remote Heroku repositories were set: `git remote -v`

To add local repository to existing Heroku app:
`heroku git:remote -a floating-taiga-21700`

To verify that Heroku can run things locally on your machine, start your local server with: `heroku local`

Launch http://localhost:5000/. Success should show “Hello world” on the page. Kill the local server with Ctrl+C. 

To deploy this endpoint to Heroku: `git push heroku master`

If deployment comes up with errors, check for failed build logs in Heroku Dashboard > app_name > Activity. Click on View build log.

Check success of deployment: `heroku open`


![Facebook Error](https://cloud.githubusercontent.com/assets/18402893/21538944/f96fcd1e-cdc7-11e6-83ee-a866190d9080.png)

The #1 error that gets reported in issues is that facebook returns an error message (like above) when trying to add the heroku endpoint to your facebook chat application.

Our flask application intentionally returns a 403 Forbidden error if the token that facebook sends doesn't match the token you set using the heroku configuration variables.

If you're getting this error, it likely means that you didn't set your heroku config values properly. Run `heroku config` from the command line within your application and verify that there's a key called `VERIFY_TOKEN` that has been set, and that it's set to the same value as what you've typed into the window on facebook.
