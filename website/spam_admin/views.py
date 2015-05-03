# -*- coding: utf-8 -*-


import logging
import http
from modularodm import Q

from framework.exceptions import HTTPError


from website.models import Node



from website.models import Comment
from flask import request
logger = logging.getLogger(__name__)

from framework.utils import iso8601format
from framework.auth.decorators import must_be_logged_in
from .decorators import must_be_spam_admin
from .utils import serialize_comments,serialize_projects
import datetime
import requests
import json

@must_be_logged_in
@must_be_spam_admin
def list_comment_page(**kwargs):
    """
    make a list of comments that are marked as possibleSpam
    """
    try:
        amount = 30
        if 'amount' in kwargs:
            amount *=0
            amount += int(kwargs['amount'])

        comments = Comment.find(
            Q('spam_status', 'eq', Comment.POSSIBLE_SPAM)
        )


        return { 'comments': serialize_comments(comments, amount),
                 'total': comments.count()
            }
    except:
        return {'comments':0,
                'total': 0
        }

@must_be_logged_in
@must_be_spam_admin
def init_spam_admin_page(**kwargs):
    """
    make sure that user is spam_admin
    """

    return {}


@must_be_logged_in
@must_be_spam_admin
def init_spam_admin_comments_page(**kwargs):
    """
    make sure that user is spam_admin
    """

    return {}





@must_be_logged_in
@must_be_spam_admin
def mark_comment_as_spam(**kwargs):
    try:
        cid = request.json.get('cid')

        comment = Comment.load(cid)

        if comment is None:
            raise HTTPError(http.BAD_REQUEST)



        comment.confirm_spam(save=True)

        train_spam(comment=comment, is_spam=True)

        comment.delete(auth=None, save=True)

        return {'message': 'comment marked as spam'}
    except:
        raise HTTPError(http.BAD_REQUEST)


@must_be_logged_in
@must_be_spam_admin
def mark_comment_as_ham(**kwargs):
    try:
        cid = request.json.get('cid')

        comment = Comment.load(cid)

        if comment is None:
            raise HTTPError(http.BAD_REQUEST)

        comment.comment.confirm_ham(save=True)
        train_spam(comment=comment,is_spam=False )


        return {'message': 'comment marked as ham'}
    except:
        raise HTTPError(http.BAD_REQUEST)


@must_be_logged_in
@must_be_spam_admin
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



@must_be_logged_in
@must_be_spam_admin
def mark_project_as_spam(**kwargs):

    try:

        pid = request.json.get('pid')

        project = Node.load(pid)

        if project is None:
            raise HTTPError(http.BAD_REQUEST)

        project.unmark_as_possible_spam( save=True)
        train_spam_project(project,is_spam=True )

        #TODO: delete node. Need high level auth for this.

        return {'message': 'project marked as spam'}
    except:
        raise HTTPError(http.BAD_REQUEST)


@must_be_logged_in
@must_be_spam_admin
def mark_project_as_ham(**kwargs):
    try:
        pid = request.json.get('pid')

        project = Node.load(pid)

        if project is None:
            raise HTTPError(http.BAD_REQUEST)

        project.unmark_as_possible_spam( save=True )
        train_spam_project(project,is_spam=False )

        return {'message': 'project marked as ham'}
    except:
        raise HTTPError(http.BAD_REQUEST)


def train_spam(comment, is_spam):
    try:
        data = {
            'message': comment.content,
            'email': comment.user.emails[0] if len(comment.user.emails) >0 else None,
            'date': str(datetime.utcnow()),
            'author': comment.user.fullname,
            'project_title':comment.node.title,
            'is_spam':is_spam
        }

        r = requests.post('http://localhost:8000/teach', data=json.dumps(data))
        if r.text == "Learned":
            return True
    except:
        pass


def train_spam_project(project, is_spam):
    try:

        serialized_project = _format_spam_node_data(project)
        serialized_project['is_spam']=is_spam

        r = requests.post('http://localhost:8000/teach', data=json.dumps(serialized_project))
        if r.text == "Learned":
            print "------------Learned-----------\n"
            return True
        else:
            print "------------NOT Learned-----------\n",r.text,"\n--------------------------------"
    except:
        pass



def _format_spam_node_data(node):
    from website.addons.wiki.model import NodeWikiPage
    from website.views import serialize_log

    logs = []
    for log in reversed(node.logs):
        if log:
            logs.append(serialize_log(log))

    #node.contributors

    content = {
        'wikis':[wiki.content for wiki in NodeWikiPage.find(Q('node','eq',node))],
        'logs':logs,
        'tags': [tag._id for tag in node.tags]
    }


    data = {
        'message':content,
        'project_title': node.title,
        'category': node.category_display,
        'description': node.description or '',
        'url': node.url,
        'absolute_url': node.absolute_url,
        'date_created': iso8601format(node.date_created),
        'date_modified': iso8601format(node.logs[-1].date) if node.logs else '',
        'date': iso8601format(node.logs[-1].date) if node.logs else '',
        'tags': [tag._id for tag in node.tags],
        'is_registration': node.is_registration,
        'registered_from_url': node.registered_from.url if node.is_registration else '',
        'registered_date': iso8601format(node.registered_date) if node.is_registration else '',
        'registration_count': len(node.node__registrations),
        'is_fork': node.is_fork,
        'forked_from_id': node.forked_from._primary_key if node.is_fork else '',
        'forked_from_display_absolute_url': node.forked_from.display_absolute_url if node.is_fork else '',
        'forked_date': iso8601format(node.forked_date) if node.is_fork else '',
        'fork_count': len(node.node__forked.find(Q('is_deleted', 'eq', False))),
        'templated_count': len(node.templated_list),
        'watched_count': len(node.watchconfig__watched),
        'private_links': [x.to_json() for x in node.private_links_active],
        'points': len(node.get_points(deleted=False, folders=False)),
        'comment_level': node.comment_level,
        'has_comments': bool(getattr(node, 'commented', [])),
        'has_children': bool(getattr(node, 'commented', False)),
        'author': node.creator.fullname,
        'email':node.creator.emails,
        #'contributors': [contributor.name in node.contributors,


    }

    return data