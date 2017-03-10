"""Used for dev-purposes to have some test-data quickly."""
from random import randint
from Entities import BlogEntity, blog_key, UserEntity
import myExceptions

UserEntity.register(username='Johnny', password='pass')
UserEntity.register(username='Jake', password='pass')
UserEntity.register(username='James', password='pass')
UserEntity.register(username='Jimmy', password='pass')
UserEntity.register(username='Joe', password='pass')
UserEntity.register(username='Jane', password='pass')
UserEntity.register(username='Jueliette', password='pass')
UserEntity.register(username='July', password='pass')


title_list = [
    'Id ex est cupidatat aliqua reprehenderit magna tempor.',
    'Ea sint fugiat amet nulla reprehenderit nostrud esse deserun.',
    'Pariatur ut consequat cupidatat exercitation ullamco eiusmod officia.',
    'Cillum incididunt ullamco adipisicing aute dolore amet adipisicing.',
    'Ut sit magna duis est eiusmod incididunt deserunt ea elit sunt amet.',
    'Laborum non enim quis fugiat culpa fugiat dolore consequat laboris.',
    'Cupidatat minim enim consequat laboris aute elit et excepteur nisi officia.',
    'Anim non ipsum labore enim consectetur pariatur laborum officia.',
    'Nisi aliquip tempor qui labore occaecat id deserunt et.',
    'Eu deserunt adipisicing laborum sint labore proident ipsum.',
    'Eiusmod dolore cupidatat pariatur anim deserunt voluptate minim non enim.',
    'Eiusmod velit proident minim amet exercitation sunt duis.'
]

article_paragraphgs = [
    """Deserunt dolore do cillum irure ipsum ea anim. Enim aute esse minim consectetur id velit tempor. Cillum fugiat non commodo nisi ut irure Lorem exercitation.""",  # noqa
    """Occaecat id mollit laboris proident cillum adipisicing culpa quis aliquip sint veniam. Quis nisi qui laboris do aute ut deserunt ullamco. Pariatur ex nostrud aliquip cillum et consectetur ipsum in tempor in. Deserunt culpa adipisicing adipisicing officia ullamco ea eu mollit aliqua.""",  # noqa
    """Officia ipsum sit mollit adipisicing duis est officia. Labore occaecat dolore ea velit dolore magna deserunt dolore excepteur labore. Exercitation nostrud officia ea qui qui et in nostrud. Quis minim adipisicing est ut proident ut ut tempor nulla exercitation id.""",  # noqa
    """Ex eu incididunt sint sint voluptate eiusmod aute amet minim fugiat nostrud. Sunt nostrud velit do mollit anim esse nostrud incididunt id. Cupidatat sit enim Lorem ut commodo labore enim magna fugiat labore sunt.""",  # noqa
    """Eu velit ut laborum dolor in velit consectetur. Lorem elit adipisicing cupidatat ex aliqua exercitation ex duis anim. Officia magna dolor in enim eu sit nulla pariatur. Tempor labore velit commodo est occaecat nostrud ullamco elit nostrud occaecat anim.""",  # noqa
    """Qui ea voluptate ut sit qui velit duis irure. Id nostrud deserunt ipsum duis do officia voluptate ullamco Lorem excepteur laboris. Minim ullamco id aliquip labore excepteur proident dolore cupidatat est laborum laboris.""",  # noqa
    """Cillum ex qui ex est laborum aute duis officia. Anim id mollit ullamco id do eu amet. Magna pariatur magna occaecat quis ut proident sunt aliqua anim deserunt. Aliqua nulla pariatur excepteur ullamco velit voluptate fugiat irure sint.""",  # noqa
    """Cillum est dolore deserunt aliquip mollit consectetur ea duis. Ut nostrud ut nisi non culpa irure magna cupidatat dolore. Esse exercitation consectetur quis nisi pariatur sint elit ullamco ad aliqua.""",  # noqa
    """Consequat amet sunt culpa pariatur do ullamco laboris eiusmod. Do dolore anim incididunt eu aute nostrud sint mollit. Consectetur anim aute enim minim consectetur ad irure.""",  # noqa
    """Est elit est veniam nisi laboris aliqua id nulla culpa. Mollit amet fugiat do fugiat dolor nisi tempor voluptate Lorem incididunt laborum. Ullamco laboris ullamco ex cillum nulla non labore mollit.""",  # noqa
    """Aute duis proident adipisicing aliqua esse dolore ad. Tempor ad voluptate consectetur excepteur do esse tempor laborum esse labore sint. Qui ullamco tempor nulla irure officia tempor amet consequat et.""",  # noqa
    """Occaecat officia consequat mollit occaecat voluptate nostrud adipisicing est aute quis laborum. Lorem ex velit excepteur officia sunt non laborum aliquip ea. Est tempor Lorem excepteur ipsum exercitation deserunt consectetur aliqua id.""",  # noqa
    """Est esse excepteur ea nostrud nostrud nostrud labore ut nostrud tempor. Dolore elit pariatur deserunt excepteur ut nisi reprehenderit velit. Aute id amet nostrud cillum in esse esse aute consectetur cillum."""  # noqa
]


def pick_random_from_list(theList):
    """Return a random item from the list."""
    return theList[randint(0, len(theList) - 1)]


def get_random_entity(users):
    """Return a random item from the entity."""
    return users[randint(0, users.count() - 1)]


def dev_create_some_blog_posts(users):
    """Generator for random blog posts, for testing in development."""
    for i in range(1, 46):
        article = ""
        article += "<h3>{}</h3>".format(pick_random_from_list(title_list))
        for j in range(0, randint(4, 8)):
            if j > 0:
                if randint(0, 5) == 1:
                    article += "<h4>{}</h4>".format(
                        pick_random_from_list(title_list))
            article += "<p>{}</p>".format(
                pick_random_from_list(article_paragraphgs))
        a = BlogEntity(
            parent=blog_key(),
            created_by=users[randint(0, users.count() - 1)],
            title='{} {}'.format(i, pick_random_from_list(title_list)),
            article=article)
        a.put()


def assign_random_votes(blog_entries, users):
    """Assign random votes to articles."""
    for blog_entry in blog_entries:
        for user in users:
            try:
                blog_entry.vote(voteBy=user,
                                voteType=pick_random_from_list(['up', 'down']))
            except myExceptions.VoteOnOwnPostNotAllowed:
                pass


user_list = UserEntity.all()
blog_entry_list = BlogEntity.all()

dev_create_some_blog_posts(user_list)
assign_random_votes(blog_entry_list, user_list)
