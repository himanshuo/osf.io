# -*- coding: utf-8 -*-

import json
import httplib
import logging
import http
from modularodm import Q
from modularodm.exceptions import ModularOdmException

from framework.exceptions import HTTPError

from website import settings
from website.models import Node
from website.util import web_url_for

from website.conferences import utils

from website.models import Guid, Comment
import pprint
from framework.auth.utils import privacy_info_handle
from website.filters import gravatar
from flask import request
logger = logging.getLogger(__name__)
from website.project.views.comment import train_spam
from website.project.views.node import _format_spam_node_data
#from website.project.views.comment import kwargs_to_comment
from framework.utils import iso8601format




def list_comment_page(**kwargs):
    """
    make a list of comments that are marked as possibleSpam
    """
    try:
        amount = 30
        if 'amount' in kwargs:
            amount *=0
            amount += int(kwargs['amount'])

        comments = Comment.find(Q('possible_spam', 'eq', True))

        return { 'comments': serialize_comments(comments, amount),
                 'total': comments.count()
            }
    except:
        return {'comments':0,
                'total': 0
        }


# def init_comments():
#     """
#     make a list of comments that are marked as possibleSpam
#     """
#
#     try:
#         num_possible_spam_comments = Comment.find(Q('possible_spam', 'eq', True)).count()
#
#         return {'num_possible_spam_comments': num_possible_spam_comments}
#     except:
#         return {'num_possible_spam_comments':0}


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


def mark_comment_as_spam(**kwargs):
    try:
        cid = request.json.get('cid')

        comment = Comment.load(cid)

        if comment is None:
            raise HTTPError(http.BAD_REQUEST)

        comment.unmark_as_possible_spam(auth=None, save=True)
        train_spam(comment=comment,is_spam=True )
        comment.delete(auth=None)
        return {'message': 'comment marked as spam'}
    except:
        raise HTTPError(http.BAD_REQUEST)
        #return {'message': 'failed to mark as spam'}


def mark_comment_as_ham(**kwargs):
    try:
        cid = request.json.get('cid')

        comment = Comment.load(cid)

        if comment is None:
            raise HTTPError(http.BAD_REQUEST)

        comment.unmark_as_possible_spam(auth=None, save=True)
        train_spam(comment=comment,is_spam=False )

        return {'message': 'comment marked as ham'}
    except:
        raise HTTPError(http.BAD_REQUEST)
        #return {'message': 'failed to mark as spam'}


def list_projects_page(**kwargs):
    """
    make a list of projects that are marked as possibleSpam
    """

    try:
        amount = 10
        if 'amount' in kwargs:
            amount *=0
            amount += int(kwargs['amount'])

        projects = Node.find(
                    Q('possible_spam', 'eq', True) &
                    Q('category', 'eq', "project")
        )

        return { 'projects': serialize_projects(projects, amount),
                 'total': projects.count()
            }
    except:
        return {'projects':0,
                'total': 0
        }


def serialize_project(project):
    from website.addons.wiki.model import NodeWikiPage
    return {
        'wikis':[wiki.content for wiki in NodeWikiPage.find(Q('node','eq',project))],
        'tags': [tag.content for tag in project.tags],
        'title': project.title,
        'description': project.description or '',
        'url': project.url,
        'date_created': iso8601format(project.date_created),
        'date_modified': iso8601format(project.logs[-1].date) if project.logs else '',
        'author':{
            'email':project.creator.emails,
            'name': project.creator.fullname,
        }

    }

