import datetime
from dataclasses import dataclass
from typing import Any

import coulomb


def dynamic_setup(site: coulomb.Site) -> dict[str, Any]:
    return {
        "all_authors": [*site.data.get(Author)],
        "links": [*site.data.get(Link)],
    }


site = coulomb.Site(
    component_path="./components",
    discover_html=True,
    context = {
        "site-title": "Piper Thunstrom",
        "all_authors": coulomb.Dynamic('Author'),
        "links": coulomb.Dynamic('Link'),
    },
    # base_path = "/"  # Will default to root, but configurable for when hanging generated sites off a root path
    assets = coulomb.Assets(
        source="./assets",
        destination="./static/"
    )
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
class HomePage(coulomb.View):
    path = "/"
    component = "HomePage"
    context = {
        "body": coulomb.Dynamic(Body, filter=lambda b: b.id == "home", single=True)  # Throw an error if the final output has more than 1.
    }


@site.register_view
class BlogPostPage(coulomb.View):
    for_each = coulomb.Dynamic(Post, filter=lambda p: p.published <= datetime.datetime.now(), context_key="post")
    path = "/blog/{date}/{slug}"
    path_components = [
        PathComponent(
            from_resource="published",
            format_field="date",
            transform=date_path  # Convert date/datetime to "YYYY/MM/DD"
        ),
        PathComponent(
            from_resource="slug"
        )
    ]
    template = "Article"


@site.register_view
class BlogIndexPage(coulomb.View):
    path = "/blog"
    template = "ArticleIndex"
    context = {
        "page_title": "Blog",
        "posts": coulomb.Dynamic(
            Post,
            filter=lambda p: p.published <= datetime.datetime.now(),
            sort_key=lambda p: datetime.date.today() - p.published
        )
    }