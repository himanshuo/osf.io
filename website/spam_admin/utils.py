from framework.auth.utils import privacy_info_handle
from modularodm import Q


def serialize_comment(comment):

    anonymous = False
    return {
        'author': {
            'url': privacy_info_handle(comment.user.url, anonymous),
            'name': privacy_info_handle(
                comment.user.fullname, anonymous, name=True
            ),
        },
        'dateCreated': comment.date_created.isoformat(),
        'dateModified': comment.date_modified.isoformat(),
        'content': comment.content,
        'hasChildren': bool(getattr(comment, 'commented', [])),
        'project': comment.node.title,
        'project_url':comment.node.url,
        'cid':comment._id
    }

def serialize_comments(comments, amount):
    count = 0
    out = []
    for comment in comments:
        out.append(serialize_comment(comment))
        count +=1
        if count >= amount:
            break
    return out

def serialize_projects(projects, amount):
    count = 0
    out = []
    for project in projects:
        out.append(serialize_project(project))
        count +=1
        if count >= amount:
            break
    return out

def human_readable_date(datetimeobj):
    return datetimeobj.strftime("%b %d, %Y")

def serialize_project(project):
    from website.addons.wiki.model import NodeWikiPage

    return {
        'wikis':[ { 'content': wiki.content if len(wiki.content) < 1000 else wiki.content[:1000]+" ...",
                    'page_name': wiki.page_name,
                    'date': human_readable_date(wiki.date),
                    'url': wiki.url
                  }
                  for wiki in NodeWikiPage.find(Q('node','eq',project)) ],
        'tags': [tag._id for tag in project.tags],
        'title': project.title,
        'description': project.description or '',
        'url': project.url,
        # 'date_created': iso8601format(project.date_created),
        'date_modified': human_readable_date(project.logs[-1].date) if project.logs else '',
        'author':{
            'email':project.creator.emails,
            'name': project.creator.fullname,
        },
         'pid':project._id

    }