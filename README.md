# Udacity Project: Multi-Usrer Blog

This is part of an assignment in the Full-Stack-course at Udacity. The goal is to create a multi-user-blog, deployed using Google App Engine.

## Installation

### Prerequesites

- [Install Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
- Also, [py-bcrypt by erlichmen](https://github.com/erlichmen/py-bcrypt/) is needed, but I have included the currect version of it as of writing inside the `lib`-folder. This uses `bcrypt`, which is more secure. However, since Google App Engine does only allow native python, we cannot use the standard bcrypt-library which is a lot faster than this. I`m using it here more for a proof-of-concept for myself. For more information, see the link above.

To run the project, clone it and terminal into the directory and do the following command:

```
dev_appserver.py .
```

### 1 Create a Basic Blog

- Blog must include the following features:
  - [ ] Front page that lists blog posts.
  - [X] A form to submit new entries.
  - [X] Blog posts have their own page.

### 2: Add User Registration

- [X] Have a registration form that validates user input, and displays the error(s) when necessary.
- [X] After a successful registration, a user is directed to a welcome page with a greeting, “Welcome, [User]” where [User] is a name set in a cookie.
- [X] If a user attempts to visit the welcome page without being signed in (without having a cookie), then redirect to the Signup page.

### 3: Add Login

- [X] Have a login form that validates user input, and displays the error(s) when necessary.
- [X] After a successful login, the user is directed to the same welcome page from Step 2.

### 4: Add Logout

- [X] Have a logout form that validates user input, and displays the error(s) when necessary.
- [X] After logging out, the cookie is cleared and user is redirected to the Signup page from Step 2.

### 5: Add Other Features on Your Own
- [ ] Users should only be able to edit/delete their posts. They receive an error message if they disobey this rule.
- [ ] Users can like/unlike posts, but not their own. They receive an error message if they disobey this rule.
- [ ] Users can comment on posts. They can only edit/delete their own posts, and they should receive an error message if they disobey this rule.


### 6: Final Touches

- [ ] Create a README.md file explaining how to run your code.
- [ ] Refactor your code so it is well structured, well commented, and conforms to the Python Style Guide.
- [ ] Make sure your project conforms to the rubric.
- [ ] Deploy your app to appspot.com using gcloud app deploy.
- [ ] Submit your project.
- [ ] Revise your project and resubmit as necessary.
- [ ] Pat yourself on the back!
