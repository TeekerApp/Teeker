# Teeker App

1. - [x] Login Page
2. - [x] Register Page (Sign Up Page)
3. - [ ] Index Page (Home Page)
4. - [ ] Account Visitor Page
5. - [ ] Personal Account Page
6. - [ ] Setting Page
7. - [ ] Search Result Page
8. - [ ] User Management Page (For Staff Access only)
9. - [ ] Recovery Password Page [90% Done]
	- The page works as intended, but need to build a timer to delete the URL after a set time.
10. - [ ] FeedBack Page
11. - [ ] Upload Post Page
12. - [ ] Inbox Page

For other Developers please install [Koala App](http://koala-app.com/) to make your `SCSS` files into `CSS` files. Make sure not to have source map files in the css folder

Need to use the Python version in `runtime.txt`.

Now using Adobe Muse to do the Front-End.

# ERROR's

## Database ERROR's
If a Database Error shows up about `OPTIONS` make these files.
1. `.env` place this inside `DATABASE_URL=sqlite:///db.sqlite3`
2. `.gitignore` place this inside `.env`

## Enviroment ERROR's
If you are having any issues when trying to run a test that involves sending emails or reCAPTCHA v2. Please make sure that you have all enviroment values. If you don't, get them from Sana or go to the Heroku Settings.
