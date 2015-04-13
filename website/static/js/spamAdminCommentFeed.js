/**
 * Renders a log feed.
 **/
'use strict';

var ko = require('knockout');

var $osf = require('js/osfHelpers');




/**
* Log model.
*/
var SpamAdminComment = function(data) {
    var self = this;

    self.cid=data.cid;
    self.author = ko.observable(data.author.name);
    self.author_url = ko.observable(data.author.url);
    self.dateCreated = ko.observable(data.dateCreated);
    self.dateModified = ko.observable(data.dateModified);
    self.content = ko.observable(data.content);
    self.project = ko.observable(data.project);
    self.project_url=ko.observable(data.project_url);




};


SpamAdminComment.prototype.markSpam = function(){
    var self=this;
 $osf.postJSON(
            "api/v1/spam_admin/mark_comment_as_spam/",
            {
                "cid":self.cid
            }
        ).done(function(response) {
            return true;
        }).fail(function(response) {
            return false;
        });
}


SpamAdminComment.prototype.markHam = function(){
    var self=this;
 $osf.postJSON(
            "/api/v1/spam_admin/mark_comment_as_ham/",
            {
                "cid":self.cid
            }
        ).done(function(response) {
            console.log(response);
            return true;
        }).fail(function(response) {
            return false;
        });
}


/**
* View model for a log list.
* @param {Log[]} logs An array of Log model objects to render.
*/
var SpamAdminCommentViewModel = function(spamAdminComments) {

    var self = this;
    self.spamAdminComments = ko.observableArray([]);

    self.total = ko.observable(3);

    self.fill_comment_list();



    // ...
};


SpamAdminCommentViewModel.prototype.markHam = function(spamAdminComment){
    var self = this;




    if (spamAdminComment.markHam()){
        self.spamAdminComments.remove(spamAdminComment);
        self.spamAdminComments.remove(spamAdminComment);


        $osf.growl('Comment Marked as Ham',"", 'success');
    }

};
SpamAdminCommentViewModel.prototype.markSpam = function(spamAdminComment){
    var self = this;


    if (spamAdminComment.markSpam()){
        self.spamAdminComments.remove(spamAdminComment);
         self.spamAdminComments.remove(spamAdminComment);

        $osf.growl('Comment Marked as Spam',"", 'success');

    }


};
//Array.prototype.remove = function(elementToDelete){
//    var self=this;
//    var i = self.indexOf(elementToDelete)
//    if(i>-1){
//        self.splice(i, 1);
//        return true;
//    }
//    return false;
//}



SpamAdminCommentViewModel.prototype.fill_comment_list = function(){
  var self = this;
  var amount = 90-self.spamAdminComments.length
  if(amount>0){
      self.get_comments(amount);
  }
};

SpamAdminCommentViewModel.prototype.get_comments = function(amount) {


    var self=this;

    var request = self.fetch(amount);
    request.done(function(response) {

        var newComments = response.comments.map(function(data){
            return new SpamAdminComment(data);
        });


        //it is better to extend an array at once rather then manually add multiple times because each addition
        //forces knockout to reload. DO THAT. apply is just pushing foreach new comment. SLOW. FIX. TODO: make fast.
        self.spamAdminComments.push.apply(self.spamAdminComments, newComments);


        self.total(response.total);

    });
    request.fail(function(error){console.log(error);});

};


SpamAdminCommentViewModel.prototype.fetch = function(amount){
    var self=this;

    var query_url = "/api/v1/spam_admin/list_comments/";
    if (amount){
        query_url += amount;
    }


    var data = $.getJSON(query_url);
    return data;
};








////////////////
// Public API //
////////////////



function SpamAdminCommentFeed(selector, options) {

    var self = this;
    self.selector = selector;

    self.init();



};






/*

I THINK THIS IS CALLED WHEN A NEW SpamAdminCommentFeed is created. I think the one that is already there doesnt count?
ONLINE, it shows that this method is called inside the SpamAdminCommentFeed prototype definition using:
     this.init.apply(this, arguments);

*/
//// Apply ViewModel bindings
SpamAdminCommentFeed.prototype.init = function() {

    var self = this;
    //self.$progBar.hide();

    $osf.applyBindings(new SpamAdminCommentViewModel(self.spamAdminComments), self.selector);



};

module.exports = SpamAdminCommentFeed;