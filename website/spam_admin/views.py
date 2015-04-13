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
logger = logging.getLogger(__name__)
#from website.project.views.comment import kwargs_to_comment


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


def init_comments():
    """
    make a list of comments that are marked as possibleSpam
    """

    try:
        num_possible_spam_comments = Comment.find(Q('possible_spam', 'eq', True)).count()

        return {'num_possible_spam_comments': num_possible_spam_comments}
    except:
        return {'num_possible_spam_comments':0}


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

# def kwargs_to_comment(kwargs, owner=False):
#
#     comment = Comment.load(kwargs.get('cid'))
#     if comment is None:
#         raise HTTPError(http.BAD_REQUEST)
#
#     if owner:
#         auth = kwargs['auth']
#         if auth.user != comment.user:
#             raise HTTPError(http.FORBIDDEN)
#
#     return comment

def serialize_comments(comments, amount):
    count = 0
    out = []
    for comment in comments:
        out.append(serialize_comment(comment))
        count +=1
        if count >= amount:
            break
    return out

    return [ serialize_comment(comment) for comment in comments]

def mark_comment_as_spam(**kwargs):
    try:
        print "mark comment as spam CALLED!!!!!!!!!"
        #import pdb;pdb.set_trace()
        #comment = kwargs_to_comment(kwargs)
        #print comment

        # comment.unmark_as_possible_spam()
        # comment.delete()
        return {'message': 'comment marked as spam'}
    except:
        #raise HTTPError(http.BAD_REQUEST)
        return {'message': 'failed to mark as spam'}


def mark_comment_as_ham(**kwargs):
    try:
        # comment = kwargs_to_comment(kwargs)
        # comment.unmark_as_possible_spam()
        # comment.delete()
        return {'message': 'comment marked as spam'}
    except:
        #raise HTTPError(http.BAD_REQUEST)
        return {'message': 'failed to mark as spam'}