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

## Steps

### 1 Create a Basic Blog

- Blog must include the following features:
  - [ ] Front page that lists blog posts.
  - A form to submit new entries.
  - Blog posts have their own page.
