import datetime
from dataclasses import dataclass

import coulomb


@dataclass
class Author:
    name: str


class HomePage(coulomb.TemplatedView):
    path = "./"
    template = "HomePage"


site = coulomb.Site(
    views=[
        HomePage
    ],
    models=[
        (Author, "./authors")
    ],
    context={
        "site_name": "Our Site"
    },
)


@site.register_model
class Post:
    title: str
    published: datetime.datetime
    content: coulomb.Content
    author: Author


@site.register_model("./page-bodies")
class Page:
    content: coulomb.Content


class Project:
    started: datetime.date
    published: datetime.datetime


site.register_model(Project)

class Color:
    red: int
    green: int
    blue: int


site.register_model(Color, "./colors")


@site.register_view
class BlogPost(coulomb.TemplatedView):
    path = "./blog/{post.date:%y/%m/%d}/{post.slug}"
    for_each = coulomb.ForEach(
        key="post",
        resource=coulomb.Dynamic(
            model=Post,
            filter=lambda p: p.published is not None
        )
    )
    template = "BlogPost"


class Assets(coulomb.StaticFolderView):
    path = "./static"
    src_dir = "./my-assets"


site.register_view(Assets)
