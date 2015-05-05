from __future__ import absolute_import
from nose.tools import *  # noqa PEP8 asserts


from framework.auth import Auth
from website.project.model import Comment

from website.settings import SPAM_ASSASSIN
from tests.base import (
    OsfTestCase,
    assert_datetime_equal,
)
from tests.factories import (
    ProjectFactory, AuthUserFactory

)
from website.spam_admin.spam_admin_settings import SPAM_ASSASSIN_URL
import httpretty
from website.spam_admin.utils import train_spam
from website.spam_admin.views import mark_comment_as_spam, mark_comment_as_ham





class TestCommentSpamAdmin(OsfTestCase):


    def setUp(self):
        super(TestCommentSpamAdmin, self).setUp()
        self.project = ProjectFactory(is_public=True)
        self.consolidated_auth = Auth(user=self.project.creator)
        self.non_contributor = AuthUserFactory()
        self.user = AuthUserFactory()
        # self.user.emails[0] = 'spam_admin@cos.com'
        # self.user.fullname = 'spam_admin'
        self.user.save()
        self.project.add_contributor(self.user)
        self.project.save()
        self.spam_admin = SpamAdminFactory()


        #spam assassin
        self.GTUBE = "SPAM"
        self.spam_assassin_active = SPAM_ASSASSIN






    def _configure_project(self, project, comment_level):

        project.comment_level = comment_level
        project.save()


    def _add_comment(self, project, content=None, **kwargs):

        def request_callback(request, uri, headers):
            import json
            data = json.loads(str(request.body))
            if data.get('message') == self.GTUBE:
                return (200, headers, "SPAM")
            return (200, headers, "HAM")

        httpretty.register_uri(
            httpretty.POST, SPAM_ASSASSIN_URL,
            body=request_callback
        )


        content = content if content is not None else 'hammer to fall'
        url = project.api_url + 'comment/'
        ret = self.app.post_json(
            url,
            {
                'content': content,
                'isPublic': 'public',
                'page': 'node',
                'target': project._id
            },
            **kwargs
        )

        return Comment.load(ret.json['comment']['id'])


    ########################## TEST MODEL / UTIL FUNCTIONS  #####################################################
    @httpretty.activate
    def test_comment_added_is_spam(self):
        comment = self._add_comment(
            self.project, content = self.GTUBE, auth=self.project.creator.auth,
        )
        self.project.reload()



        assert_equal(len(self.project.commented), 1)
        if self.spam_assassin_active:
            assert_equal(comment.spam_status , Comment.POSSIBLE_SPAM)
        else:
            assert_equal(comment.spam_status , Comment.UNKNOWN)
    @httpretty.activate
    def test_comment_added_is_not_spam(self):
        comment = self._add_comment(
            self.project,auth=self.project.creator.auth,
        )
        self.project.reload()



        assert_equal(len(self.project.commented), 1)
        assert_equal(comment.spam_status , Comment.UNKNOWN)
    @httpretty.activate
    def test_train_spam_comment(self):
        comment = self._add_comment(
            self.project,content=self.GTUBE, auth=self.project.creator.auth,
        )
        self.project.reload()


        if self.spam_assassin_active:
            assert_true(train_spam(comment, is_spam=True))
        else:
            assert_false(train_spam(comment, is_spam=True))
    @httpretty.activate
    def test_train_ham_comment(self):
        comment = self._add_comment(
            self.project, auth=self.project.creator.auth,
        )
        if self.spam_assassin_active:
            assert_true(train_spam(comment, is_spam=False))
        else:
            assert_false(train_spam(comment, is_spam=False))

    @httpretty.activate
    def test_auto_mark_spam_if_flagged_enough_times(self):
        comment = self._add_comment(
            self.project, auth=self.project.creator.auth,
        )


        for i in range(Comment.NUM_FLAGS_FOR_SPAM):
            reporter = AuthUserFactory()
            url = self.project.api_url + 'comment/{0}/report/'.format(comment._id)
            self.app.post_json(
                url,
                {
                    'category': 'spam',
                    'text': 'ads',
                },
                auth=reporter.auth,
            )

        comment.reload()
        if self.spam_assassin_active:
            assert_equal(comment.spam_status , Comment.POSSIBLE_SPAM)
        else:
            assert_equal(comment.spam_status , Comment.UNKNOWN)
    @httpretty.activate
    def test_dont_auto_mark_spam_if_not_flagged_enough_times(self):
        comment = self._add_comment(
            self.project, auth=self.project.creator.auth,
        )


        for i in range(Comment.NUM_FLAGS_FOR_SPAM-1):
            reporter = AuthUserFactory()
            url = self.project.api_url + 'comment/{0}/report/'.format(comment._id)
            with assert_raises(ValueError):
                self.app.post_json(
                    url,
                    {
                        'category': 'spam',
                        'text': 'ads',
                    },
                    auth=reporter.auth,
                )

        comment.reload()
        assert_equal(comment.spam_status , Comment.UNKNOWN)

    @httpretty.activate
    def test_dont_auto_mark_if_already_ham(self):
        comment_ham = self._add_comment(
            self.project, auth=self.project.creator.auth,
        )
        comment_ham.confirm_ham(save=True)


        for i in range(Comment.NUM_FLAGS_FOR_SPAM):
            reporter = AuthUserFactory()
            comment_ham.report_abuse(reporter, category='spam', text='ads',save=True)

        assert_equal(comment_ham.spam_status , Comment.HAM)

    @httpretty.activate
    def test_dont_auto_mark_if_already_spam(self):
        comment_spam = self._add_comment(
            self.project, auth=self.project.creator.auth,
        )
        comment_spam.confirm_ham(save=True)

        with assert_raises(ValueError):
            for i in range(Comment.NUM_FLAGS_FOR_SPAM):
                reporter = AuthUserFactory()
                comment_spam.unreport_abuse(reporter, save=True)

        assert_equal(comment_spam.spam_status , Comment.HAM)



    ###############################  TEST VIEW   #############################################
    # @httpretty.activate
    # def test_delete_if_marked_as_spam(self):
    #
    #
    #     comment = self._add_comment(
    #         self.project, auth=self.user.auth,
    #     )
    #
    #
    #     self.app.post_json(
    #         '/api/v1/spam_admin/mark_comment_as_spam/',
    #         {
    #             'auth':self.spam_admin.auth,
    #             'cid':comment._id
    #         },
    #     )
    #
    #     # mark_comment_as_spam(auth=self.project.creator.auth, cid=comment._id )
    #
    #     assert_equal(comment.spam_status , Comment.SPAM)


    # def test_delete_if_marked_as_spam(self):
    #     comment = self._add_comment(
    #         self.project, auth=self.project.creator.auth,
    #     )
    #     mark_comment_as_spam(auth=self.project.creator.auth, cid=comment._id )
    #
    #     assert_equal(comment.spam_status , Comment.SPAM)
    #     assert_true(comment.is_deleted)
    #
    #
    # def test_marked_as_ham(self):
    #     comment = self._add_comment(
    #         self.project, auth=self.project.creator.auth,
    #     )
    #     mark_comment_as_ham(auth=self.project.creator.auth, cid=comment._id )
    #     assert_equal(comment.spam_status , Comment.HAM)
    #     assert_false(comment.is_deleted)
    #
    # # def test_list_possible_spam_comments(self):
    # #     for i in range(5):
    # #         self._add_comment(
    # #             self.project, content=self.GTUBE,auth=self.project.creator.auth,
    # #         )
    # #         self._add_comment(
    # #             self.project, auth=self.project.creator.auth,
    # #         )
    # #
    # #     list_comment_page(
    # #
    # #     )
    # #     assert_equal(comment.spam_status == Comment.HAM)
    # #     assert_false(comment.is_deleted)

