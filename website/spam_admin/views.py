# -*- coding: utf-8 -*-
from modularodm import Q
from framework.exceptions import HTTPError
from website.models import Node
from website.models import Comment
from framework.auth.decorators import must_be_logged_in
from .decorators import must_be_spam_admin
from .utils import serialize_comments,serialize_projects, train_spam_project, train_spam
from flask import request
import logging
import httplib as http

logger = logging.getLogger(__name__)



@must_be_logged_in
@must_be_spam_admin
def init_spam_admin_page(**kwargs):
    """
    determine whether use is on comments page or projects page
    """
    return {}


################################### COMMENTS ############################################################

@must_be_logged_in
@must_be_spam_admin
def init_spam_admin_comments_page(**kwargs):
    """
    determine whether use is on comments page or projects page
    """
    return {}


@must_be_logged_in
@must_be_spam_admin
def list_comment_page(**kwargs):
    """
    make a list of comments that are marked as possibleSpam
    """
    try:
        amount = 30

        if 'amount' in kwargs:
            amount = int(kwargs['amount'])

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
def mark_comment_as_spam(**kwargs):
    try:

        cid = request.json.get('cid')
        auth = kwargs.get('auth') or None
        comment = Comment.load(cid)

        if comment is None:
            raise HTTPError(http.BAD_REQUEST)



        comment.confirm_spam(save=True)

        train_spam(comment=comment, is_spam=True)

        comment.delete(auth=auth, save=True)

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

        comment.confirm_ham(save=True)
        train_spam(comment=comment,is_spam=False )


        return {'message': 'comment marked as ham'}
    except:
        raise HTTPError(http.BAD_REQUEST)


##################################  PROJECTS   #######################################################
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
                    Q('spam_status', 'eq', Node.POSSIBLE_SPAM) &
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

        project.confirm_spam(save=True)
        train_spam_project(project,is_spam=True )



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

        project.confirm_ham(save=True)
        train_spam_project(project,is_spam=False )

        return {'message': 'project marked as ham'}
    except:
        raise HTTPError(http.BAD_REQUEST)











