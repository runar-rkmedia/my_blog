"""Used for dev-purposes to have some test-data quickly."""
from Entities import BlogEntity,blog_key

def dev_create_some_blog_posts():
    """Generator for random blog posts, for testing in development."""
    for i in range(0, 45):
        a = BlogEntity(
            parent=blog_key(),
            title='Some Title {}'.format(i),
            article="""
            Cernantur lorem sint e nulla, nisi si ea eram quibusdam in doctrina enim
            excepteur, te quae fabulas praetermissum te dolor nam est export nostrud, tempor
            o senserit a sint arbitror exquisitaque ad noster fabulas mandaremus. Cernantur
            ut nisi consequat, lorem mentitum e lorem sint ubi qui cillum hic irure, dolore
            fabulas ut senserit, ad si domesticarum quo o noster se legam ne officia aute
            eiusmod nescius, sunt laboris est minim constias. Amet cohaerescant mandaremus
            magna incurreret. Singulis e aute et laboris fore anim singulis constias an qui
            a adipisicing e hic veniam nostrud probant, cupidatat eram do laboris
            imitarentur e deserunt nisi quis te anim, nam export labore aliqua fabulas ex
            singulis ut malis vidisse.Id duis arbitror arbitrantur, pariatur velit magna an
            nulla si est dolor ad quem an velit ubi quamquam in culpa laborum do constias
            quid o deserunt nisi expetendis, anim mandaremus eu dolore quae, nisi mandaremus
            in familiaritatem. Ab sunt cupidatat probant, ut sint sunt fugiat possumus.
            Quibusdam noster fore te quis et si quem constias ut senserit, o quo
            despicationes e o eu philosophari.

            Quem ubi iudicem, sunt incurreret cernantur. Ab consequat ex voluptate, id minim
            iis tamen a veniam tractavissent voluptate aliqua nescius ne excepteur illum est
            singulis fidelissimae, hic do duis multos legam ut excepteur eram possumus ex
            ipsum fabulas ita iudicem, minim ne deserunt est eram. Ubi quem illustriora non
            do ut cohaerescant est magna ullamco ab incididunt iis te multos fore non
            vidisse.Ea eram te multos quo o tempor praetermissum, litteris ne cupidatat ut
            illum eu singulis sed a nulla deserunt fabulas se excepteur aute eu incurreret
            sempiternum e si ne graviterque in est sed quorum quorum enim. Vidisse aut
            minim. Est fugiat cernantur id amet aut o fugiat tempor, ex velit ea aute, et
            export vidisse.

            Ne elit ea culpa ex magna fabulas ad despicationes non nostrud enim quamquam,
            expetendis philosophari ab nescius, fabulas amet constias mentitum quem, tamen
            cupidatat ne quamquam aut ita nam praesentibus ea nulla do occaecat. Fabulas in
            ipsum. Culpa non officia, quibusdam illum constias te velit ne fore commodo
            ullamco e officia est aliqua probant.Fabulas graviterque hic pariatur ea ad
            dolor anim veniam ingeniis a ingeniis in voluptate, dolore iudicem sed aliqua
            quid, a si eram incurreret, e fore laborum appellat et iis eram tempor
            coniunctione quo constias doctrina ut praetermissum. Appellat sunt nulla id
            duis, o cillum e sunt, voluptate illum et voluptate praesentibus, dolore
            pariatur iis incididunt. Export voluptate est sempiternum quo nulla quibusdam ad
            adipisicing, arbitror quae sunt singulis illum, eu mandaremus ne arbitror.
            Quamquam quorum dolor singulis minim, nescius quorum appellat mentitum.
            """
            )
        a.put()
dev_create_some_blog_posts()
