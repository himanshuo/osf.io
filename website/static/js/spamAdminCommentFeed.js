/**
 * Renders a log feed.
 **/
'use strict';

var ko = require('knockout');

var $osf = require('js/osfHelpers');

/**
* Log model.
*/
var SpamAdminComment = function() {
    var self = this;
    self.author = ko.observable('author name');
    self.author_url = ko.observable('www.google.com');
    self.dateCreated = ko.observable('9/20/1995');
    self.dateModified = ko.observable('10/2/2015');
    self.content = ko.observable('fake content');
    self.project = ko.observable('project title');
    self.project_url=ko.observable('www.project.com');
};

/**
* View model for a log list.
* @param {Log[]} logs An array of Log model objects to render.
*/
var SpamAdminCommentViewModel = function(spamAdminComments) {

    var self = this;
    self.spamAdminComments = ko.observableArray(spamAdminComments);


    // ...
};

////////////////
// Public API //
////////////////

var defaults = {
    //data: []
    //progBar: '#logProgressBar'
};

function SpamAdminCommentFeed(selector, options) {

    var self = this;
    self.selector = selector;
    self.options = $.extend({}, defaults, options);
    //self.$progBar = $(self.options.progBar);
    self.spamAdminComments = self.options.data.map(function(spamAdminComment) {
        return new SpamAdminComment();
    });
    $osf.applyBindings(new SpamAdminCommentViewModel(self.spamAdminComments), self.selector);

};

SpamAdminCommentFeed.prototype.get_comments = function() {
    console.log('get_comments called.');
    var self=this;
    var request = this.fetch();
    request.done(function(response) { console.log(response); });
    request.fail(function(error){console.log(error);});

};



SpamAdminCommentFeed.prototype.fetch = function(){
    var self=this;
   console.log('fetch func called');
    // Assign handlers immediately after making the request,
    // and remember the jqxhr object for this request
    var data = $.getJSON( "/spam_admin/list_comments");
    return data;
};


/*

I THINK THIS IS CALLED WHEN A NEW SpamAdminCommentFeed is created. I think the one that is already there doesnt count?
ONLINE, it shows that this method is called inside the SpamAdminCommentFeed prototype definition using:
     this.init.apply(this, arguments);

*/
//// Apply ViewModel bindings
//SpamAdminCommentFeed.prototype.init = function(selector, options) {
//
//    var self = this;
//    //self.$progBar.hide();
//    console.log('spam admin comment feed prototype init called.');
//    $osf.applyBindings(new SpamAdminCommentViewModel(self.spamAdminComments), self.selector);
//
//};

module.exports = SpamAdminCommentFeed;