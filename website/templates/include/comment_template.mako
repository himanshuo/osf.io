<script type="text/html" id="commentTemplate">
    <div class="comment-container" data-bind="if: shouldShow, attr:{id: id}">

        <div class="comment-body">
            <div data-bind="visible: loading">
                <i class="fa fa-spinner fa-spin"></i>
            </div>

            <div data-bind="ifnot: loading">
                <div data-bind="if: isDeleted">
                    <div>
                        <span data-bind="if: hasChildren() && shouldShowChildren()">
                            <i data-bind="css: toggleIcon, click: toggle"></i>
                        </span>
                        Comment deleted.
                        <span data-bind="if: canEdit">
                            <a data-bind="click: startUndelete">Restore</a>
                        </span>
                    </div>
                    <div data-bind="if: canEdit">
                        <div data-bind="if: undeleting">
                            <a class="btn btn-default btn-sm" data-bind="click: submitUndelete">Submit</a>
                            <a class="btn btn-default btn-sm" data-bind="click: cancelUndelete">Cancel</a>
                        </div>
                    </div>
                </div>

                <div data-bind="if: isHidden">
                    <div>
                        <span data-bind="if: hasChildren() && shouldShowChildren()">
                            <i data-bind="css: toggleIcon, click: toggle"></i>
                        </span>
                        The original file or wiki is not accessible from this ${node['node_type']} or has been deleted.
                    </div>
                </div>

                <div data-bind="if: isAbuse">
                    <div>
                        <span data-bind="if: hasChildren() && shouldShowChildren()">
                            <i data-bind="css: toggleIcon, click: toggle"></i>
                        </span>
                        Comment reported. <a data-bind="click: startUnreportAbuse">Not abuse</a>
                    </div>
                    <div data-bind="if: unreporting">
                        <a class="btn btn-primary btn-sm" data-bind="click: submitUnreportAbuse">Submit</a>
                        <a class="btn btn-default btn-sm" data-bind="click: cancelUnreportAbuse">Cancel</a>
                    </div>
                </div>

                <div data-bind="if: isVisible">

                    <div class="comment-info">
                        <form class="form-inline">
                            <span data-bind="if: author.gravatarUrl">
                                <img data-bind="attr: {src: author.gravatarUrl}"/>
                            </span>
                            <span data-bind="if: author.id">
                                <a class="comment-author" data-bind="text: author.fullname, attr: {href: author.url}"></a>
                            </span>
                            <span data-bind="ifnot: author.id">
                                <span class="comment-author" data-bind="text: author.fullname"></span>
                            </span>
                            <span data-bind="if: mode !== 'pane'">
                                <a class="comment-author" data-bind="attr: {href: targetUrl()}, text: cleanTitle"></a>
                            </span>
                            <span class="comment-date pull-right">
                                <span data-bind="template: {if: modified, afterRender: setupToolTips}">
                                    <a data-toggle="tooltip" data-bind="attr: {title: prettyDateModified()}">*</a>
                                </span>
                                <span data-bind="text: prettyDateCreated"></span>
                                &nbsp;
                                <span class="comment-link-icon" data-bind="if: mode == 'widget'">
                                    <a data-bind="attr:{href: '/'+id()}">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Link to comment" class="fa fa-link"></i>
                                    </a>
                                </span>
                            </span>
                        </form>
                    </div>

                    <div>

                        <div class="comment-content">

                            <div data-bind="ifnot: editing">
                                <span data-bind="if: mode !== 'widget' && hasChildren() && shouldShowChildren()">
                                    <i data-bind="css: toggleIcon, click: toggle"></i>
                                </span>
                                <span class="overflow" style="display: inline-block"
                                  data-bind="html: contentDisplay, css: {'edit-comment': editHighlight}, event: {mouseenter: startHoverContent, mouseleave: stopHoverContent}"></span>
                            </div>

                            <!--
                                Hack: Use template binding with if rather than vanilla if
                                binding to get access to afterRender
                            -->
                            <div data-bind="template {if: editing, afterRender: autosizeText}">
                                <div class="form-group" style="padding-top: 10px">
                                    <textarea class="form-control" data-bind="value: content, valueUpdate: 'input', attr: {maxlength: $root.MAXLENGTH}"></textarea>
                                </div>
                                <div class="form-inline">
                                    <a class="btn btn-primary" data-bind="click: submitEdit, visible: editNotEmpty"><i class="fa fa-check-square-o"></i> Save</a>
                                    <a class="btn btn-default" data-bind="click: cancelEdit"><i class="fa fa-undo"></i> Cancel</a>
                                    <span data-bind="text: editErrorMessage" class="comment-error"></span>
                                </div>
                            </div>

                        </div>

                        <div data-bind="ifnot: mode === 'widget'">

                            <span class="comment-error">{{errorMessage}}</span>

                            <span>&nbsp;</span>

                            <!-- Action bar -->
                            <div style="display: inline">
                                <div data-bind="ifnot: editing, event: {mouseover: setupToolTips('i')}" class="comment-actions pull-right">
                                    <a data-bind="attr:{href: '/'+id()}" style="color: #000000">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Link to comment" class="fa fa-link"></i>
                                    </a>
                                    <span data-bind="if: canEdit, click: edit">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Edit" class="fa fa-pencil"></i>
                                    </span>
                                    <span data-bind="if: $root.canComment, click: showReply">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Reply" class="fa fa-reply"></i>
                                    </span>
                                    <span data-bind="if: canReport, click: reportAbuse">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Report" class="fa fa-warning"></i>
                                    </span>
                                    <span data-bind="if: canEdit, click: startDelete">
                                        <i data-toggle="tooltip" data-placement="bottom" title="Delete" class="fa fa-trash-o"></i>
                                    </span>
                                </div>
                            </div>

                        </div>

                        <div class="comment-report" data-bind="if: reporting">
                            <form class="form-inline" data-bind="submit: submitAbuse">
                                <select class="form-control" data-bind="options: abuseOptions, optionsText: abuseLabel, value: abuseCategory"></select>
                                <input class="form-control" data-bind="value: abuseText" placeholder="Describe abuse" />
                            </form>
                            <a class="btn btn-danger btn-sm" data-bind="click: submitAbuse"><i class="fa fa-check-square-o"></i> Report</a>
                            <a class="btn btn-default btn-sm" data-bind="click: cancelAbuse"><i class="fa fa-undo"></i> Cancel</a>
                        </div>

                        <div class="comment-delete" data-bind="if: deleting">
                            <a class="btn btn-danger btn-sm" data-bind="click: submitDelete"><i class="fa fa-check-square-o"></i> Delete</a>
                            <a class="btn btn-default btn-sm" data-bind="click: cancelDelete"><i class="fa fa-undo"></i> Cancel</a>
                        </div>

                    </div>

                </div>
            </div>


        </div>

        <ul class="comment-list">

            <!-- ko if: replying -->

                <div>
                    <div class="form-group" style="padding-top: 10px">
                        <textarea class="form-control" placeholder="Add a comment" data-bind="value: replyContent, valueUpdate: 'input', attr: {maxlength: $root.MAXLENGTH}"></textarea>
                    </div>
                    <div>
                        <a class="btn btn-primary" data-bind="click: submitReply, visible: replyNotEmpty, css: {disabled: submittingReply}"><i class="fa fa-check-square-o"></i> {{saveButtonText}}</a>
                        <a class="btn btn-default" data-bind="click: cancelReply, css: {disabled: submittingReply}"><i class="fa fa-undo"></i> Cancel</a>
                        <span data-bind="text: replyErrorMessage" class="comment-error"></span>
                    </div>
                </div>

            <!-- /ko -->

            <!-- ko if: showChildren() && shouldShowChildren() -->
                <!-- ko template: {name:  'commentTemplate', foreach: comments} -->
                <!-- /ko -->
            <!-- /ko -->

        </ul>

        <div data-bind="if: shouldContinueThread">
            <a data-bind="attr: {href: '/' + id()}">Continue this thread &#8594;</a>
        </div>

    </div>

</script>

