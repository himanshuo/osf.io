<%inherit file="base.mako"/>
<%def name="title()">Spam Admin</%def>
<%def name="content()">


<div id="himanshu">


   <div  data-bind="foreach: {data: spamAdminComments, as: 'comment'}">
        <div class="search-result well">
            <h4><a data-bind="attr: { href: comment.project_url }" ><span data-bind="text: comment.project"></span></a></h4>
        <p><span data-bind="text: comment.content"></span></p>
            <p>
                <strong>Author:</strong> <span data-bind="text: comment.author"></span>
                <span class="pull-right"><strong>Last Edited:</strong>   <span data-bind="text: comment.dateModified"></span> </span></p>
        </div>

   </div>





</%def>



<%def name="javascript_bottom()">
<script src=${"/static/public/js/spam-admin-page.js" | webpack_asset}></script>
</%def>