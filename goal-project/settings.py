import datetime
import pathlib
from dataclasses import dataclass

import coulomb


site = coulomb.Site(
    component_path="./components",
    discover_html=True,
    context = {
        "site-title": "Piper Thunstrom",
        "all_authors": coulomb.Dynamic('Author'),
        "links": coulomb.Dynamic('Link'),
    },
    # base_path = "/"  # Will default to root, but configurable for when hanging generated sites off a root path
)


@site.register_model("data/Body")
@dataclass
class Author:
    name: str
    short_name: str
    email: str
    avatar: str
    bio: coulomb.Content
    id: str = None


@site.register_model("data/Body")
@dataclass
class Body:
    content: coulomb.Content
    id: str = None


@site.register_model("data/Header")
@dataclass
class Header:
    path: str
    alt: str
    id: str = None


@site.register_model("data/Link")
@dataclass
class Link:
    title: str
    url: str
    img: str
    priority: int
    id: str = None


@site.register_model("data/Post")
@dataclass
class Post:
    title: str
    slug: str
    author: Author
    header: Header
    summary: str
    published: datetime.date
    content: coulomb.Content


@site.register_view
class HomePage(coulomb.TemplatedView):
    path = "/"
    template = "HomePage"
    context = {
        "body": coulomb.Dynamic(Body, filter=lambda b: b.id == "home", single=True)  # Throw an error if the final output has more than 1.
    }


@site.register_view
class BlogPostPage(coulomb.TemplatedView):
    path = "/blog/{post.date:%y/%m/%d}/{post.slug}"
    for_each = coulomb.ForEach(
        key="post",
        resource=(post for post in site.data.query(Post) if post.published <= datetime.datetime.now())
    )
    template = "Article"


@site.register_view
class BlogIndexPage(coulomb.TemplatedView):
    path = "/blog"
    template = "ArticleIndex"
    context = {
        "page_title": "Blog",
        "posts": (post for post in site.data.query(Post, sorted=lambda p: datetime.date.today() - p.published))
    }


@site.register_view
class Assets(coulomb.StaticFolderView):
    path = "/static"
    src_dir = pathlib.Path("assets")
